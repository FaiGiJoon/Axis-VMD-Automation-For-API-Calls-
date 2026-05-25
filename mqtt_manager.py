from axis_base import AxisDevice

class MQTTManager:
    def __init__(self, device: AxisDevice):
        self.device = device

    def configure_client(self, config):
        """
        Configures the MQTT client.
        :param config: Dictionary containing MQTT client configuration.
        """
        path = "/axis-cgi/mqtt/client.cgi"
        data = {
            "apiVersion": "1.0",
            "method": "configureClient",
            "params": config
        }
        return self.device.post(path, json_data=data).json()

    def activate_client(self):
        """Activates the MQTT client."""
        path = "/axis-cgi/mqtt/client.cgi"
        data = {
            "apiVersion": "1.0",
            "method": "activateClient"
        }
        return self.device.post(path, json_data=data).json()

    def deactivate_client(self):
        """Deactivates the MQTT client."""
        path = "/axis-cgi/mqtt/client.cgi"
        data = {
            "apiVersion": "1.0",
            "method": "deactivateClient"
        }
        return self.device.post(path, json_data=data).json()

    def get_client_status(self):
        """Returns the current MQTT client status."""
        path = "/axis-cgi/mqtt/client.cgi"
        data = {
            "apiVersion": "1.0",
            "method": "getClientStatus"
        }
        return self.device.post(path, json_data=data).json()

    def configure_event_publication(self, filters):
        """
        Configures event publication to the MQTT broker.
        :param filters: List of event filters.
        """
        path = "/axis-cgi/mqtt/event.cgi"
        data = {
            "apiVersion": "1.0",
            "method": "configureEventPublication",
            "params": {
                "eventFilterList": filters
            }
        }
        return self.device.post(path, json_data=data).json()
