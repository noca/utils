#!/bin/bash

# setting up irq affinity according to /proc/interrupts
# by Ningning Li
#
#  This script executes successfull in centos6.3 , other os did not test :)
#
#  This script will assign like:
#       em1-0  CPU0
#       em1-1  CPU1
#       em1-2  CPU2
#       em1-3  CPU3
#       em2-0  CPU0
#       em2-1  CPU1
#       em2-2  CPU2
#       em2-3  CPU3


set_affinity()
{
    MASK=$((1<<$VEC))
    printf "%s mask=%X for /proc/irq/%d/smp_affinity\n" $DEV $MASK $IRQ
    printf "%X" $MASK > /proc/irq/$IRQ/smp_affinity
    #echo $DEV mask=$MASK for /proc/irq/$IRQ/smp_affinity
    #echo $MASK > /proc/irq/$IRQ/smp_affinity
}


if [ "$1" = "" ] ; then
        echo "Description:"
        echo "    This script attempts to bind each queue of a multi-queue NIC"
        echo "    to the same numbered core, ie em1:0 --> cpu0, em2:0 --> cpu0"
        echo "usage:"
        echo "    $0 em1 [em1 ...]"
fi


# check for irqbalance running
IRQBALANCE_ON=`ps ax | grep -v grep | grep -q irqbalance; echo $?`
if [ "$IRQBALANCE_ON" == "0" ] ; then
        echo " WARNING: irqbalance is running and will"
        echo "          likely override this script's affinitization."
        echo "          Please stop the irqbalance service and/or execute"
        echo "          'killall irqbalance'"
        echo
        echo "or execute the following:"
        echo "/etc/init.d/irqbalance stop "
        echo "chkconfig irqbalance off    "
fi

#
# Set up the desired devices.
#

for DEV in $*
do
     MAX=`grep $DEV /proc/interrupts | wc -l`
     if [ "$MAX" == "0" ] ; then
       echo no $DIR vectors found on $DEV
       continue
       #exit 1
     fi

     for VEC in `seq 0 1 $MAX`
     do
        IRQ=`cat /proc/interrupts | grep -i $DEV-$VEC"$"  | cut  -d:  -f1 | sed "s/ //g"`
        if [ -n  "$IRQ" ]; then
          set_affinity
        fi
     done
done
