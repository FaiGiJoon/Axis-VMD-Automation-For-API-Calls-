from axis_base import AxisDevice

def get_view_areas(device):
    path = "/axis-cgi/viewarea/info.cgi"
    return device.get(path, params={"schemaversion": "1"}).text