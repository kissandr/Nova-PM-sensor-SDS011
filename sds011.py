#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:   Dr. M. Luetzelberger
# Date:     2017-03-08
# Name:     sds011_pylab.py
# Purpose:  UI for controlling SDS011 PM sensor
# Version:  1.0.1
# Depends:  must use Python 2.7, requires matplotlib
# Changes:
# Credits:  http://raspberryblog.de  
# TODO:     Enable sleep on start
#           Add datetime to UI 

from __future__ import print_function
import serial, struct, urllib2
api_key = "YOUR_THINGSPEAK_API_KEY"
ser = serial.Serial()
ser.port = "/dev/ttyS0"
ser.baudrate = 9600

ser.open()
ser.flushInput()

spm10=0
spm25=0
i=0
while i<56:
    byte = 0
    while byte != "\xaa":
        byte = ser.read(size=1)
    d = ser.read(size=10)
    if d[0] == "\xc0":
        r = struct.unpack('<xHHxxBBB', d)
        pm25 = r[0]/10.0
        pm10 = r[1]/10.0
        checksum = sum(ord(v) for v in d[1:7])%256
        #print("PM 2.5: {} μg/m^3  PM 10: {} μg/m^3 CRC={}".format(pm25, pm10, "OK" if (checksum==r[2] and r[3]==0xab) else "NOK"))
        if r[3]==0xab and checksum==r[2]:
            i+=1
            spm10+=pm10
            spm25+=pm25
pm10=spm10/i
pm25=spm25/i
print(pm10,pm25,i)
urllib2.urlopen("https://api.thingspeak.com/update?api_key={}&field1={}&field2={}".format(apikey,pm10,pm25)).read()

