from axis_base import AxisDevice

class StorageManager:
    def __init__(self, device: AxisDevice):
        self.device = device

    def get_storage_status(self):
        """Retrieves information about all storage devices."""
        path = "/axis-cgi/storage/status.cgi"
        data = {
            "apiVersion": "1.0",
            "method": "getStatus"
        }
        return self.device.post(path, json_data=data).json()

    def list_disks(self):
        """Lists available storage disks."""
        path = "/axis-cgi/storage/list.cgi"
        data = {
            "apiVersion": "1.0",
            "method": "list"
        }
        return self.device.post(path, json_data=data).json()
