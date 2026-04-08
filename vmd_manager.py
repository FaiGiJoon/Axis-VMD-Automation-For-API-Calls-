import time
import json
import argparse
from datetime import datetime
from vmd_manager import VMDManager # Assume the class from before is in vmd_manager.py

def one_time_setup(vmd, profile_name, include_area):
    """Configures a camera once and exits."""
    print(f"[*] Starting one-time setup for {profile_name}...")
    config = vmd.get_config()
    if config:
        # Example: Update the first profile
        config['profiles'][0]['name'] = profile_name
        config['profiles'][0]['triggers'][0]['data'] = include_area
        
        if vmd.set_config(config):
            print(f"[+] Success: {profile_name} configured.")

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
            for profile in config['profiles']:
                for filter_obj in profile['filters']:
                    if filter_obj['type'] == "timeShortLivedLimit":
                        new_val = 4 if (now >= 22 or now <= 6) else 1
                        if filter_obj['data'] != new_val:
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
    vmd = VMDManager(args.ip, args.user, args.password)

    if args.mode == 'setup':
        # Example area coordinates
        area = [[-1.0, -1.0], [1.0, -1.0], [1.0, 1.0], [-1.0, 1.0]]
        one_time_setup(vmd, "Standard_Security", area)
    elif args.mode == 'service':
        background_service(vmd)