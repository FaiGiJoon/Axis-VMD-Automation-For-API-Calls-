from axis_base import AxisDevice

def check_system_ready(device):
    path = "/axis-cgi/systemready.cgi"
    data = {"apiVersion": "1.0", "method": "systemready"}
    return device.post(path, json_data=data).json()