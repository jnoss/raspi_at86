#!/usr/bin/env python
from at86_fns import *

#print sys.argv[1:]
data_to_write=[]
for x in sys.argv[1:]:
 data_to_write.append(int(x,16))
#print data_to_write
writeframe(data_to_write)
