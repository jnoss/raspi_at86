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


register_to_read=int(sys.argv[1],16)
print 'reading spi1 register: ' , hex(register_to_read)

commandByte = ( register_to_read & int('0x3f', 16) ) | registerReadCommand
print 'command byte is: ', hex(commandByte)

spi = spidev.SpiDev()
spi.open(0,1)

resp=spi.xfer2([commandByte,0x00])  # xfer2 keeps ce open between bytes, xfer closes and reopns
print 'response is: PHY: ', hex(resp[0]), ' and register value: ', hex(resp[1])
