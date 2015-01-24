#!/usr/bin/env python
from at86_fns import *

register_to_write=int(sys.argv[1],16)
data_to_write=int(sys.argv[2],16)

writereg(register_to_write,data_to_write)
