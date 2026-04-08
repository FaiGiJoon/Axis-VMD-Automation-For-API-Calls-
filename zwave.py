from axis_base import AxisDevice

def list_zwave_nodes(device):
    path = "/axis-cgi/zwave/node.cgi"
    params = {"action": "list"}
    return device.get(path, params=params).text