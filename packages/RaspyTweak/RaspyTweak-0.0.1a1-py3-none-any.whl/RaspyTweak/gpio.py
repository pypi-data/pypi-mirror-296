#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# RaspyTweak
#
# Author: Voyager
# Date: 09/15/2024

import sys

from .constants import *

from deprecated import deprecated
from time import sleep, time
import threading

class GPIOPin:
    """GPIOPin class for raspberry pi"""
    def __init__(self, num, mode):
        if 0 <= num <= 40:
            self.num = num
        else:
            print('\033[31mInvalid pin number -> Enter a number from 0 to 40\033[0m')
            return
        if mode == OUT or mode == WRITE:
            self.mode = OUT
        elif mode == IN or mode == READ:
            self.mode = IN
        else:
            print('\033[31mInvalid pin mode -> Enter OUT or WRITE for output, or IN or READ for input\033[0m')
            return

        if self.num and self.mode:
            try:
                with open('/sys/class/gpio/export', 'w') as f:
                    f.write(str(self.num) + '\n')
                sleep(0.05)
                with open(f'/sys/class/gpio/gpio{str(self.num)}/direction', 'w') as f:
                    f.write(str(self.mode) + '\n')
            except Exception as e:
                print(f"\033[31mRan into a uncatched exception:\033[0m {e}")

    def __del__(self):
        try:
            self.reset()
            with open(f'/sys/class/gpio/unexport', 'w') as f:
                f.write(str(self.num) + '\n')
        except Exception as e:
            print(f"\033[31mRan into a uncatched exception:\033[0m {e}")

    @deprecated(reason="\033[31mUse __del__ instead, by using the del keyword.\033[0m", version="0.0.0.0a2", action="once")
    def unexport(self):
        try:
            self.reset()
            with open(f'/sys/class/gpio/unexport', 'w') as f:
                f.write(str(self.num) + '\n')
        except Exception as e:
            print(f"\033[31mRan into a uncatched exception:\033[0m {e}")

    def reset(self):
        """
        Reset the GPIO pin to its default state.

        This function resets the GPIO pin to its default state by setting its value to LOW and direction to input.
        It uses the os.system() function to execute shell commands to achieve this.

        :return: None
        :raises Exception: If any uncaught exception occurs during the operation.
        """

        try:
            with open(f'/sys/class/gpio/gpio{str(self.num)}/value', 'w') as f:
                f.write('0' + '\n')
            sleep(0.05)
            with open(f'/sys/class/gpio/gpio{str(self.num)}/direction', 'w') as f:
                f.write('in' + '\n')
        except Exception as e:
            print(f"\033[31mRan into a uncatched exception:\033[0m {e}")

    def write(self, value):
        """
        Write a value to the GPIO pin.

        This function writes a value (0 or 1) to the GPIO pin. If the provided value is not 0 or 1,
        it prints an error message and does not write anything to the pin.

        :param value: The value to write to the GPIO pin. It can be either 0 or 1, or the constants LOW (0) or HIGH (1).
        :type value: int

        :raises Exception: If any uncaught exception occurs during the operation.
        """

        try:
            if value == 0 or value == LOW:
                with open(f'sys/class/gpio/gpio{str(self.num)}/value', 'w') as f:
                    f.write('0' + '\n')
            elif value == 1 or value == HIGH:
                with open(f'sys/class/gpio/gpio{str(self.num)}/value', 'w') as f:
                    f.write('1' + '\n')
            else:
                print('\033[31mInvalid value -> Enter 1 or HIGH for HIGH, 0 or LOW for LOW\033[0m')
        except Exception as e:
            print(f"\033[31mRan into a uncatched exception:\033[0m {e}")

    def read(self):
        """
        Read the current value of the GPIO pin.

        The function reads the value from the GPIO pin's value file and returns it as an integer.
        If the GPIO pin is not in input mode, it prints an error message and returns None.

        :return: The current value of the GPIO pin (0 or 1) if the pin is in input mode, otherwise None.
        :rtype: int or None
        """

        if self.mode == IN or self.mode == READ:
            try:
                with open(f'/sys/class/gpio/gpio{str(self.num)}/value', 'r') as file:
                    value = file.read().strip()
                return int(value)
            except (FileNotFoundError, OSError) as e:
                return None
            except Exception as e:
                print(f"\033[31mRan into a uncatched exception:\033[0m {e}")
                return None
        else:
            print('\033[31mCannot read -> GPIO pin is not in input mode\033[0m')
            return None

    def set_mode(self, mode):
        """
        Set the GPIO pin mode to either input or output.

        :param mode: The mode to set the GPIO pin to. It can be either 'OUT' or 'WRITE' for output, or 'IN' or 'READ' for input.
        :return: None
        :raises OSError: If the operation fails to set the mode due to an error.
        :raises Exception: If any other uncaught exception occurs during the operation.
        """

        try: 
            self.mode = mode
            with open(f'/sys/class/gpio/gpio{str(self.num)}/direction', 'w') as f:
                    f.write(str(self.mode) + '\n')
        except Exception as e:
            print(f"\033[31mRan into a uncatched exception:\033[0m {e}")

    def pwm(self, duty_cycle: int, frequency: float, duration: float):
        """
        Generates a software PWM signal.

        :param duty_cycle: The percentage of time the signal stays HIGH (0-100).
        :param frequency: The PWM signal frequency in Hz (cycles per second).
        :param duration: How long to run the PWM signal in seconds.
        """
        if not (0 <= duty_cycle <= 100):
            print("\033[31mInvalid duty cycle -> Enter a value between 0 and 100\033[0m")
            return

        period = 1 / frequency
        high_time = period * (duty_cycle / 100)
        low_time = period * (1 - duty_cycle / 100)
        end_time = time() + duration
        while time() < end_time:
            self.write(HIGH)
            sleep(high_time)

            self.write(LOW)
            sleep(low_time)

    def run_pwm(self, duty_cycle: int, frequency: float, duration: float) -> threading.Thread:
        """Run PWM in a separate thread."""
        thread = threading.Thread(target=self.pwm, args=(duty_cycle, frequency, duration))
        thread.start()
        return thread
