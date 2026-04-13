import unittest
from unittest.mock import MagicMock, patch
from axis_base import AxisDevice
from vmd_manager import VMDManager
from param_manager import ParamManager

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
        result = pm.update_param("Group.Path", "value")

        mock_session.get.assert_called_with("http://1.2.3.4/axis-cgi/param.cgi", params={"action": "update", "Group.Path": "value"})
        self.assertEqual(result, "OK")

if __name__ == '__main__':
    unittest.main()
