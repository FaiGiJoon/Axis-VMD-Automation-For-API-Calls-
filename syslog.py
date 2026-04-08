from axis_base import AxisDevice

def configure_syslog(device, server_ip):
    path = "/axis-cgi/remotesyslog.cgi"
    data = {
        "apiVersion": "1.0",
        "method": "setup",
        "params": {
            "Server1": {"Address": server_ip, "Port": 514, "Protocol": "UDP", "Enabled": True}
        }
    }
    return device.post(path, json_data=data).json()