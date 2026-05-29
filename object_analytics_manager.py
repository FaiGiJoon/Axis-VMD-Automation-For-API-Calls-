class ObjectAnalyticsManager:
    def __init__(self, device):
        self.device = device
        self.endpoint = "/local/objectanalytics/control.cgi"

    def _call(self, method, params=None):
        data = {
            "apiVersion": "1.2",
            "context": "AxisVapixAutomation",
            "method": method
        }
        if params:
            data["params"] = params

        response = self.device.post(self.endpoint, json_data=data)
        return response.json()

    def get_configuration(self):
        """Retrieves the complete AOA application configuration."""
        return self._call("getConfiguration")

    def get_capabilities(self):
        """Retrieves AOA configuration capabilities."""
        return self._call("getConfigurationCapabilities")

    def set_configuration(self, config):
        """
        Applies a complete AOA application configuration.
        :param config: The configuration data object.
        """
        return self._call("setConfiguration", params=config)

    def get_supported_versions(self):
        """Retrieves supported API versions."""
        return self._call("getSupportedVersions")

    def send_alarm_event(self, scenario_id):
        """Triggers a test alarm for a specific scenario."""
        return self._call("sendAlarmEvent", params={"scenario": scenario_id})
