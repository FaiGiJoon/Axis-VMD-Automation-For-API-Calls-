from axis_base import AxisDevice

class OverlayManager:
    def __init__(self, device: AxisDevice):
        self.device = device

    def list_overlays(self):
        """Lists all dynamic overlays."""
        path = "/axis-cgi/dynamicoverlay.cgi"
        data = {
            "apiVersion": "1.0",
            "method": "list"
        }
        return self.device.post(path, json_data=data).json()

    def create_overlay(self, overlay_config):
        """
        Creates a new dynamic overlay.
        :param overlay_config: Dictionary containing overlay configuration.
        """
        path = "/axis-cgi/dynamicoverlay.cgi"
        data = {
            "apiVersion": "1.0",
            "method": "create",
            "params": overlay_config
        }
        return self.device.post(path, json_data=data).json()

    def remove_overlay(self, overlay_id):
        """Removes a dynamic overlay."""
        path = "/axis-cgi/dynamicoverlay.cgi"
        data = {
            "apiVersion": "1.0",
            "method": "remove",
            "params": {"id": overlay_id}
        }
        return self.device.post(path, json_data=data).json()

    def update_overlay(self, overlay_id, overlay_config):
        """Updates an existing dynamic overlay."""
        path = "/axis-cgi/dynamicoverlay.cgi"
        data = {
            "apiVersion": "1.0",
            "method": "setConfiguration",
            "params": {
                "id": overlay_id,
                **overlay_config
            }
        }
        return self.device.post(path, json_data=data).json()
