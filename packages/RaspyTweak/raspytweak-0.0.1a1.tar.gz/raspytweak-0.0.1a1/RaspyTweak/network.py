#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# RaspyTweak
#
# Author: Voyager
# Date: 09/15/2024

import psutil
import socket

def network_io() -> dict[str, int]:
    """Returns a dictionary with bytes sent and received on each network interface."""
    net_io = psutil.net_io_counters(pernic=True)
    network_data = {}
    for interface, stats in net_io.items():
        network_data[interface] = {
            'bytes_sent': stats.bytes_sent,
            'bytes_received': stats.bytes_recv,
            'packets_sent': stats.packets_sent,
            'packets_received': stats.packets_recv
        }
    return network_data

def network_interfaces() -> dict[str, str]:
    """Returns a dictionary with network interface addresses (IP, MAC, etc.)."""
    net_if_addrs = psutil.net_if_addrs()
    interfaces = {}
    for interface, addresses in net_if_addrs.items():
        interfaces[interface] = {}
        for addr in addresses:
            if addr.family == socket.AF_INET:  # IPv4
                interfaces[interface]['IPv4'] = addr.address
            elif addr.family == socket.AF_INET6:  # IPv6
                interfaces[interface]['IPv6'] = addr.address
            elif addr.family == psutil.AF_LINK:  # MAC address
                interfaces[interface]['MAC'] = addr.address
    return interfaces

def network_stats() -> dict[str, int | bool]:
    """Returns statistics about each network interface."""
    net_stats = psutil.net_if_stats()
    stats = {}
    for interface, stat in net_stats.items():
        stats[interface] = {
            'is_up': stat.isup,
            'speed_mbps': stat.speed,
            'duplex': stat.duplex,
            'mtu': stat.mtu
        }
    return stats

def full_network_info() -> dict[str, dict[str, int | str | bool]]:
    """Returns comprehensive network information including I/O, interfaces, and stats."""
    return {
        'network_io': network_io(),
        'network_interfaces': network_interfaces(),
        'network_stats': network_stats()
    }
