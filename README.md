Axis VAPIX API Automation FrameworkA comprehensive, modular collection of Python scripts designed to automate, manage, and dynamically monitor Axis Communications network devices.
This framework leverages the VAPIX® API to enable programmatic control and intelligent surveillance environments.OverviewThis repository provides a specialized toolkit for security engineers and system integrators.
Each script is decoupled, allowing for the automation of specific camera features—from Video Motion Detection (VMD) and PTZ Autotracking to I/O Port Management and System Diagnostics.
Project StructureThe framework is built on a modular architecture to ensure consistency and security across all API calls.axis_base.py: The core engine handling Digest Authentication, connection persistence, and HTTP transport.
Individual Scripts: Specialized modules for specific API endpoints, including:vmd_manager.py: Motion detection and filter optimization.ptz_autotracker.py: Intelligent tracking control.io_ports.py: Physical relay and 
supervised I/O automation.zipstream.py: Dynamic bitrate and storage optimization.
[30+ other specialized scripts for various Axis services].API CoverageCategorySupported APIsDetectionVMD 4, Shock Detection, Thermal/Thermometry, AutotrackerControlPTZ, Siren/Light, Z-Wave, I/O Ports, Video OutputSystemRAID, SSH, 
Remote Syslog, Time/NTP, SystemreadyStreamingZipstream, Stream Profiles, RTSP, Signed Video, QuadViewInstallation and Setup1. PrerequisitesPython 3.8+Requests libraryBashpip install requests
2. Configure CredentialsEvery script in this repository utilizes the AxisDevice class. You will need to provide your camera's details within your implementation:Pythonfrom axis_base import AxisDevice

# Initialize your device
cam = AxisDevice(ip="192.168.1.100", user="admin", password="your_password")
Usage ExamplesTriggering a Siren and LightBashpython siren_light.py --action start
Dynamic Zipstream AdjustmentPythonfrom zipstream import set_zipstream_strength

# Increase compression during low-activity hours
set_zipstream_strength(cam, strength="extreme")
Core FeaturesScalability: Configure multiple cameras simultaneously using standard JSON profiles.Error Resilience: Built-in handling for Axis-specific error codes (1000-2999).Lower False Positives: Capability to adjust sensitivity based on environmental metadata or time of day.VMS-Agnostic: Compatible with Milestone, Genetec, or Axis Camera Station.LicenseThis project is licensed under the MIT License. You are free to use, modify, and distribute it in both personal and commercial environments. See the LICENSE file for details.
