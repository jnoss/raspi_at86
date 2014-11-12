#!/usr/bin/env python
import spidev
import time

import sys

print sys.argv[1]
hexin=int(sys.argv[1],16)
print hex(hexin)
hex2=hexin & int('0xc0',16)
print hex(hex2)

spi = spidev.SpiDev()
spi.open(0,0)

resp=spi.xfer2([0x00,0x00])
print resp
