#!/usr/bin/env python
from at86_fns import *

writereg(0x04,0x2e) # set spi cmd mode to return irq status in phy
