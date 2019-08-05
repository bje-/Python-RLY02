"""Control an RLY02 or RLY08 USB relay"""

import argparse
import time
import sys
from struct import unpack
import serial

SERIAL_PATH = '/dev/ttyACM0'
BAUD_RATE = 9600

# Put None placeholder in index 0 for easy list access
RELAY_ON = [None] + range(0x65, 0x6d)
RELAY_OFF = [None] + range(0x6F, 0x77)
INFO = 0x5A
RELAY_STATES = 0x5B


def send_command(cmd, read_response=False):
    """Send a command down the USB line"""
    ser = serial.Serial(SERIAL_PATH, BAUD_RATE)
    ser.write(chr(cmd) + '\n')
    response = ser.read() if read_response else None
    ser.close()
    return response


def click_relay(n):
    """Click relay"""
    assert n in range(1, 9), "argument must be 1 to 8"
    send_command(RELAY_ON[n])
    time.sleep(1)
    send_command(RELAY_OFF[n])


def get_relay_states():
    """Get the state of the two relays"""
    states = send_command(RELAY_STATES, read_response=True)
    response = format(unpack('b', states)[0], '08b')
    states = dict()
    for i, bit in enumerate(response[::-1], 1):
        states[i] = bit == '1'
    return states


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", type=int, choices=range(1, 9),
                        help='relay number')
    parser.add_argument("-a", type=str, choices=['on', 'off', 'click'],
                        help='action')
    parser.add_argument("-s", action="store_true", help='get relay states')
    args = parser.parse_args()

    if args.s:
        print get_relay_states()
    elif (args.r is None) ^ (args.a is None):
        parser.error('-r and -a must be given together')
    elif (args.r is not None) and (args.a is not None):
        if args.a == 'on':
            send_command(RELAY_ON[args.r])
        elif args.a == 'off':
            send_command(RELAY_OFF[args.r])
        elif args.a == 'click':
            click_relay(args.r)
        else:
            raise ValueError('invalid action: %s' % args.a)
    else:
        parser.print_help()
        sys.exit(1)
    sys.exit()
