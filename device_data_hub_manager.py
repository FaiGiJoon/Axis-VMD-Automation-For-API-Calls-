from axis_base import AxisDevice

class DeviceDataHubManager:
    """
    Manager for Axis Device Data Hub API (ACAP 12.11+).
    Provides publish/subscribe inter-application communication management.
    """
    def __init__(self, device: AxisDevice):
        self.device = device

    def get_status(self):
        """Retrieves status of the Device Data Hub service."""
        path = "/axis-cgi/devicedatahub.cgi"
        payload = {
            "apiVersion": "1.0",
            "method": "getStatus"
        }
        response = self.device.post(path, json_data=payload)
        return response.json()

    def get_topics(self):
        """Retrieves active publish/subscribe topics in Device Data Hub."""
        path = "/axis-cgi/devicedatahub.cgi"
        payload = {
            "apiVersion": "1.0",
            "method": "getTopics"
        }
        response = self.device.post(path, json_data=payload)
        return response.json()

    def publish_event(self, topic: str, payload_data: dict):
        """
        Publishes an event/payload to a Device Data Hub topic.
        :param topic: Topic identifier (e.g. 'com.axis.device_data_hub.events')
        :param payload_data: Event payload data
        """
        path = "/axis-cgi/devicedatahub.cgi"
        payload = {
            "apiVersion": "1.0",
            "method": "publish",
            "params": {
                "topic": topic,
                "data": payload_data
            }
        }
        response = self.device.post(path, json_data=payload)
        return response.json()
