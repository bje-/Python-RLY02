"""Control an RLY02 USB relay"""

import time
import getopt
import sys
from struct import unpack
import serial

SERIAL_PATH = '/dev/ttyACM0'
BAUD_RATE = 9600

commands = {
    'relay_1_on': 0x65,
    'relay_1_off': 0x6F,
    'relay_2_on': 0x66,
    'relay_2_off': 0x70,
    'info': 0x5A,
    'relay_states': 0x5B,
}


def send_command(cmd, read_response=False):
    """Send a command down the USB line"""
    ser = serial.Serial(SERIAL_PATH, BAUD_RATE)
    ser.write(chr(cmd) + '\n')
    response = ser.read() if read_response else None
    ser.close()
    return response


def turn_relay_1_on():
    """Turn relay 1 on"""
    send_command(commands['relay_1_on'])


def turn_relay_1_off():
    """Turn relay 1 off"""
    send_command(commands['relay_1_off'])


def click_relay_1():
    """Click relay 1"""
    send_command(commands['relay_1_on'])
    time.sleep(1)
    send_command(commands['relay_1_off'])


def turn_relay_2_on():
    """Turn relay 2 on"""
    send_command(commands['relay_2_on'])


def turn_relay_2_off():
    """Turn relay 2 off"""
    send_command(commands['relay_2_off'])


def click_relay_2():
    """Click relay 2"""
    send_command(commands['relay_2_on'])
    time.sleep(1)
    send_command(commands['relay_2_off'])


def get_relay_states():
    """Get the state of the two relays"""
    states = send_command(commands['relay_states'], read_response=True)
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
                        '1_on': turn_relay_1_on,
                        '1_off': turn_relay_1_off,
                        '1_click': click_relay_1,
                        '2_on': turn_relay_2_on,
                        '2_off': turn_relay_2_off,
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
