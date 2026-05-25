from axis_base import AxisDevice

def toggle_autotracker(device, enable=True):
    # Endpoint for Autotracking 2
    path = "/axis-cgi/ptz-autotracking/admin.cgi"
    params = {"action": "set", "enabled": "yes" if enable else "no"}
    return device.get(path, params=params).text

# Usage:        
# cam = AxisDevice("192.168.1.100", "root", "pass")
# print(toggle_autotracker(cam, True))