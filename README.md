# Axis VAPIX API Automation Framework

A comprehensive, modular collection of Python scripts designed to automate, manage, and dynamically monitor Axis Communications network devices. This framework leverages the VAPIX® API to enable programmatic control and intelligent surveillance environments.

## Overview

This repository provides a specialized toolkit for security engineers and system integrators. Each script is decoupled, allowing for the automation of specific camera features—from Video Motion Detection (VMD) and PTZ Autotracking to I/O Port Management and System Diagnostics.

## Project Structure

The framework is built on a modular architecture to ensure consistency and security across all API calls.

* **axis_base.py**: The core engine handling Digest Authentication, connection persistence, and HTTP transport.
* **Individual Scripts**: Specialized modules for specific API endpoints, including:
    * **vmd_manager.py**: Motion detection and filter optimization.
    * **ptz_autotracker.py**: Intelligent tracking control.
    * **io_ports.py**: Physical relay and supervised I/O automation.
    * **zipstream.py**: Dynamic bitrate and storage optimization.
    * [30+ other specialized scripts for various Axis services].

## API Coverage

| Category | Supported APIs |
| :--- | :--- |
| **Detection** | VMD 4, Shock Detection, Thermal/Thermometry, Autotracker |
| **Control** | PTZ, Siren/Light, Z-Wave, I/O Ports, Video Output |
| **System** | RAID, SSH, Remote Syslog, Time/NTP, Systemready |
| **Streaming** | Zipstream, Stream Profiles, RTSP, Signed Video, QuadView |

## Installation and Setup

### 1. Prerequisites
* Python 3.8+
* Requests library

```bash
pip install requests

2. Configure Credentials
Every script in this repository utilizes the AxisDevice class. You will need to provide your camera's details within your implementation:

Python
from axis_base import AxisDevice

# Initialize your device
cam = AxisDevice(ip="192.168.1.100", user="admin", password="your_password")
Usage Examples
Triggering a Siren and Light
Bash
python siren_light.py --action start
Dynamic Zipstream Adjustment
Python
from zipstream import set_zipstream_strength

# Increase compression during low-activity hours
set_zipstream_strength(cam, strength="extreme")
Core Features
Scalability: Configure multiple cameras simultaneously using standard JSON profiles.

Error Resilience: Built-in handling for Axis-specific error codes (1000-2999).

Lower False Positives: Capability to adjust sensitivity based on environmental metadata or time of day.

VMS-Agnostic: Compatible with Milestone, Genetec, or Axis Camera Station.

License
This project is licensed under the MIT License. You are free to use, modify, and distribute it in both personal and commercial environments. See the LICENSE file for details.
