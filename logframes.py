#!/usr/bin/env python
from at86_fns import *
import RPi.GPIO as GPIO
import time

datalogfile='/root/at86packets.log'

def callback(channel):
 with open(datalogfile,'a') as outfile:
  timestamp=time.time()
  outfile.write('%s,' % timestamp)
  phy,resp2,hexresp2=readframe()
  outfile.write('%s\n' % resp2)
  print 'time is %s and response array isi %s' % (timestamp, resp2)
 getirq()
 #time.sleep(1) #this was to rate limit the repeating calls to callback, isn't happening any more

'''
x,y,z,q=readreg(0x01) #check if we are in rx
if 0x06==y:
 print 'confirmed in rx mode'
else:
 raise NameError('not in rx mode')
'''
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN)
GPIO.add_event_detect(23,GPIO.RISING,callback=callback)
getirq() #we need to clear this so we don't loop forever - this is after the event attach to prevent any chance for missing
while 1:
 try:
  time.sleep(1)
 except KeyboardInterrupt:
  GPIO.cleanup()
  raise NameError('keyboard interrupted')
 
