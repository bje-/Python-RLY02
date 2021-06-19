"""Control an RLY02 USB relay"""

import argparse
import time
import sys
from struct import unpack
import serial

SERIAL_PATH = '/dev/ttyACM0'
BAUD_RATE = 9600

RELAY_1_ON = 0x65
RELAY_1_OFF = 0x6F
RELAY_2_ON = 0x66
RELAY_2_OFF = 0x70
INFO = 0x5A
RELAY_STATES = 0x5B


def send_command(cmd, read_response=False):
    """Send a command down the USB line"""
    ser = serial.Serial(SERIAL_PATH, BAUD_RATE)
    ser.write(chr(cmd) + '\n')
    response = ser.read() if read_response else None
    ser.close()
    return response


def click_relay(relaynum):
    """Click relay"""
    assert relaynum in [1, 2], "argument must be 1 or 2"
    send_command(RELAY_1_ON if relaynum == 1 else RELAY_2_ON)
    time.sleep(1)
    send_command(RELAY_1_OFF if relaynum == 1 else RELAY_2_OFF)


def get_relay_states():
    """Get the state of the two relays"""
    states = send_command(RELAY_STATES, read_response=True)
    response = unpack('b', states)[0]
    states = {
        0: {'1': False, '2': False},
        1: {'1': True, '2': False},
        2: {'1': False, '2': True},
        3: {'1': True, '2': True},
    }
    return states[response]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", type=int, choices=[1, 2], help='relay number')
    parser.add_argument("-a", type=str, choices=['on', 'off', 'click'],
                        help='action')
    parser.add_argument("-s", action="store_true", help='get relay states')
    args = parser.parse_args()

    if args.s:
        print(get_relay_states())
    elif (args.r is None) ^ (args.a is None):
        parser.error('-r and -a must be given together')
    elif (args.r is not None) and (args.a is not None):
        actions = {
            '1_on': lambda: send_command(RELAY_1_ON),
            '1_off': lambda: send_command(RELAY_1_OFF),
            '1_click': lambda: click_relay(1),
            '2_on': lambda: send_command(RELAY_2_ON),
            '2_off': lambda: send_command(RELAY_2_OFF),
            '2_click': lambda: click_relay(2),
        }
        actions['%s_%s' % (args.r, args.a)]()
    else:
        parser.print_help()
        sys.exit(1)
    sys.exit()
