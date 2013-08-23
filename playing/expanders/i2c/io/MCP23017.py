#!/usr/bin/python

from playing.pi.gpio.i2c.Adafruit_I2C import Adafruit_I2C

import time

class MCP23017Bank():
	def __init__(self,name,direction=0x00,pullups=0x00,latch=0x00):
		self.name = name
		self.direction = direction
		self.pullups = pullups
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
   IODIRA = 0x00		# Input or Output
   IODIRB = 0x01		# Input or Output
   IOPOLA = 0x02		# Invert polarity of input pins
   IOPOLB = 0x03		# Invert polarity of input pins
   GPPUA  = 0x0c		# Enable / disable pull-up resistors 
   GPPUB  = 0x0d		# Enable / disable pull-up resistors 
   GPIOA  = 0x12		# Read and write to the values in the bank
   GPIOB  = 0x13		# Read and write to the values in the bank
   OLATA  = 0x14		# Output latch 
   OLATB  = 0x15		# Output latch


   INPUT  = True
   OUTPUT = False

   def __init__(self, addr=0x20):
      self.i2c = Adafruit_I2C(addr)
      self.bankA = MCP23017Bank('A')
      self.bankB = MCP23017Bank('B')
      # Bank A
      self.i2c.write8(self.IODIRA, self.bankA.direction)
      self.i2c.write8(self.GPPUA, self.bankA.pullups)
      self.bankA.latch = self.i2c.readU8(self.OLATA)
      # Bank B
      self.i2c.write8(self.IODIRB, self.bankB.direction)
      self.i2c.write8(self.GPPUB, self.bankB.pullups)
      self.bankB.latch = self.i2c.readU8(self.OLATB)


   def output(self, bank, pin, value):
      assert 0 <= pin <= 7, 'Invalid pin number'

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






if __name__=='__main__':
   mcp = MCP23017()
   print "0x%0.2x" % mcp.bankB.direction
   print mcp.bankA.printLatchValues()
   print mcp.bankB.printLatchValues()
   
   mcp.output('A', 7, True)
   time.sleep(1)
   mcp.output('A',6,True)
   time.sleep(1)
   mcp.output('A',5,True)
   time.sleep(1)
   mcp.output('A',4,True)
   time.sleep(1)
   mcp.output('A',3,True)
   time.sleep(1)
   mcp.output('A',2,True)
   time.sleep(1)
   mcp.output('A',1,True)
   time.sleep(1)
   mcp.output('A',0,True)
   time.sleep(1)
   mcp.output('B', 0, True)
   time.sleep(1)
   mcp.output('B',1,True)
   time.sleep(1)
   mcp.output('B',2,True)
   time.sleep(1)
   mcp.output('B',3,True)
   time.sleep(1)
   mcp.output('B',4,True)
   time.sleep(1)
   mcp.output('B',5,True)
   time.sleep(1)
   mcp.output('B',6,True)
   time.sleep(1)
   mcp.output('B',7,True)
   time.sleep(1)
   mcp.output('A', 7, False)
   time.sleep(1)
   mcp.output('A',6,False)
   time.sleep(1)
   mcp.output('A',5,False)
   time.sleep(1)
   mcp.output('A',4,False)
   time.sleep(1)
   mcp.output('A',3,False)
   time.sleep(1)
   mcp.output('A',2,False)
   time.sleep(1)
   mcp.output('A',1,False)
   time.sleep(1)
   mcp.output('A',0,False)
   time.sleep(1)
   mcp.output('B', 0, False)
   time.sleep(1)
   mcp.output('B',1,False)
   time.sleep(1)
   mcp.output('B',2,False)
   time.sleep(1)
   mcp.output('B',3,False)
   time.sleep(1)
   mcp.output('B',4,False)
   time.sleep(1)
   mcp.output('B',5,False)
   time.sleep(1)
   mcp.output('B',6,False)
   time.sleep(1)
   mcp.output('B',7,False)
   time.sleep(1)



