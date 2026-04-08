from axis_base import AxisDevice

def get_streaming_indicator_status(device):
    """Checks if the video streaming indicator (Privacy LED/Overlay) is active."""
    path = "/axis-cgi/videostreamingindicator.cgi"
    data = {
        "apiVersion": "1.0",
        "method": "getStatus"
    }
    return device.post(path, json_data=data).json()

def configure_streaming_indicator(device, enable=True):
    """Turns the privacy streaming indicator on or off."""
    path = "/axis-cgi/videostreamingindicator.cgi"
    data = {
        "apiVersion": "1.0",
        "method": "setConfiguration",
        "params": {
            "enabled": enable
        }
    }
    return device.post(path, json_data=data).json()