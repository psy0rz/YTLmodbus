#!/usr/bin/python3
import time
import minimalmodbus
import sys

#crude tool to ping a bunch of meters on a bus
#for DDS353H-1 / DDS353H-2 / DDS353H-3 / YTL5281 / YTL5282 / YTL5283




rs485 = minimalmodbus.Instrument('/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0', 4)
rs485.serial.baudrate = 9600
rs485.serial.bytesize = 8
rs485.serial.parity = minimalmodbus.serial.PARITY_EVEN
rs485.serial.stopbits = 1
rs485.serial.timeout = 0.2
rs485.debug = False
rs485.mode = minimalmodbus.MODE_RTU


while True:
    print("scanning...")

    for i in range(1,20):
        try:
            rs485.address=i
            ret=rs485.read_register(272)
            print("reply from {}".format(ret))

        except Exception as e:
            pass

        time.sleep(0.1)
