from axis_base import AxisDevice
from param_manager import ParamManager

def toggle_ssh(device: AxisDevice, enable=False):
    """Enables or disables the SSH service on the camera."""
    pm = ParamManager(device)
    # Convert boolean to Axis 'yes' or 'no'
    state = "yes" if enable else "no"
    return pm.update_param("Network.SSH.Enabled", state)

# Example Usage:
# cam = AxisDevice("192.168.1.100", "admin", "password")
# print(toggle_ssh(cam, enable=False)) # Locks down SSH
