#!/usr/bin/python

from playing.pi.gpio.i2c.Adafruit_I2C import Adafruit_I2C

# Used for testing only
import time
import RPi.GPIO as GPIO

class MCP23017Bank():
   def __init__(self,name,direction=0xff,pullups=0x00,polarity=0x00,interruptsEnabled=0x00,interruptsDefaults=0x00,interruptsType=0xff,latch=0x00):
      self.name = name
      self.direction = direction
      self.pullups = pullups
      self.polarity = polarity
      self.interruptsEnabled = interruptsEnabled
      self.interruptsDefaults = interruptsDefaults
      self.interruptsType = interruptsType
      self.latch = latch

   def printLatchValues(self):
      print 'Latch Value: 0x%0.2x' % self.latch
      zero = self.latch 
      one = self.latch
      two = self.latch
      three = self.latch
      four = self.latch
      five = self.latch
      six = self.latch
      seven = self.latch

      zero = zero & (1 << 0)
      one = one & (1 << 1)
      two = two & (1 << 2)
      three = three & (1 << 3)
      four = four & (1 << 4)
      five = five & (1 << 5)
      six = six & (1 << 6)
      seven = seven & (1 << 7)

      a = [zero, one, two, three, four, five, six, seven]
      for i in range(len(a)):
         if a[i] == (1 << i):
            isSet = True
         else:
            isSet = False
         print 'GP%s%d:%s' % (self.name, i, isSet)
   
