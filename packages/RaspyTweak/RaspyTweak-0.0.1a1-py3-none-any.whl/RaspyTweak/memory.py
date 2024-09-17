#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# RaspyTweak
#
# Author: Voyager
# Date: 09/15/2024

import psutil

def memory_info() -> dict[str, int]:
    """Returns a dictionary with total, available, and used memory."""
    mem = psutil.virtual_memory()
    return {
        'total': mem.total,
        'available': mem.available,
        'used': mem.used,
        'free': mem.free
    }
