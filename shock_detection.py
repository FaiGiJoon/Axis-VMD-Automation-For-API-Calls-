from axis_base import AxisDevice

def set_shock_sensitivity(device, level=50):
    path = "/axis-cgi/shockdetection/setsensitivitylevel.cgi"
    params = {"schemaversion": "1", "level": level}
    return device.get(path, params=params).text