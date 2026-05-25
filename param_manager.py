from axis_base import AxisDevice

class ParamManager:
    def __init__(self, device: AxisDevice):
        self.device = device

    def get_param(self, group_path):
        """Retrieves a single parameter."""
        return self.get_params([group_path])

    def get_params(self, group_paths=None):
        """
        Retrieves multiple parameter groups in a single HTTP request.
        :param group_paths: A list of parameter group paths (e.g., ['root.Network', 'root.System']).
                           If None, retrieves all parameters.
        """
        # Optimization: Batching multiple parameter reads reduces network
        # round-trip overhead significantly. Passing multiple groups as a
        # comma-separated list is more efficient than individual requests.
        path = "/axis-cgi/param.cgi"
        params = {"action": "list"}
        if group_paths:
            params["group"] = ",".join(group_paths)
        return self.device.get(path, params=params).text

    def update_param(self, group_path, value):
        """Updates a single parameter."""
        return self.update_params({group_path: value})

    def update_params(self, params_dict):
        """
        Updates multiple parameters in a single HTTP request.
        :param params_dict: A dictionary of group_path: value pairs.
        """
        # Optimization: Batching multiple parameter updates reduces network
        # round-trip overhead significantly compared to individual requests.
        path = "/axis-cgi/param.cgi"
        params = {"action": "update"}
        params.update(params_dict)
        return self.device.get(path, params=params).text
