from axis_base import AxisDevice

def set_zipstream_strength(device, strength="medium"):
    # values: off, low, medium, high, extreme
    path = "/axis-cgi/zipstream/setstrength.cgi"
    params = {"strength": strength}
    return device.get(path, params=params).text