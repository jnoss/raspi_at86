#!/usr/bin/env python
from at86_fns import *

writereg(0x02,0x08) # have to go from P_ON to TRX_OFF before you can get to other states
writereg(0x04,0x2e) # set spi cmd mode to return irq status in phy
writereg(0x0e,0xff) # set irq mask to allow all interrupts to trigger irq pin
