# mac-address-changer
# MAC Address Changer | v2.0

![Banner](main/banner.png)

## Overview
A simple Python tool to change MAC addresses on Linux systems.  
Supports manual MAC entry or random MAC generation.

---

## Features
- Change MAC address manually.
- Generate a random MAC address.
- Works on Linux (root permission required).
- Logs all changes with timestamps.

---

## Installation
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/mac-address-changer.git

# Enter the project directory
cd mac-address-changer

# Make sure Python 3 is installed
python3 --version
# Change MAC address randomly
sudo python3 mac_changer.py -i wlan0 -r

# Change MAC address manually
sudo python3 mac_changer.py -i eth0 -m 00:11:22:33:44:55
Logging

All MAC changes are logged in mac_address_change.log with timestamp:

[04-01-2026 22:18:45] Interface: wlan0 | Old: 84:4b:4d:dd:3f:07 | New: 00:00:00:00:00:11
