#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# RaspyTweak
#
# Author: Voyager
# Date: 09/15/2024

import subprocess
from time import sleep as wait
from .errors import *

def shutdown():
    """Shuts down the Raspberry Pi safely."""
    try:
        info("Shutting down...")
        wait(0.5)
        subprocess.run(['sudo', 'shutdown', '-h', 'now'], check=True)
    except (subprocess.CalledProcessError, Exception) as e:
        error(f"Error occurred during shutdown: {e}")

def reboot():
    """Reboots the Raspberry Pi."""
    try:
        info("Rebooting...")
        wait(0.5)
        subprocess.run(['sudo', 'reboot'], check=True)
    except (subprocess.CalledProcessError, Exception) as e:
        print(f"Error occurred during reboot: {e}")

def sleep():
    """Puts Raspberry Pi into low-power mode by turning off HDMI."""
    try:
        info("Entering low-power mode (HDMI off)...")
        wait(0.5)
        subprocess.run(['sudo', '/opt/vc/bin/tvservice', '-o'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while entering low-power mode: {e}")

def wake():
    """Restores HDMI after low-power mode."""
    try:
        info("Waking up (HDMI on)...")
        wait(0.5)
        subprocess.run(['sudo', '/opt/vc/bin/tvservice', '-p'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while waking up: {e}")

def convert_bytes(size_in_bytes: int):
    """Converts bytes to a more human-readable format (KB, MB, GB, etc.)."""
    if size_in_bytes == 0:
        return "0B"
    
    # Define the size units
    size_units = ["B", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    size = size_in_bytes

    # Divide by 1024 to move to the next unit
    while size >= 1024 and i < len(size_units) - 1:
        size /= 1024.0
        i += 1
    
    # Return formatted string with two decimal places
    return f"{size:.2f} {size_units[i]}"

def battery_info():
    """Returns battery charge information (if available)."""
    try:
        with open('/sys/class/power_supply/BAT0/capacity', 'r') as f:
            return f.read().strip() + '%'
    except FileNotFoundError:
        return "Battery information not available."
