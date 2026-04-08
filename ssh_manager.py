from axis_base import AxisDevice

def toggle_ssh(device, enable=False):
    """Enables or disables the SSH service on the camera."""
    path = "/axis-cgi/param.cgi"
    # Convert boolean to Axis 'yes' or 'no'
    state = "yes" if enable else "no"
    params = {
        "action": "update",
        "Network.SSH.Enabled": state
    }
    return device.get(path, params=params).text

# Example Usage:
# cam = AxisDevice("192.168.1.100", "admin", "password")
# print(toggle_ssh(cam, enable=False)) # Locks down SSH