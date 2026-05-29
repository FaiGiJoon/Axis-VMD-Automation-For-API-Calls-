import unittest
from unittest.mock import MagicMock, patch
from axis_base import AxisDevice
from app_manager import AppManager
from object_analytics_manager import ObjectAnalyticsManager
from image_manager import ImageManager

class TestNewManagers(unittest.TestCase):
    def setUp(self):
        self.device = AxisDevice("192.168.1.100", "admin", "pass")
        # Mock the session to avoid real network calls
        self.device.session = MagicMock()

    def test_app_manager_list(self):
        mock_xml = """<reply result="ok">
            <application Name="vmd" Status="Running" NiceName="Video Motion Detection"/>
        </reply>"""
        self.device.session.post.return_value.text = mock_xml

        apps = self.device.apps.list_apps()
        self.assertEqual(len(apps), 1)
        self.assertEqual(apps[0]['Name'], 'vmd')
        self.assertEqual(apps[0]['Status'], 'Running')

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

if __name__ == '__main__':
    unittest.main()
