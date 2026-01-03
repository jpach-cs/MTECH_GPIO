"""
MTECH_GPIO
==========

A minimal educational GPIO wrapper for Raspberry Pi,
built on top of lgpio.

Designed for teaching Embedded Systems at Montana Tech.

MIT License

Copyright (c) 2026
Jakub Leszek Pach, Montana Technological University

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...
"""

import lgpio
import time
import threading

# -------------------------------
# Constants (RPi.GPIO compatible)
# -------------------------------

BCM   = "BCM"
BOARD = "BOARD"

IN = 0
OUT = 1

LOW = 0
HIGH = 1

PUD_OFF = 0
PUD_DOWN = 1
PUD_UP = 2


# ==========================
# Internal state (GLOBAL)
# ==========================


_mode = BCM
_chip = 0
_device = lgpio.gpiochip_open(_chip)
_claimed_pins = set()

# BOARD → BCM mapping (40-pin header)
_BOARD_TO_BCM = {
    11: 17,
    12: 18,
    13: 27,
    15: 22,
    16: 23,
    18: 24,
    22: 25,
    7: 4,
    29: 5,
    31: 6,
    32: 12,
    33: 13,
    35: 19,
    36: 16,
    37: 26,
    38: 20,
    40: 21
}

# ==========================
# Internal helpers
# ==========================

def _map_pin(pin):
    if _mode == BCM:
        return pin
    if pin not in _BOARD_TO_BCM:
        raise ValueError("Invalid BOARD pin")
    return _BOARD_TO_BCM[pin]

# ==========================
# Public API (procedural)
# ==========================

def setmode(mode):
    global _mode
    if mode not in (BCM, BOARD):
        raise ValueError("Invalid mode")
    _mode = mode

def setup(pin, direction, pull_up_down=PUD_OFF):
    bcm = _map_pin(pin)

    if direction == OUT:
        lgpio.gpio_claim_output(_device, bcm)

    elif direction == IN:
        if pull_up_down == PUD_OFF:
            pud = lgpio.SET_PULL_NONE
        elif pull_up_down == PUD_DOWN:
            pud = lgpio.SET_PULL_DOWN
        elif pull_up_down == PUD_UP:
            pud = lgpio.SET_PULL_UP
        else:
            raise ValueError("Invalid pull_up_down value")

        lgpio.gpio_claim_input(_device, bcm, pud)

    else:
        raise ValueError("Invalid direction")

    _claimed_pins.add(bcm)


def output(pin, value):
    bcm = _map_pin(pin)
    lgpio.gpio_write(_device, bcm, value)

def input(pin):
    bcm = _map_pin(pin)
    return lgpio.gpio_read(_device, bcm)

def get_device():
    """Advanced use only"""
    return _device

def cleanup():
    for bcm in _claimed_pins:
        lgpio.gpio_free(_device, bcm)
    _claimed_pins.clear()
    lgpio.gpiochip_close(_device)

# ==========================
# PWM 
# ==========================

_pwm_threads = {}  # pin -> thread info

def pwm_start(pin, frequency, duty_cycle):
    """Start PWM on pin"""
    import threading

    bcm = _map_pin(pin)

    # if exist - stop
    pwm_stop(pin)

    running = True
    thread_info = {"thread": None, "running": running, "freq": frequency, "duty": duty_cycle}
    _pwm_threads[bcm] = thread_info

    def _run():
        while thread_info["running"]:
            period = 1.0 / thread_info["freq"]
            on = period * (thread_info["duty"] / 100.0)
            off = period - on
            output(pin, HIGH)
            time.sleep(on)
            output(pin, LOW)
            time.sleep(off)

    t = threading.Thread(target=_run, daemon=True)
    thread_info["thread"] = t
    t.start()

def pwm_change_duty(pin, duty_cycle):
    bcm = _map_pin(pin)
    if bcm in _pwm_threads:
        _pwm_threads[bcm]["duty"] = duty_cycle
    else:
        raise RuntimeError("PWM not started on this pin")

def pwm_change_frequency(pin, frequency):
    bcm = _map_pin(pin)
    if bcm in _pwm_threads:
        _pwm_threads[bcm]["freq"] = frequency
    else:
        raise RuntimeError("PWM not started on this pin")

def pwm_stop(pin):
    bcm = _map_pin(pin)
    if bcm in _pwm_threads:
        _pwm_threads[bcm]["running"] = False
        thread = _pwm_threads[bcm]["thread"]
        if thread:
            thread.join()
        output(pin, LOW)
        del _pwm_threads[bcm]

