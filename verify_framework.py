import unittest
from unittest.mock import patch, MagicMock
from axis_base import AxisDevice
from vmd_manager import VMDManager
from param_manager import ParamManager
from ptz_manager import PTZManager
from mqtt_manager import MQTTManager
from overlay_manager import OverlayManager
from storage_manager import StorageManager

class TestAxisFramework(unittest.TestCase):

    def setUp(self):
        self.device = AxisDevice("1.2.3.4", "admin", "pass")

    @patch('axis_base.requests.Session')
    def test_axis_device_get(self, mock_session_class):
        mock_session = mock_session_class.return_value
        self.device.session = mock_session
        mock_session.get.return_value.status_code = 200
        mock_session.get.return_value.text = "OK"
        mock_session.get.return_value.encoding = 'utf-8'

        self.device.get("/test", params={"a": 1})
        mock_session.get.assert_called_once_with("http://1.2.3.4/test", params={"a": 1}, timeout=10, stream=False)

    @patch('axis_base.requests.Session')
    def test_vmd_manager(self, mock_session_class):
        mock_session = mock_session_class.return_value
        self.device.session = mock_session
        vmd = VMDManager(self.device)

        # Test get_config
        mock_session.get.return_value.status_code = 200
        mock_session.get.return_value.json.return_value = {"profiles": []}
        mock_session.get.return_value.encoding = 'utf-8'

        config = vmd.get_config()
        self.assertEqual(config, {"profiles": []})
        mock_session.get.assert_called_with("http://1.2.3.4/axis-cgi/vmd/config.cgi", params=None, timeout=10, stream=False)

        # Test set_config
        mock_session.post.return_value.status_code = 200
        mock_session.post.return_value.encoding = 'utf-8'
        success = vmd.set_config({"profiles": []})
        self.assertTrue(success)
        mock_session.post.assert_called_with("http://1.2.3.4/axis-cgi/vmd/config.cgi", json={"profiles": []}, params=None, timeout=10)

    @patch('axis_base.requests.Session')
    def test_param_manager(self, mock_session_class):
        mock_session = mock_session_class.return_value
        self.device.session = mock_session
        pm = ParamManager(self.device)

        mock_session.get.return_value.status_code = 200
        mock_session.get.return_value.text = "Group.Path=value"
        mock_session.get.return_value.encoding = 'utf-8'

        # Test get_param
        val = pm.get_param("Group.Path")
        self.assertIn("Group.Path=value", val)

        # Test update_param
        pm.update_param("Group.Path", "value")
        mock_session.get.assert_called_with("http://1.2.3.4/axis-cgi/param.cgi", params={"action": "update", "Group.Path": "value"}, timeout=10, stream=False)

    @patch('axis_base.requests.Session')
    def test_param_manager_batch(self, mock_session_class):
        mock_session = mock_session_class.return_value
        self.device.session = mock_session
        pm = ParamManager(self.device)

        mock_session.get.return_value.status_code = 200
        mock_session.get.return_value.text = "OK"
        mock_session.get.return_value.encoding = 'utf-8'

        # Test batch get
        pm.get_params(["root.Network", "root.System"])
        mock_session.get.assert_called_with("http://1.2.3.4/axis-cgi/param.cgi", params={"action": "list", "group": "root.Network,root.System"}, timeout=10, stream=False)

        # Test batch update
        pm.update_params({
            "root.Image.I0.Appearance.Brightness": "50",
            "root.Image.I0.Appearance.Contrast": "50"
        })
        expected_params_update = {
            "action": "update",
            "root.Image.I0.Appearance.Brightness": "50",
            "root.Image.I0.Appearance.Contrast": "50"
        }
        mock_session.get.assert_called_with("http://1.2.3.4/axis-cgi/param.cgi", params=expected_params_update, timeout=10, stream=False)

    @patch('axis_base.requests.Session')
    def test_ptz_manager(self, mock_session_class):
        mock_session = mock_session_class.return_value
        self.device.session = mock_session
        ptz = PTZManager(self.device)

        mock_session.get.return_value.status_code = 200
        mock_session.get.return_value.text = "OK"
        mock_session.get.return_value.encoding = 'utf-8'

        ptz.move("left")
        mock_session.get.assert_called_with("http://1.2.3.4/axis-cgi/com/ptz.cgi", params={"move": "left"}, timeout=10, stream=False)

        ptz.go_to_preset("Entrance")
        mock_session.get.assert_called_with("http://1.2.3.4/axis-cgi/com/ptz.cgi", params={"gotoserverpresetname": "Entrance"}, timeout=10, stream=False)

    @patch('axis_base.requests.Session')
    def test_mqtt_manager(self, mock_session_class):
        mock_session = mock_session_class.return_value
        self.device.session = mock_session
        mqtt = MQTTManager(self.device)

        mock_session.post.return_value.status_code = 200
        mock_session.post.return_value.json.return_value = {"apiVersion": "1.0", "method": "activateClient"}
        mock_session.post.return_value.encoding = 'utf-8'

        mqtt.activate_client()
        mock_session.post.assert_called_with("http://1.2.3.4/axis-cgi/mqtt/client.cgi", json={"apiVersion": "1.0", "method": "activateClient"}, params=None, timeout=10)

    @patch('axis_base.requests.Session')
    def test_overlay_manager(self, mock_session_class):
        mock_session = mock_session_class.return_value
        self.device.session = mock_session
        overlay = OverlayManager(self.device)

        mock_session.post.return_value.status_code = 200
        mock_session.post.return_value.json.return_value = {"apiVersion": "1.0", "method": "list"}
        mock_session.post.return_value.encoding = 'utf-8'

        overlay.list_overlays()
        mock_session.post.assert_called_with("http://1.2.3.4/axis-cgi/dynamicoverlay.cgi", json={"apiVersion": "1.0", "method": "list"}, params=None, timeout=10)

    @patch('axis_base.requests.Session')
    def test_storage_manager(self, mock_session_class):
        mock_session = mock_session_class.return_value
        self.device.session = mock_session
        storage = StorageManager(self.device)

        mock_session.post.return_value.status_code = 200
        mock_session.post.return_value.json.return_value = {"apiVersion": "1.0", "method": "getStatus"}
        mock_session.post.return_value.encoding = 'utf-8'

        storage.get_storage_status()
        mock_session.post.assert_called_with("http://1.2.3.4/axis-cgi/storage/status.cgi", json={"apiVersion": "1.0", "method": "getStatus"}, params=None, timeout=10)

if __name__ == '__main__':
    unittest.main()
