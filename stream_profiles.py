from axis_base import AxisDevice

def list_profiles(device):
    path = "/axis-cgi/streamprofile.cgi"
    data = {"apiVersion": "1.0", "method": "list", "params": {"streamProfileName": []}}
    return device.post(path, json_data=data).json()