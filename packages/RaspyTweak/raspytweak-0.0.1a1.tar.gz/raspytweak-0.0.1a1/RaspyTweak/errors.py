#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# RaspyTweak
#
# Author: Voyager
# Date: 09/15/2024

# RasberryPi Exceptions
class RaspberryPiError(Exception):
    """Raised when an error occurs in the Raspberry Pi library."""

class RaspberryPiWarning(Warning):
    """Raised when a warning occurs in the Raspberry Pi library."""

class RaspberryPiInvalid(RaspberryPiWarning):
    """Raised when an unsupported Raspberry Pi is used."""

# Module exceptions
class BaseError(Exception):
    """Raised when an error occurs in the module."""

class BaseWarning(Warning):
    """Raised when a warning occurs."""

class Note(Warning):
    """Raised when an notice is displayed."""

# OS Exceptions
class OSException(Exception):
    """Raised when an error occurs in the OS module."""

class OSWarning(Warning):
    """Raised when an warning occurs."""

class OSInvalid:
    """Raised when an unsupported OS is used."""
    __code__: int = 0x0081
    
    def __init__(self, *args) -> None:
        self.args = args

        print(f'{self.args[0]}')
        exit(self.__code__)

# GPIO Exceptions
class GPIOError(RaspberryPiError):
    """Raised when an error occurs in the GPIO module."""

class InvalidPin(GPIOError):
    """Raised when an invalid pin number is used."""

# Exceptions
class Timeout(RaspberryPiError):
    """Raised when a timeout occurs."""

class ValueOutOfRange(RaspberryPiError):
    """Raised when a value is out of range."""

class ReadOnly(RaspberryPiError):
    """Raised when a read-only only attribute is modified."""

class WriteOnly(RaspberryPiError):
    """Raised when a write-only attribute is accessed."""

class NotInitialized(RaspberryPiError):
    """Raised when a module is not initialized."""

class NotSupported(RaspberryPiError):
    """Raised when a feature is not supported."""

class UncatchedException(Exception):
    """Raised when an uncaught exception occurs."""

class NotImplemented():
    """Raised when an feature is not implemented."""

def suppress_traceback(func):
    """A decorator to suppress traceback for the given function."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Ignored exception: {e}")
    return wrapper

def error(s: str):
    print(f"error: {s}")

def info(s: str):
    print(f"info: {s}")