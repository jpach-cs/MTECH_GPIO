# MTECH_GPIO

A minimal educational GPIO wrapper for Raspberry Pi 3-5, designed for teaching Embedded Systems at Montana Tech.

---

## Overview

At Montana Tech, introductory Embedded Systems courses (135 and 136) are conducted on Raspberry Pi 4.  
While there are several GPIO libraries available for Python – such as `RPi.GPIO`, `pigpio`, and `PiZero` – `RPi.GPIO` is often the simplest starting point for beginners because it focuses on **basic digital electronics concepts** without requiring advanced programming techniques.

However, `RPi.GPIO` is no longer officially supported by the Raspberry Pi Foundation, and its compatibility with newer Raspberry Pi models is limited.  
`lgpio` is now considered one of the most reliable and modern GPIO libraries (it is also used under the hood by `gpiozero`).  

To ease the learning curve for students who have only completed introductory courses (135 and 136), I developed **MTECH_GPIO**, a lightweight wrapper around `lgpio`.  

---

## Key Features

- **RPi.GPIO-compatible procedural API**  
  Students familiar with `RPi.GPIO` can transition seamlessly.
  
- **Unified PWM interface**  
  PWM is implemented **procedurally**, not object-oriented, to match the style of `RPi.GPIO` and simplify usage for beginners.
  
- **Simplified pin modes**  
  Supports BCM and BOARD numbering modes.
  
- **Input/Output control with built-in pull-up/pull-down support**  
  Students can quickly configure pins without worrying about low-level `lgpio` calls.
  
- **Designed for education**  
  Focused on teaching **digital electronics and GPIO concepts**, not on advanced software engineering.

---

## Installation

```bash
# Clone this repository
git clone https://github.com/jpach-cs/MTECH_GPIO

# Navigate into the repository
cd MTECH_GPIO

# Install repository
sudo python3 -m pip install .

# Use the library in Python
python3
>>> import MTECH_GPIO as gpio
```

## Example Usage
```python
import MTECH_GPIO as gpio
import time

gpio.setmode(gpio.BCM)

# Setup pin 17 as output
gpio.setup(17, gpio.OUT)

# Simple blinking
for _ in range(5):
    gpio.output(17, gpio.HIGH)
    time.sleep(0.5)
    gpio.output(17, gpio.LOW)
    time.sleep(0.5)

# PWM example
gpio.pwm_start(17, frequency=1000, duty_cycle=50)
time.sleep(2)
gpio.pwm_change_duty(17, 75)
time.sleep(2)
gpio.pwm_change_frequency(17, 500)
time.sleep(2)
gpio.pwm_stop(17)

# Cleanup all pins
gpio.cleanup()
```

## License

MIT License © 2026 Jakub Leszek Pach, Montana Technological University

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

The software is provided "as is", without warranty of any kind. The author is not responsible for any damage or malfunction resulting from its use.