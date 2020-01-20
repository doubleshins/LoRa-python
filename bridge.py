#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import sys

sys.path.insert(0, '/usr/lib/python2.7/bridge/')  
from bridgeclient import BridgeClient as bridgeclient
value = bridgeclient()

while True:
    h0 = value.get("hour")
    t0 = value.get("minute")
    b0 = value.get("second")
    print "MCU Sensor Data :"+h0+"/"+t0+"/"+b0   
    time.sleep(0.2)
