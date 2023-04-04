#! /bin/bash -eu

case "$1" in
    CH1) ch=26 ;;
    CH2) ch=20 ;;
    CH3) ch=21 ;;
    *)
	echo "Parameter error (channel)" >&2
	exit 1
	;;
esac

case "$2" in
    ON) state=0 ;;
    OFF) state=1 ;;
    *)
	echo "Parameter error (state)" >&2
	exit 1
	;;
esac

# Check if gpio is already exported
if [ ! -d /sys/class/gpio/"gpio$ch" ] ; then
    echo "$ch" > /sys/class/gpio/export
fi
echo out > /sys/class/gpio/"gpio$ch"/direction
echo "$state" > /sys/class/gpio/"gpio$ch"/value
echo "Done: $1 $2"
exit 0
