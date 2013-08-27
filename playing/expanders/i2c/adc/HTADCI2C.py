#!/usr/bin/python

from playing.pi.gpio.i2c.Adafruit_I2C import Adafruit_I2C

# Used for testing
import time

class HTADCI2C():
   
   CONFIG_REGISTER = 0x00

   RESOLUTION_10BIT = True
   RESOLUTION_8BIT = False
   RESOLUTION_BIT = 0

   FILTER_ON = True
   FILTER_OFF = False
   FILTER_BIT = 1     # Although the filter is controled with two bits currently only the first bit is used. 
   
   def __init__(self, addr=0x2c):
      self.i2c = Adafruit_I2C(addr)
      self.config = self.i2c.readU8(self.CONFIG_REGISTER)
      self.resolution = self.RESOLUTION_8BIT

   def setResolution(self, resolution=RESOLUTION_8BIT):
      if resolution == self.RESOLUTION_8BIT:
         self.config = self.config & ~(1 << self.RESOLUTION_BIT)
         self.resolution = self.RESOLUTION_8BIT
      elif resolution == self.RESOLUTION_10BIT:
         self.config = self.config | (1 << self.RESOLUTION_BIT)
         self.resolution = self.RESOLUTION_10BIT

      self.i2c.write8(self.CONFIG_REGISTER, self.config)
     

   def setFilter(self, filterEnabled=FILTER_OFF):
      if filterEnabled == self.FILTER_ON:
         self.config = self.config & ~(1 << self.FILTER_BIT)
      elif filterEnabled == self.FILTER_OFF:
         self.config = self.config | (1 << self.FILTER_BIT)

      self.i2c.write8(self.CONFIG_REGISTER, self.config)

   def read(self, pin):
      if self.resolution == self.RESOLUTION_8BIT:
         return self.read8bit()[pin]
      else:
         values = self.read10bit()
         # 0 is items 0 and 1
         # 1 is items 2 and 3 
         # 2 is items 4 and 5
         # 3 is items 6 and 7
         # 4 is items 8 and 9
         # 5 is items 10 and 11
         # 6 is items 12 and 13
         # 7 is items 14 and 15
         # 8 is items 16 and 17
         # 9 is items 18 and 19

         pindoubled = pin * 2
         pindoubledplusone = pindoubled + 1

         high = values[pindoubled]
         low = values[pindoubledplusone]

         return (high << 8) + low


   def read8bit(self):
      return self.i2c.readList(0x01, 0x0a)

   def read10bit(self):
      return self.i2c.readList(0x00, 0x14)

if __name__=='__main__':
   adc = HTADCI2C()

   adc.setResolution(resolution=adc.RESOLUTION_10BIT)
   adc.setFilter(filterEnabled=adc.FILTER_ON)
   time.sleep(0.1)

   while True:
      print 'X,Y(%d,%d)' % (adc.read(1),adc.read(0))     # For testing this is attached to a analog thumbstick ala xbox.
      time.sleep(0.5)

