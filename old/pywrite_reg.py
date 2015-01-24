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


register_to_write=int(sys.argv[1],16)
print 'writing register: ' , hex(register_to_write)

commandByte = ( register_to_write & int('0x3f', 16) ) | registerWriteCommand
print 'command byte is: ', hex(commandByte)

data_to_write=int(sys.argv[2],16)
print 'data to write is: ', hex(data_to_write)

spi = spidev.SpiDev()
spi.open(0,0)

resp=spi.xfer2([commandByte,data_to_write])  # xfer2 keeps ce open between bytes, xfer closes and reopns
print 'response is: PHY: ', hex(resp[0]), ' and reply while writing data: ', hex(resp[1])
