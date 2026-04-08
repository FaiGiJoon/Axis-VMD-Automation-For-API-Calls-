from axis_base import AxisDevice

def get_supervised_io_status(device):
    """Retrieves the status of supervised I/O ports (Normal, Active, Cut, or Shorted)."""
    path = "/axis-cgi/supervisedio.cgi"
    data = {
        "apiVersion": "1.0",
        "method": "getPorts"
    }
    return device.post(path, json_data=data).json()

def set_supervised_state(device, port_id, supervised=True):
    """Enables or disables supervision on a specific I/O port."""
    path = "/axis-cgi/supervisedio.cgi"
    data = {
        "apiVersion": "1.0",
        "method": "setPorts",
        "params": {
            "ports": [
                {
                    "port": port_id,
                    "supervised": supervised
                }
            ]
        }
    }
    return device.post(path, json_data=data).json()