# Python-RLY02 #

Python code for controlling RLY02 (usb module with 2 relay outputs at 16A )

The relays are identified by 1 and 2 and the allowed actions are on, off and click. 
You can interact with them with things like:

## Swith relay 1 on ##
python rly02.py -r 1 -a on

## Swith relay 2 off ##
python rly02.py -r 1 -a off

## Click relay 1 (on and off) ##
python rly02.py -r 1 -a click

## Read relay states ##
python rly02.py -s

*NOTE:* ensure that you have the correct permissions in /dev/ttyACM0 for your user.

# Python-RLY08 #

There is a separate Python program capable of controlling the RLY08
with eight relays. It works just like the RLY02 program, but accepts
relay numbers (`-r`) up to 8. This program is backwards compatible
with the RLY02 board.

## Switch relay 7 on ##
python rly08.py -r 7 -a on

## Switch relay 7 off ##
python rly08.py -r 7 -a off
