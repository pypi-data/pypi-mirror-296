#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# RaspyTweak
#
# Author: Voyager
# Date: 09/15/2024

__all__ = ['gpio', 'errors', 'constants', 'cpu', 'system', 'memory', 'disk', 'network']

__package_name__ = 'RaspyTweak'
__author__ = 'Voyager'
__version__ = '0.0.0.1a1'
__version_prefix__ = 'pre-alpha'
__doc__  = 'A library for raspberry pi'

from .errors import *
from .constants import *
from .gpio import *
from .system import *
from .cpu import *
from .memory import *
from .disk import *
from .network import *


def system_info() -> dict[str, int | None]:
    """Returns a dictionary containing various system information."""
    return {
        'cpu_usage': cpu_usage(),
        'cpu_frequency_mhz': cpu_frequency(),
        'cpu_core_count': cpu_count(logical=False),
        'logical_cpu_count': cpu_count(logical=True),
        'cpu_temperature_celsius': cpu_temperature(),
        'memory': memory_info(),
        'disk_usage': disk_usage()
    }
