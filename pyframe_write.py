#!/usr/bin/env python
import spidev
import time
import sys

registerReadCommand = int('0x80',16)   #   // 1  0 ADDRESS[5:0]
registerWriteCommand = int('0xC0',16)  #1 1 ADDRESS[5:0]

frameReadCommand = int('0x20',16)  #0 0 1 reserved[4:0] see p17-18
frameWriteCommand = int('0x60',16)  #0 1 1 reserved[4:0] see p18
sramReadCommand = int('0x00',16)  #0 0 0 reserved[4:0] see p19-20  //address in byte 2 sent
sramWriteCommand = int('0x40',16)  #0 1 0 reserved[4:0] see p20

frameLength=len(sys.argv)-1

#register_to_write=int(sys.argv[1],16)
print 'writing frame buffer, length in bytes: ' , frameLength 

commandByte = frameWriteCommand
print 'command byte is: ', hex(commandByte)

#for byte_to_write in 
data_to_write=sys.argv[1:]
# print byte_to_write
data_to_write.insert(0,hex(frameLength))
data_to_write.insert(0,hex(commandByte))
#data_to_write=int(sys.argv[2],16)
print 'data to write is: ', data_to_write 

myarray=[]

for x in data_to_write:
 myarray.append(int(x,16))

print 'converted to ints: ', myarray

spi = spidev.SpiDev()
spi.open(0,0)

resp=spi.xfer2(myarray)  # xfer2 keeps ce open between bytes, xfer closes and reopns
print 'PHY is: ', hex(resp[0])
print resp
print 'done'
