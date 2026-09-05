import xml.etree.ElementTree as ET

class AppManager:
    def __init__(self, device):
        self.device = device

    def list_apps(self):
        """Lists all installed ACAP applications."""
        path = "/axis-cgi/applications/list.cgi"
        response = self.device.post(path)

        # Optimization: Parse raw bytes directly via response.content to avoid Python string decoding overhead
        root = ET.fromstring(response.content)
        apps = []
        for app in root.findall('application'):
            apps.append(app.attrib)
        return apps

    def get_apps_dict(self):
        """Returns a dictionary mapping application names to application attributes for O(1) lookup."""
        return {app.get('Name'): app for app in self.list_apps() if app.get('Name')}

    def upload_app(self, file_data, filename="package.eap"):
        """
        Uploads an ACAP application package (.eap) to the Axis device.
        :param file_data: bytes or file-like object containing the .eap file data.
        :param filename: name of the file being uploaded.
        """
        path = "/axis-cgi/applications/upload.cgi"
        files = {
            'file': (filename, file_data, 'application/octet-stream')
        }
        response = self.device.post(path, files=files)
        return response.text.strip() == "OK"

    def control_app(self, app_id, action):
        """
        Controls an ACAP application.
        :param app_id: The application package name (e.g., 'vmd').
        :param action: start, stop, restart, remove.
        """
        path = "/axis-cgi/applications/control.cgi"
        params = {
            "action": action,
            "package": app_id
        }
        response = self.device.post(path, params=params)
        return response.text.strip() == "OK"

    def start_app(self, app_id):
        return self.control_app(app_id, "start")

    def stop_app(self, app_id):
        return self.control_app(app_id, "stop")

    def restart_app(self, app_id):
        return self.control_app(app_id, "restart")

    def remove_app(self, app_id):
        return self.control_app(app_id, "remove")

    def get_app_info(self, app_id):
        return self.get_apps_dict().get(app_id)

    def get_config_param(self, name):
        """
        Retrieves the value of a global application configuration parameter (e.g., AllowUnsigned, AllowRoot).
        """
        path = "/axis-cgi/applications/config.cgi"
        params = {
            "action": "get",
            "name": name
        }
        response = self.device.post(path, params=params)
        root = ET.fromstring(response.content)
        if root.attrib.get("result") == "ok":
            param_elem = root.find("param")
            if param_elem is not None:
                return param_elem.attrib.get("value")
        return None

    def set_config_param(self, name, value):
        """
        Sets the value of a global application configuration parameter.
        :param name: parameter name (e.g., 'AllowUnsigned')
        :param value: value to set (bool or str)
        """
        path = "/axis-cgi/applications/config.cgi"
        if isinstance(value, bool):
            value = "true" if value else "false"
        params = {
            "action": "set",
            "name": name,
            "value": str(value)
        }
        response = self.device.post(path, params=params)
        root = ET.fromstring(response.content)
        return root.attrib.get("result") == "ok"

    def upload_license_key(self, app_id, license_data=None):
        """
        Uploads a license key for a specified application.
        :param app_id: application package name.
        :param license_data: optional license key content/data to upload.
        """
        path = "/axis-cgi/applications/license.cgi"
        params = {
            "action": "uploadlicensekey",
            "package": app_id
        }
        response = self.device.post(path, params=params, data=license_data)
        return response.text.strip() == "OK"

    def remove_license_key(self, app_id):
        """
        Removes a license key for a specified application.
        :param app_id: application package name.
        """
        path = "/axis-cgi/applications/license.cgi"
        params = {
            "action": "removelicensekey",
            "package": app_id
        }
        response = self.device.post(path, params=params)
        return response.text.strip() == "OK"

    def get_supported_sdks(self):
        """
        Retrieves general information related to ACAP support, returning a list of supported SDKs.
        """
        path = "/axis-cgi/applications/info.cgi"
        response = self.device.post(path)
        root = ET.fromstring(response.content)
        sdks = []
        for sdk in root.findall(".//supportedSdks/sdk"):
            if sdk.text:
                sdks.append(sdk.text)
        return sdks
