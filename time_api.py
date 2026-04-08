from axis_base import AxisDevice

def get_device_time(device):
    path = "/axis-cgi/datetime.cgi"
    params = {"action": "get"}
    return device.get(path, params=params).text