class MCP23017():

   # Register Constants
   IODIRA   = 0x00     # Input or Output
   IODIRB   = 0x01     # Input or Output
   IOPOLA   = 0x02     # Invert polarity of input pins
   IOPOLB   = 0x03     # Invert polarity of input pins
   GPINTENA = 0x04     # Interrupt on change controls register (corrosponding DEFVAL and INTCON must also be configured)
   GPINTENB = 0x05     # Interrupt on change controls register (corrosponding DEFVAL and INTCON must also be configured)
   DEFVALA  = 0x06     # Default comapre register (interrupt will occur when there is a mismatch between this and the value of the pin) 
   DEFVALB  = 0x07     # Default comapre register (interrupt will occur when there is a mismatch between this and the value of the pin)
   INTCONA  = 0x08     # Interrupt control register (specifies how the interrupts work)
   INTCONB  = 0x09     # Interrupt control register (specifies how the interrupts work)
   IOCON    = 0x0a     # I/O expander configuration register 
   GPPUA    = 0x0c     # Enable / disable pull-up resistors 
   GPPUB    = 0x0d     # Enable / disable pull-up resistors 
   INTFA    = 0x0e     # Interrupt flag register (shows which pin caused the interrupt)
   INTFB    = 0xff     # Interrupt flag register (shows which pin caused the interrupt)
   INTCAPA  = 0x10     # Interrupt capture register (the value at the time the interrupt occurred
   INTCAPB  = 0x11     # Interrupt capture register (the value at the time the interrupt occurred
   GPIOA    = 0x12     # Read and write to the pins in the bank
   GPIOB    = 0x13     # Read and write to the pins in the bank
   OLATA    = 0x14     # Output latch 
   OLATB    = 0x15     # Output latch

   MIRROR_BIT = 6      # The bit in IOCON that controls the mirroring behaviour of the interrupts


   INPUT  = True
   OUTPUT = False

   def __init__(self, addr=0x20):
      self.i2c = Adafruit_I2C(addr)
      self.bankA = MCP23017Bank('A')
      self.bankB = MCP23017Bank('B')
      self.config = self.i2c.readU8(self.IOCON)

      # Bank A
      self.i2c.write8(self.IODIRA, self.bankA.direction)
      self.i2c.write8(self.GPPUA, self.bankA.pullups)
      self.i2c.write8(self.IOPOLA, self.bankA.polarity)
      self.i2c.write8(self.GPINTENA, self.bankA.interruptsEnabled)
      self.i2c.write8(self.DEFVALA, self.bankA.interruptsDefaults)
      self.i2c.write8(self.INTCONA, self.bankA.interruptsType)
      self.bankA.latch = self.i2c.readU8(self.OLATA)
      # Bank B
      self.i2c.write8(self.IODIRB, self.bankB.direction)
      self.i2c.write8(self.GPPUB, self.bankB.pullups)
      self.i2c.write8(self.IOPOLB, self.bankB.polarity)
      self.i2c.write8(self.GPINTENB, self.bankB.interruptsEnabled)
      self.i2c.write8(self.DEFVALB, self.bankB.interruptsDefaults)
      self.i2c.write8(self.INTCONA, self.bankA.interruptsType)
      self.bankB.latch = self.i2c.readU8(self.OLATB)


   def output(self, bank, pin, value):
      assert 0 <= pin <= 7, 'Invalid pin number'
      assert bank in ('A', 'B'), 'Bank can be either A or B nothing else'

      if bank == 'A':
         if value:
            self.bankA.latch = self.bankA.latch | (1 << pin)
         else:
            self.bankA.latch = self.bankA.latch & ~(1 << pin)
         self.i2c.write8(self.OLATA, self.bankA.latch)
      if bank == 'B':
         if value:
            self.bankB.latch = self.bankB.latch | (1 << pin)
         else:
            self.bankB.latch = self.bankB.latch & ~(1 << pin)
         self.i2c.write8(self.OLATB, self.bankB.latch)


   def input(self, bank, pin):
      assert 0 <= pin <= 7, 'Invalid pin number'
      assert bank in ('A', 'B'), 'Bank can be either A or B nothing else'

      if bank == 'A':
         assert (self.bankA.direction & (1 << pin)) != 0, 'Pin is not configures as input'
         value = self.i2c.readU8(self.GPIOA)

      if bank == 'B':
         assert (self.bankB.direction & (1 << pin)) != 0, 'Pin is not configures as input'
         value = self.i2c.readU8(self.GPIOB)

      return (value >> pin) & 1

   def configInterruptMirroring(self, enable=True):
      if enable: 
         self.config = self.config | (1 << MIRROR_BIT)
      else:
         self.config = self.config & ~(1 << MIRROR_BIT)

      self.i2c.write8(self.IOCON, self.config)




   def configPin(self,bank,pin,pullup=None,direction=None,polarity=None,interruptEnabled=None,interruptDefault=None,interruptType=None):
      assert 0 <= pin <= 7, 'Invalid pin number'
      assert bank in ('A', 'B'), 'Bank can be either A or B nothing else'
      assert pullup in (None, True, False), 'Invalid value for pullup argument, must be None, True, or False'
      assert direction in (None, True, False), 'Invalid value for direction argument, must be None, True, or False'
      assert polarity in (None, True, False), 'Invalid value for polarity argument, must be None, True, or False'
      assert interruptEnabled in (None, True, False), 'Invalud value for interruptEnabled argument, must ne None, True, or False'

      if interruptEnabled is not None:
         assert interruptDefault in (True, False), 'Default value for interrupt check must be provided'
         assert interruptType in (True, False), 'Type of interrupt must be provided'

      if pullup == None and direction == None and polarity == None and interruptEnabled == None:
         return #Nothing to do as no values are not specified. 
      
      if bank == 'A':
         if pullup == True:
            self.bankA.pullups = self.bankA.pullups | (1 << pin)
         elif pullup == False:
            self.bankA.pullups = self.bankA.pullups & ~(1 << pin)
         
         if pullup in (True, False):
            self.i2c.write8(self.GPPUA, self.bankA.pullups)

         if direction == True:
            self.bankA.direction = self.bankA.direction | (1 << pin)
         elif direction == False:
            self.bankA.direction = self.bankA.direction & ~(1 << pin)

         if direction in (True, False):
            self.i2c.write8(self.IODIRA, self.bankA.direction)

         if polarity == True:
            self.bankA.polarity = self.bankA.polarity | (1 << pin)
         elif polarity == False:
            self.bankA.polarity = self.bankA.polarity & ~(1 << pin)

         if polarity in (True, False):
            self.i2c.write8(self.IOPOLA, self.bankA.polarity)

         if interruptEnabled == True:
            self.bankA.interruptsEnabled = self.bankA.interruptsEnabled | (1 << pin)
         elif interruptEnabled == False:
            self.bankA.interruptsEnabled = self.bankA.interruptsEnabled & ~(1 << pin)

         if interruptDefault == True:
            self.bankA.interruptsDefaults = self.bankA.interruptsDefaults | (1 << pin)
         elif interruptDefault == False:
            self.bankA.interruptsDefaults = self.bankA.interruptsDefaults & ~(1 << pin)

         if interruptType == True:
            self.bankA.interruptsType = self.bankA.interruptsType  | (1 << pin)
         elif interruptType == False:
            self.bankA.interruptsType = self.bankA.interruptsType & ~(1 << pin)

         if interruptEnabled in (True, False):
            self.i2c.write8(self.GPINTENA, self.bankA.interruptsEnabled)
            self.i2c.write8(self.DEFVALA, self.bankA.interruptsDefaults)
            self.i2c.write8(self.INTCONA, self.bankA.interruptsType)

      if bank == 'B':
         if pullup == True:
            self.bankB.pullups = self.bankB.pullups | (1 << pin)
         elif pullup == False:
            self.bankB.pullups = self.bankB.pullups & ~(1 << pin)
         
         if pullup in (True, False):
            self.i2c.write8(self.GPPUB, self.bankB.pullups)

         if direction == True:
            self.bankB.direction = self.bankB.direction | (1 << pin)
         elif direction == False:
            self.bankB.direction = self.bankB.direction & ~(1 << pin)

         if direction in (True, False):
            self.i2c.write8(self.IODIRB, self.bankB.direction)

         if polarity == True:
            self.bankB.polarity = self.bankB.polarity | (1 << pin)
         elif polarity == False:
            self.bankB.polarity = self.bankB.polarity & ~(1 << pin)

         if polarity in (True, False):
            self.i2c.write8(self.IOPOLB, self.bankB.polarity)
            
         if interruptEnabled == True:
            self.bankB.interruptsEnabled = self.bankB.interruptsEnabled | (1 << pin)
         elif interruptEnabled == False:
            self.bankB.interruptsEnabled = self.bankB.interruptsEnabled & ~(1 << pin)

         if interruptDefault == True:
            self.bankB.interruptsDefaults = self.bankB.interruptsDefaults | (1 << pin)
         elif interruptDefault == False:
            self.bankB.interruptsDefaults = self.bankB.interruptsDefaults & ~(1 << pin)

         if interruptType == True:
            self.bankB.interruptsType = self.bankB.interruptsType  | (1 << pin)
         elif interruptType == False:
            self.bankB.interruptsType = self.bankB.interruptsType & ~(1 << pin)

         if interruptEnabled in (True, False):
            self.i2c.write8(self.GPINTENB, self.bankB.interruptsEnabled)
            self.i2c.write8(self.DEFVALB, self.bankB.interruptsDefaults)
            self.i2c.write8(self.INTCONB, self.bankB.interruptsType)




if __name__=='__main__':
   mcp = MCP23017()
   mcp.configPin('A', 7, pullup=True, direction=True, polarity=True, interruptEnabled=True, interruptDefault=False, interruptType=False)

   #while True:
   #   print mcp.input('A',7)
   #   time.sleep(0.05)

   GPIO.setmode(GPIO.BCM)

   GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

   try:
      GPIO.wait_for_edge(22, GPIO.FALLING)
      print 'button pressed'

   except KeyboardInterrupt:
      GPIO.cleanup()
   GPIO.cleanup()

   



