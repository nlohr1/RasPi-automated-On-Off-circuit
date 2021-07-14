# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#!/usr/bin/python
# Simple script for shutting down the raspberry Pi at the press of a button and/or with
# the same (input-)line connected to GND per transistor, this activated by absence ("0") of
# another (external) signal as beeing a 230V-Sensor (optocoupler) or a signal from RasPi,
# activated from Octoprint as GPIO-line.

import RPi.GPIO as GPIO
import time
import os

# Use the Broadcom SOC Pin numbers "BCM",
# Setup the Pins with internal pullups enabled, PIN-23 (BCM) as input in reading mode, and
# PIN-18 as Output, to use as Signal for the On-Off-Board indicating the Pi is up and running:
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT, pull_up_down = GPIO.PUD_UP) # set BCM 18 (GPIO 1) as Output and high.
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)  # set BCM 23 (GPIO 4) as Input with internal pull-Up R's.

# Our function on *what to do* after the Shutdown-Button is pressed (=connected to GND), or
# automatically (here default), when the Optocoupler sets this line to GND - in absence of Main-Power:
def Shutdown(channel):
  GPIO.output(18, GPIO.LOW) # LOW on Pin-18 terminates the constant-charge of the Timing-Capacitor!
  os.system("sudo shutdown -h now")

# Sensing "button-pressed?":
# Add our Shutdown function to execute when the "button pressed" event (on Pin-23) happens:
GPIO.add_event_detect(23, GPIO.FALLING, callback = Shutdown, bouncetime = 2000)

# Now wait:
while 1:
  time.sleep(100)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

