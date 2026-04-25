from axis_base import AxisDevice

class ParamManager:
    def __init__(self, device: AxisDevice):
        self.device = device

    def update_params(self, params_dict):
        """
        Updates multiple parameters in a single HTTP request.
        This reduces network overhead and round-trip time.
        """
        path = "/axis-cgi/param.cgi"
        params = {"action": "update"}
        params.update(params_dict)
        return self.device.get(path, params=params).text

    def update_param(self, group_path, value):
        """Updates a single parameter by wrapping the batch update method."""
        return self.update_params({group_path: value})
