"""Control a 3-channel RPi Relay Board."""

import argparse
import sys
from RPi import GPIO

# Relay channel definitions
channels = {1: 26, 2: 20, 3: 21}

# Initialise GPIO
GPIO.setmode(GPIO.BCM)
for ch in [1, 2, 3]:
    GPIO.setup(channels[ch], GPIO.OUT)

parser = argparse.ArgumentParser()
parser.add_argument("-r", type=int, choices=[1, 2, 3], help='relay number', required=True)
parser.add_argument("-a", type=str, choices=['on', 'off'], help='action', required=True)
args = parser.parse_args()

# Relays are active-low
GPIO.output(channels[args.r], args.a == 'on')
GPIO.cleanup()

sys.exit()
