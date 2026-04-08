from axis_base import AxisDevice

def list_recording_groups(device):
    path = "/axis-cgi/record/recording_group/list.cgi"
    return device.get(path, params={"schemaversion": "1"}).text