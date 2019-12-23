#!/usr/bin/env python
import sys, serial, struct, urllib2
if len(sys.argv) != 4 or len(sys.argv[3])!=16:
    print("Usage:sds010.py <serial port> <samples> <Thingspeak API key>")
    exit()

ser = serial.Serial()
ser.port = sys.argv[1]
ser.baudrate = 9600
ser.open()
ser.flushInput()

spm10=0
spm25=0
i=0
while i<int(sys.argv[2]):
    byte = 0
    while byte != "\xaa":
        byte = ser.read(size=1)
    d = ser.read(size=10)
    if d[0] == "\xc0":
        r = struct.unpack('<xHHxxBBB', d)
        pm25 = r[0]/10.0
        pm10 = r[1]/10.0
        checksum = sum(ord(v) for v in d[1:7])%256
        if r[3]==0xab and checksum==r[2]:
            i+=1
            spm10+=pm10
            spm25+=pm25
#            print("{}: pm10={} pm2.5={}".format(i,pm10,pm25))

pm10=spm10/i
pm25=spm25/i
urllib2.urlopen("https://api.thingspeak.com/update?api_key={}&field1={}&field2={}".format(sys.argv[3],pm10,pm25)).read()

