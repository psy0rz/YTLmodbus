#!/usr/bin/python3

#read kwh meters and send values to influxdb
#for DDS353H-1 / DDS353H-2 / DDS353H-3 / YTL5281 / YTL5282 / YTL5283


import time
import minimalmodbus
import sys
import pprint
from influxdb import InfluxDBClient
import config

while True:
    try:
        #influx db settings
        db = InfluxDBClient(config.host,config.port, config.username, config.password, config.database)
        print("Connecting db")
        db.create_database('energy')


        rs485 = minimalmodbus.Instrument(config.serial_port, 1)
        rs485.serial.baudrate = 9600
        rs485.serial.bytesize = 8
        rs485.serial.parity = minimalmodbus.serial.PARITY_EVEN
        rs485.serial.stopbits = 1
        rs485.serial.timeout = 1
        rs485.debug = False
        rs485.mode = minimalmodbus.MODE_RTU
        # rs485.precalculate_read_size=True
        rs485.close_port_after_each_call=False

        if len(sys.argv)>1:
            rs485.address=int(sys.argv[1])
            cmd=sys.argv[2]
            if len(sys.argv)==4:
                par=eval(sys.argv[3])
            else:
                par=None

            if cmd=="pages":
                print(bin(rs485.read_register(0x112)))
                if par!=None:
                    rs485.write_register(0x112, par)
            
            #number of decimals (0, 1, 2)
            #scrolling time (seconds)
            if cmd=="display":
                print(bin(rs485.read_register(0x113)))
                if par!=None:
                    rs485.write_register(0x113, par)

            if cmd=="display2":
                print(bin(rs485.read_register(0x114)))
                if par!=None:
                    rs485.write_register(0x114, par)

            #??? default was 0b1111101000
            if cmd=="test1":
                print(bin(rs485.read_register(0x118)))
                if par!=None:
                    rs485.write_register(0x118, par)


            sys.exit(0)


        while True:


            influx_measurements=[]
            start_time=time.time()
            for id in range(1,13):
                rs485.address=id

                influx_measurement={
                    "measurement": "Meter values",
                    "tags": {
                        "Meter id": id
                    },
                    "fields": {
                        "Frequency": rs485.read_register(0x130, number_of_decimals=2),
                        "V1": rs485.read_register(0x131, number_of_decimals=2),
                        "I1": float(rs485.read_long(0x139))/1000,
                        "P1": rs485.read_long(0x140),
                        "Q1": rs485.read_long(0x148),
                        "S1": rs485.read_long(0x150),
                        "PF1": rs485.read_register(0x158,number_of_decimals=3),
                        "TA": float(rs485.read_long(0xA000))/100,
                        "TR": float(rs485.read_long(0xA01E))/100,
                    }
                }

                pprint.pprint(influx_measurement)
                influx_measurements.append(influx_measurement)
                time.sleep(0.03)


            print("Writing")
            db.write_points(influx_measurements)

            print("Done, pausing")
            time_left=10-(time.time()-start_time)
            if time_left>0:
                time.sleep(time_left)



    except Exception as e:
        print(str(e))
        print("Pausing and restarting...")
        time.sleep(10)



