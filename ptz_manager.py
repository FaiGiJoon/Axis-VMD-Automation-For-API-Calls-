from axis_base import AxisDevice

class PTZManager:
    def __init__(self, device: AxisDevice):
        self.device = device

    def move(self, move_cmd):
        """
        Executes a continuous move command.
        :param move_cmd: String like 'left', 'right', 'up', 'down'
        """
        path = "/axis-cgi/com/ptz.cgi"
        params = {"move": move_cmd}
        return self.device.get(path, params=params).text

    def zoom(self, zoom_val):
        """
        Executes a zoom command.
        :param zoom_val: Integer or zoom command
        """
        path = "/axis-cgi/com/ptz.cgi"
        params = {"zoom": str(zoom_val)}
        return self.device.get(path, params=params).text

    def go_to_preset(self, preset_name):
        """Moves the camera to a specific preset."""
        path = "/axis-cgi/com/ptz.cgi"
        params = {"gotoserverpresetname": preset_name}
        return self.device.get(path, params=params).text

    def list_presets(self, camera=1):
        """Lists all server presets for a camera."""
        path = "/axis-cgi/com/ptz.cgi"
        params = {"query": "presetname", "camera": camera}
        return self.device.get(path, params=params).text

    def go_home(self, camera=1):
        """Moves the camera to its home position."""
        path = "/axis-cgi/com/ptz.cgi"
        params = {"move": "home", "camera": camera}
        return self.device.get(path, params=params).text
