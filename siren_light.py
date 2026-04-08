from axis_base import AxisDevice

def control_siren(device, action="start"):
    path = "/axis-cgi/siren_and_light.cgi"
    params = {"action": action, "siren": "on" if action == "start" else "off"}
    return device.get(path, params=params).text