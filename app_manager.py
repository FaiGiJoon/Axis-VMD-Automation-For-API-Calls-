import xml.etree.ElementTree as ET

class AppManager:
    def __init__(self, device):
        self.device = device

    def list_apps(self):
        """Lists all installed ACAP applications."""
        path = "/axis-cgi/applications/list.cgi"
        response = self.device.post(path)

        # Parse XML response
        root = ET.fromstring(response.text)
        apps = []
        for app in root.findall('application'):
            apps.append(app.attrib)
        return apps

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
        apps = self.list_apps()
        for app in apps:
            if app.get('Name') == app_id:
                return app
        return None
