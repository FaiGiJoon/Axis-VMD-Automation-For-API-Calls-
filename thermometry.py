from axis_base import AxisDevice

def get_temperature_data(device):
    """Gets the current temperature readings from all configured measurement areas."""
    path = "/axis-cgi/thermometry/data.cgi"
    data = {
        "apiVersion": "1.0",
        "method": "getData"
    }
    return device.post(path, json_data=data).json()

def get_thermometry_config(device):
    """Retrieves the configuration of temperature measurement zones."""
    path = "/axis-cgi/thermometry/config.cgi"
    data = {
        "apiVersion": "1.0",
        "method": "getConfiguration"
    }
    return device.post(path, json_data=data).json()