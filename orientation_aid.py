from axis_base import AxisDevice

def set_north_direction(device):
    path = "/axis-cgi/ptz-orientationaid.cgi"
    data = {
        "apiVersion": "1.0",
        "method": "setNorth",
        "params": {}
    }
    return device.post(path, json_data=data).json()