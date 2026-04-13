import time
import json
import argparse
from datetime import datetime
from axis_base import AxisDevice

class VMDManager:
    def __init__(self, device: AxisDevice):
        self.device = device

    def get_config(self):
        """Retrieves the current VMD4 configuration."""
        path = "/axis-cgi/vmd/config.cgi"
        response = self.device.get(path)
        if response.status_code == 200:
            return response.json()
        return None

    def set_config(self, config):
        """Updates the VMD4 configuration."""
        path = "/axis-cgi/vmd/config.cgi"
        response = self.device.post(path, json_data=config)
        return response.status_code == 200

def one_time_setup(vmd, profile_name, include_area):
    """Configures a camera once and exits."""
    print(f"[*] Starting one-time setup for {profile_name}...")
    config = vmd.get_config()
    if config:
        # Example: Update the first profile
        if 'profiles' in config and len(config['profiles']) > 0:
            config['profiles'][0]['name'] = profile_name
            # Ensure triggers exists before assigning
            if 'triggers' in config['profiles'][0] and len(config['profiles'][0]['triggers']) > 0:
                config['profiles'][0]['triggers'][0]['data'] = include_area

            if vmd.set_config(config):
                print(f"[+] Success: {profile_name} configured.")
        else:
            print("[-] No profiles found in configuration.")

def background_service(vmd, interval=60):
    """
    Monitors the camera. Example: Changes sensitivity based on time of day.
    """
    print(f"[*] Background service started. Polling every {interval}s...")
    
    while True:
        now = datetime.now().hour
        config = vmd.get_config()
        
        if config:
            # DYNAMIC LOGIC: 
            # If it's night (22:00 - 06:00), increase 'short-lived limit' 
            # to prevent bugs/noise from triggering alarms.
            is_modified = False
            for profile in config.get('profiles', []):
                for filter_obj in profile.get('filters', []):
                    if filter_obj.get('type') == "timeShortLivedLimit":
                        new_val = 4 if (now >= 22 or now <= 6) else 1
                        if filter_obj.get('data') != new_val:
                            filter_obj['data'] = new_val
                            is_modified = True
            
            if is_modified:
                vmd.set_config(config)
                print(f"[!] {datetime.now()}: Applied night-time sensitivity filters.")
        
        time.sleep(interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VMD Automation Tool")
    parser.add_argument("--mode", choices=['setup', 'service'], required=True)
    parser.add_argument("--ip", required=True)
    parser.add_argument("--user", default="admin")
    parser.add_argument("--password", required=True)
    
    args = parser.parse_args()
    cam = AxisDevice(args.ip, args.user, args.password)
    vmd = VMDManager(cam)

    if args.mode == 'setup':
        # Example area coordinates
        area = [[-1.0, -1.0], [1.0, -1.0], [1.0, 1.0], [-1.0, 1.0]]
        one_time_setup(vmd, "Standard_Security", area)
    elif args.mode == 'service':
        background_service(vmd)
