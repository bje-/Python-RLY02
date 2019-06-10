"""Control an RLY02 USB relay"""

import time
import getopt
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


def click_relay_1():
    """Click relay 1"""
    send_command(RELAY_1_ON)
    time.sleep(1)
    send_command(RELAY_1_OFF)


def click_relay_2():
    """Click relay 2"""
    send_command(RELAY_2_ON)
    time.sleep(1)
    send_command(RELAY_2_OFF)


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


def usage():
    """Print usage"""
    print """Change relay status:
    python rly02.py -r [1,2] -a [on, off, click]
Get device info:
    python rly02.py -i
Get relay states:
    python rly02.py -s
Help!;
    python rly02.py -h
"""


if __name__ == '__main__':

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hr:a:is",
                                   ["help", None, None, "info", "states"])
        dict_opts = {}
        for o, a in opts:
            dict_opts[o] = a
    except getopt.GetoptError:
        print
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ("-r",):
            if a in ['1', '2']:
                relay = a
                if '-a' in dict_opts and \
                   dict_opts['-a'] in ['on', 'off', 'click']:
                    action = dict_opts['-a']

                    actions = {
                        '1_on': lambda: send_command(RELAY_1_ON),
                        '1_off': lambda: send_command(RELAY_1_OFF),
                        '1_click': click_relay_1,
                        '2_on': lambda: send_command(RELAY_2_ON),
                        '2_off': lambda: send_command(RELAY_2_OFF),
                        '2_click': click_relay_2,
                    }
                    actions['%s_%s' % (relay, action)]()

                    sys.exit()
                else:
                    print "Action must be on, off or click"
            else:
                print "Relay must be 1 or 2"

        elif o in ("-s", "--states"):
            print get_relay_states()
            sys.exit()

    usage()
    sys.exit()
