import unittest
from unittest.mock import MagicMock, patch
from axis_base import AxisDevice
from app_manager import AppManager
from object_analytics_manager import ObjectAnalyticsManager
from image_manager import ImageManager
from recording_manager import RecordingManager
from device_data_hub_manager import DeviceDataHubManager

class TestNewManagers(unittest.TestCase):
    def setUp(self):
        self.device = AxisDevice("192.168.1.100", "admin", "pass")
        # Mock the session to avoid real network calls
        self.device.session = MagicMock()

    def test_app_manager_list(self):
        mock_xml = """<reply result="ok">
            <application Name="vmd" Status="Running" NiceName="Video Motion Detection"/>
        </reply>"""
        self.device.session.post.return_value.content = mock_xml.encode('utf-8')
        self.device.session.post.return_value.text = mock_xml

        apps = self.device.apps.list_apps()
        self.assertEqual(len(apps), 1)
        self.assertEqual(apps[0]['Name'], 'vmd')
        self.assertEqual(apps[0]['Status'], 'Running')

    def test_app_manager_get_apps_dict(self):
        mock_xml = """<reply result="ok">
            <application Name="vmd" Status="Running" NiceName="Video Motion Detection"/>
            <application Name="analytics" Status="Stopped" NiceName="Analytics"/>
        </reply>"""
        self.device.session.post.return_value.content = mock_xml.encode('utf-8')

        apps_dict = self.device.apps.get_apps_dict()
        self.assertEqual(len(apps_dict), 2)
        self.assertIn('vmd', apps_dict)
        self.assertEqual(apps_dict['vmd']['Status'], 'Running')

        app_info = self.device.apps.get_app_info('analytics')
        self.assertEqual(app_info['Status'], 'Stopped')

    def test_app_manager_control(self):
        self.device.session.post.return_value.text = "OK"
        success = self.device.apps.start_app("vmd")
        self.assertTrue(success)
        self.device.session.post.assert_called_with(
            "http://192.168.1.100/axis-cgi/applications/control.cgi",
            json=None,
            params={"action": "start", "package": "vmd"},
            timeout=10
        )

    def test_recording_manager(self):
        self.device.session.get.return_value.text = "OK"

        rec = self.device.recording
        rec.list_recording_groups()
        self.device.session.get.assert_called_with(
            "http://192.168.1.100/axis-cgi/record/recording_group/list.cgi",
            params={"schemaversion": "1"},
            timeout=10,
            stream=False
        )

        rec.get_recording_spans(recording_id="rec_1")
        self.device.session.get.assert_called_with(
            "http://192.168.1.100/axis-cgi/record/spans.cgi",
            params={"schemaversion": "1", "recordingid": "rec_1"},
            timeout=10,
            stream=False
        )

        rec.get_recording_segments(recording_id="rec_1", span_id="span_1")
        self.device.session.get.assert_called_with(
            "http://192.168.1.100/axis-cgi/record/segments.cgi",
            params={"schemaversion": "1", "recordingid": "rec_1", "spanid": "span_1"},
            timeout=10,
            stream=False
        )

        rec.search_recordings(start_time="2026-01-01T00:00:00Z")
        self.device.session.get.assert_called_with(
            "http://192.168.1.100/axis-cgi/record/search.cgi",
            params={"schemaversion": "1", "starttime": "2026-01-01T00:00:00Z"},
            timeout=10,
            stream=False
        )

        rec.get_playback_uri(recording_id="rec_1")
        self.device.session.get.assert_called_with(
            "http://192.168.1.100/axis-cgi/record/playback.cgi",
            params={"schemaversion": "1", "recordingid": "rec_1", "format": "h264"},
            timeout=10,
            stream=False
        )

    def test_device_data_hub_manager(self):
        mock_json = {"apiVersion": "1.0", "data": {"status": "ok"}}
        self.device.session.post.return_value.json.return_value = mock_json

        ddh = self.device.device_data_hub
        status = ddh.get_status()
        self.assertEqual(status, mock_json)
        self.device.session.post.assert_called_with(
            "http://192.168.1.100/axis-cgi/devicedatahub.cgi",
            json={"apiVersion": "1.0", "method": "getStatus"},
            params=None,
            timeout=10
        )

        ddh.subscribe("com.axis.events")
        self.device.session.post.assert_called_with(
            "http://192.168.1.100/axis-cgi/devicedatahub.cgi",
            json={"apiVersion": "1.0", "method": "subscribe", "params": {"topic": "com.axis.events"}},
            params=None,
            timeout=10
        )

        ddh.unsubscribe("com.axis.events")
        self.device.session.post.assert_called_with(
            "http://192.168.1.100/axis-cgi/devicedatahub.cgi",
            json={"apiVersion": "1.0", "method": "unsubscribe", "params": {"topic": "com.axis.events"}},
            params=None,
            timeout=10
        )

    def test_aoa_manager_get_config(self):
        mock_json = {"data": {"scenarios": []}}
        self.device.session.post.return_value.json.return_value = mock_json

        config = self.device.aoa.get_configuration()
        self.assertEqual(config, mock_json)

    def test_image_manager_snapshot(self):
        self.device.session.get.return_value.content = b"fakejpegdata"

        img = self.device.image.get_snapshot(resolution="640x480")
        self.assertEqual(img, b"fakejpegdata")
        self.device.session.get.assert_called_with(
            "http://192.168.1.100/axis-cgi/jpg/image.cgi",
            params={"camera": 1, "resolution": "640x480"},
            timeout=10,
            stream=True
        )

    def test_fluent_api_caching(self):
        # Ensure managers are cached and not recreated
        apps1 = self.device.apps
        apps2 = self.device.apps
        self.assertIs(apps1, apps2)

        rec1 = self.device.recording
        rec2 = self.device.recording
        self.assertIs(rec1, rec2)

        ddh1 = self.device.device_data_hub
        ddh2 = self.device.device_data_hub
        self.assertIs(ddh1, ddh2)

if __name__ == '__main__':
    unittest.main()
