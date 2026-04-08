from axis_base import AxisDevice

def get_raid_status(device):
    path = "/axis-cgi/raidmanagement.cgi"
    data = {"apiVersion": "1.0", "method": "getStatus"}
    return device.post(path, json_data=data).json()