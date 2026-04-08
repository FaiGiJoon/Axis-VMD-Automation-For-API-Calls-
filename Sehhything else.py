from axis_base import AxisDevice

class ParamManager:
    def __init__(self, device):
        self.device = device

    def update_param(self, group_path, value):
        path = "/axis-cgi/param.cgi"
        params = {"action": "update", group_path: value}
        return self.device.get(path, params=params).text

# --- Categorized Calls ---
# Regional Settings: cam_params.update_param("RegionalSettings.Language", "en-US")
# Signed Video:      cam_params.update_param("Image.I0.MPEG.SignedVideo.Enabled", "yes")
# Rate Control:      cam_params.update_param("Image.I0.RateControl.MaxBitrate", "5000")
# Serial Port:       cam_params.update_param("Serial.Ser0.BaudRate", "9600")