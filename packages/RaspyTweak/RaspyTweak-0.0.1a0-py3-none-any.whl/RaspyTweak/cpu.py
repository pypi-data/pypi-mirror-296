#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# RaspyTweak
#
# Author: Voyager
# Date: 09/15/2024

import subprocess
import psutil

def cpu_usage() -> float:
    """Returns the current CPU usage as a percentage."""
    return psutil.cpu_percent(interval=1)

def cpu_frequency() -> float | None:
    """Returns the current CPU frequency in MHz."""
    freq = psutil.cpu_freq()
    if freq:
        return freq.current
    return None

def cpu_count(logical: bool = True) -> int:
    """
    Returns the number of CPU cores.
    :param logical: If True, return logical cores, otherwise physical cores.
    """
    return psutil.cpu_count(logical=logical)

def cpu_temperature() -> float | None:
    """Returns the CPU temperature on a Raspberry Pi."""
    try:
        result = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True)
        temp_str = result.stdout
        # Extract the temperature value from the output (e.g., 'temp=45.8'C\n')
        temp = float(temp_str.split('=')[1].split("'")[0])
        return temp
    except Exception as e:
        print(f"Error fetching CPU temperature: {e}")
        return None
