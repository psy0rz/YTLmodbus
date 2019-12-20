#!/usr/bin/python
import time
import minimalmodbus
import sys

#crude tool to change initial id from 1 to something else
#for DDS353H-1 / DDS353H-2 / DDS353H-3 / YTL5281 / YTL5282 / YTL5283

id=int(sys.argv[1])

rs485 = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
rs485.serial.baudrate = 9600
rs485.serial.bytesize = 8
rs485.serial.parity = minimalmodbus.serial.PARITY_EVEN
rs485.serial.stopbits = 1
rs485.serial.timeout = 0.1
rs485.debug = False
rs485.mode = minimalmodbus.MODE_RTU


rs485new = minimalmodbus.Instrument('/dev/ttyUSB0', id)
rs485new.serial.baudrate = 9600
rs485new.serial.bytesize = 8
rs485new.serial.parity = minimalmodbus.serial.PARITY_EVEN
rs485new.serial.stopbits = 1
rs485new.serial.timeout = 0.1
rs485new.debug = False
rs485new.mode = minimalmodbus.MODE_RTU


while True:
    try:
        rs485.write_register(272, value=id)
        print("Changed id")

    except Exception as e:
        pass

    try:
        ret=rs485new.read_register(272)
        print("found id {}".format(ret))

    except Exception as e:
        print ("error")
        pass

    time.sleep(1)
