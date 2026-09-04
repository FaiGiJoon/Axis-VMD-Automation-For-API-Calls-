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

    def get_app_info(self, app_id):
        return self.get_apps_dict().get(app_id)
