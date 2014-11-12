import spidev
import time
import sys

registerReadCommand = int('0x80',16)   #   // 1  0 ADDRESS[5:0]
registerWriteCommand = int('0xC0',16)  #1 1 ADDRESS[5:0]
frameReadCommand = int('0x20',16)  #0 0 1 reserved[4:0] see p17-18
frameWriteCommand = int('0x60',16)  #0 1 1 reserved[4:0] see p18
sramReadCommand = int('0x00',16)  #0 0 0 reserved[4:0] see p19-20  //address in byte 2 sent
sramWriteCommand = int('0x40',16)  #0 1 0 reserved[4:0] see p20


def readframe():
  print 'reading frame buffer, length in bytes TBD'
  commandByte = frameReadCommand
  print 'command byte is: ', hex(commandByte)
  spi = spidev.SpiDev()
  spi.open(0,0)
 
  resp=spi.xfer2([commandByte,0x00])  # xfer2 keeps ce open between bytes, xfer closes and reopns
  phy = hex(resp[0])
  phr = hex(resp[1])
  print 'PHY is: ', phy, ' PHR is: ', phr
  frame_length_to_read=resp[1]
  array_to_read_frame=[0x00]*frame_length_to_read
  array_to_read_frame.insert(0,commandByte)

  print 'frame of length: ', frame_length_to_read, ' usng array to read fram: ' , array_to_read_frame
  resp2=spi.xfer2(array_to_read_frame)  # xfer2 keeps ce open between bytes, xfer closes and reopns
  print 'as ints:'
  print resp2
  print 'in hex:'
  hexarr_resp2=[]
  for x in resp2:
    hexarr_resp2.append(hex(x))
  print hexarr_resp2
  print 'done'
  return phy, resp2, hexarr_resp2

#takes an array of bytes (ints) (usu passed in hex rep, but, still bytes)
#returns resp and hex_resp
def writeframe(frame_data):

  frameLength=len(frame_data)
  print 'writing frame buffer, length in bytes: ' , frameLength 

  commandByte = frameWriteCommand
  print 'command byte is: ', hex(commandByte)

  data_to_write=frame_data

  data_to_write.insert(0,frameLength)
  data_to_write.insert(0,commandByte)

  print 'data to write is: ', data_to_write 

  myarray=[]
  for x in data_to_write:
    myarray.append(hex(x))
  print 'showing as hex: ', myarray

  spi = spidev.SpiDev()
  spi.open(0,0)

  resp=spi.xfer2(data_to_write)  # xfer2 keeps ce open between bytes, xfer closes and reopns
  resp_phy=resp[0] # rest ignore
  hex_resp_phy=hex(resp_phy)
  
  print 'PHY is: ', hex_resp_phy
  print 'done'
  return resp, hex_resp_phy
  
#takes reg to read
# returns   return resp_phy, resp_val, hex_resp_phy, hex_resp_val
def readreg(register_to_read):
  print 'reading register: ' , hex(register_to_read)

  commandByte = ( register_to_read & int('0x3f', 16) ) | registerReadCommand
  print 'command byte is: ', hex(commandByte)

  spi = spidev.SpiDev()
  spi.open(0,0)

  resp=spi.xfer2([commandByte,0x00])  # xfer2 keeps ce open between bytes, xfer closes and reopns
  resp_phy=resp[0]
  resp_val=resp[1]
  hex_resp_phy=hex(resp_phy)
  hex_resp_val=hex(resp_val)
  print 'response is: PHY: ', hex_resp_phy, ' and register value: ', hex_resp_val
  return resp_phy, resp_val, hex_resp_phy, hex_resp_val
  
  

def writereg(register_to_write, data_to_write):
  print 'writing register: ' , hex(register_to_write)

  commandByte = ( register_to_write & int('0x3f', 16) ) | registerWriteCommand
  print 'command byte is: ', hex(commandByte)

  print 'data to write is: ', hex(data_to_write)

  spi = spidev.SpiDev()
  spi.open(0,0)

  resp=spi.xfer2([commandByte,data_to_write])  # xfer2 keeps ce open between bytes, xfer closes and reopns
  resp_phy=resp[0]
  hex_resp_phy=hex(resp_phy)
  print 'response is: PHY: ', resp_phy
  print 'response is: PHY: ', hex_resp_phy
  return resp_phy, hex_resp_phy


def setup():
  writereg(0x04,0x2e) # set spi cmd mode to return irq status in phy
  
def set_rx():
  writereg(0x02,0x08)
  writereg(0x02,0x06)
  
def set_tx():
  writereg(0x02,0x08)
  writereg(0x02,0x09)
  
def start_tx():
  writereg(0x02,0x02)
  
def getstatus():
  readreg(0x01)

def getirq():
  readreg(0x0f)



