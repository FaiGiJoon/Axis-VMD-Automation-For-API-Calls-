from axis_base import AxisDevice

class ParamManager:
    def __init__(self, device: AxisDevice):
        self.device = device

    def update_param(self, group_path, value):
        path = "/axis-cgi/param.cgi"
        params = {"action": "update", group_path: value}
        return self.device.get(path, params=params).text
