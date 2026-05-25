import unittest
from unittest.mock import MagicMock, patch
from axis_base import AxisDevice
from vmd_manager import VMDManager
from param_manager import ParamManager
from ptz_manager import PTZManager
from mqtt_manager import MQTTManager
from overlay_manager import OverlayManager
from storage_manager import StorageManager

class TestAxisFramework(unittest.TestCase):

    @patch('requests.Session')
    def test_axis_device_get(self, mock_session_cls):
        mock_session = mock_session_cls.return_value
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "OK"
        mock_session.get.return_value = mock_response

        device = AxisDevice("1.2.3.4", "user", "pass")
        resp = device.get("/test", params={"a": 1})

        mock_session.get.assert_called_once_with("http://1.2.3.4/test", params={"a": 1})
        self.assertEqual(resp.text, "OK")

    @patch('requests.Session')
    def test_vmd_manager(self, mock_session_cls):
        mock_session = mock_session_cls.return_value

        # Test get_config
        mock_get_resp = MagicMock()
        mock_get_resp.status_code = 200
        mock_get_resp.json.return_value = {"profiles": []}
        mock_session.get.return_value = mock_get_resp

        device = AxisDevice("1.2.3.4", "user", "pass")
        vmd = VMDManager(device)
        config = vmd.get_config()
        self.assertEqual(config, {"profiles": []})
        mock_session.get.assert_called_with("http://1.2.3.4/axis-cgi/vmd/config.cgi", params=None)

        # Test set_config
        mock_post_resp = MagicMock()
        mock_post_resp.status_code = 200
        mock_session.post.return_value = mock_post_resp

        success = vmd.set_config({"profiles": []})
        self.assertTrue(success)
        mock_session.post.assert_called_with("http://1.2.3.4/axis-cgi/vmd/config.cgi", json={"profiles": []})

    @patch('requests.Session')
    def test_param_manager(self, mock_session_cls):
        mock_session = mock_session_cls.return_value
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "OK"
        mock_session.get.return_value = mock_response

        device = AxisDevice("1.2.3.4", "user", "pass")
        pm = ParamManager(device)

        # Test update
        result = pm.update_param("Group.Path", "value")
        mock_session.get.assert_called_with("http://1.2.3.4/axis-cgi/param.cgi", params={"action": "update", "Group.Path": "value"})
        self.assertEqual(result, "OK")

        # Test get
        result_get = pm.get_param("Group.Path")
        mock_session.get.assert_called_with("http://1.2.3.4/axis-cgi/param.cgi", params={"action": "list", "group": "Group.Path"})
        self.assertEqual(result_get, "OK")

    @patch('requests.Session')
    def test_param_manager_batch(self, mock_session_cls):
        mock_session = mock_session_cls.return_value
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "OK"
        mock_session.get.return_value = mock_response

        device = AxisDevice("1.2.3.4", "user", "pass")
        pm = ParamManager(device)

        # Test batch update
        params_update = {"root.Image.I0.Appearance.Brightness": "50", "root.Image.I0.Appearance.Contrast": "50"}
        pm.update_params(params_update)
        expected_params_update = {"action": "update"}
        expected_params_update.update(params_update)
        mock_session.get.assert_called_with("http://1.2.3.4/axis-cgi/param.cgi", params=expected_params_update)

        # Test batch get
        params_get = ["root.Network", "root.System"]
        pm.get_params(params_get)
        mock_session.get.assert_called_with("http://1.2.3.4/axis-cgi/param.cgi", params={"action": "list", "group": "root.Network,root.System"})

    @patch('requests.Session')
    def test_ptz_manager(self, mock_session_cls):
        mock_session = mock_session_cls.return_value
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "OK"
        mock_session.get.return_value = mock_response

        device = AxisDevice("1.2.3.4", "user", "pass")
        ptz = PTZManager(device)

        ptz.move("left")
        mock_session.get.assert_called_with("http://1.2.3.4/axis-cgi/com/ptz.cgi", params={"move": "left"})

        ptz.go_to_preset("Entrance")
        mock_session.get.assert_called_with("http://1.2.3.4/axis-cgi/com/ptz.cgi", params={"gotoserverpresetname": "Entrance"})

    @patch('requests.Session')
    def test_mqtt_manager(self, mock_session_cls):
        mock_session = mock_session_cls.return_value
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success"}
        mock_session.post.return_value = mock_response

        device = AxisDevice("1.2.3.4", "user", "pass")
        mqtt = MQTTManager(device)

        mqtt.activate_client()
        mock_session.post.assert_called_with("http://1.2.3.4/axis-cgi/mqtt/client.cgi", json={"apiVersion": "1.0", "method": "activateClient"})

    @patch('requests.Session')
    def test_overlay_manager(self, mock_session_cls):
        mock_session = mock_session_cls.return_value
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success"}
        mock_session.post.return_value = mock_response

        device = AxisDevice("1.2.3.4", "user", "pass")
        overlay = OverlayManager(device)

        overlay.list_overlays()
        mock_session.post.assert_called_with("http://1.2.3.4/axis-cgi/dynamicoverlay.cgi", json={"apiVersion": "1.0", "method": "list"})

    @patch('requests.Session')
    def test_storage_manager(self, mock_session_cls):
        mock_session = mock_session_cls.return_value
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success"}
        mock_session.post.return_value = mock_response

        device = AxisDevice("1.2.3.4", "user", "pass")
        storage = StorageManager(device)

        storage.get_storage_status()
        mock_session.post.assert_called_with("http://1.2.3.4/axis-cgi/storage/status.cgi", json={"apiVersion": "1.0", "method": "getStatus"})

    @patch('requests.Session')
    def test_encoding_default(self, mock_session_cls):
        mock_session = mock_session_cls.return_value
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.encoding = None  # Simulate no encoding set
        mock_session.get.return_value = mock_response
        mock_session.post.return_value = mock_response

        device = AxisDevice("1.2.3.4", "user", "pass")

        # Test GET
        resp_get = device.get("/test")
        self.assertEqual(resp_get.encoding, 'utf-8')

        # Test POST
        resp_post = device.post("/test", json_data={})
        self.assertEqual(resp_post.encoding, 'utf-8')

if __name__ == '__main__':
    unittest.main()
