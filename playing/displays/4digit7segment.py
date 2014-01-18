#!/usr/bin/python

from playing.expanders.i2c.io.MCP23017 import MCP23017
import time

# This module makes use of the MCP23017 IO expander, if the configuration (pin allocation) is different then it will need adjusting here.
# For use on breadboard it makes sense to use bank A of one side of the display and bank B for the other side. In order to keep pin 1s 
# in the same orientation therefore bank B will be used for pins 1-8 and bank A for pins 9-16. 
# 
# This python code is based on the Arduino Countdown Timer by Sparkfun 
# http://www.hobbytronics.co.uk/tutorials-code/arduino-tutorials/arduino-countdown-timer 

class Pin:
	def __init__(self, bank, pinno):
		self.bank = bank
		self.pinno = pinno

class FourDigitSevenSegment:
	def __init__(self, brightness=500, flashColon=False, addr=None):
		self.brightness = brightness
		self.flashColon = flashColon
		self.mcp = MCP23017()
		self.mcp.configAll(direction=False)
		
		# Configure the port mappings
		self.digit1 = Pin('B', 0)
		self.digit2 = Pin('B', 1)
		self.digit3 = Pin('B', 5)
		self.digit4 = Pin('B', 7)
		self.segA   = Pin('A', 5)
		self.segB   = Pin('A', 7)
		self.segC   = Pin('A', 4)
		self.segD   = Pin('B', 2)
		self.segE   = Pin('B', 4)
		self.segF   = Pin('A', 2)
		self.segG   = Pin('A', 6)
		self.dp     = Pin('B', 6)
		self.colonA = Pin('B', 3)
		self.colonK = Pin('A', 3)
		self.apostropheA = Pin('A', 1)
		self.apostropheB = Pin('A', 0)
		
		self.DIGIT_OFF = False
		self.DIGIT_ON = True
		self.SEGMENT_ON = False
		self.SEGMENT_OFF = True       
		
	def displayNumber(self, num):
		digit = 4
		while digit > 0:
			if digit == 1:
				self.mcp.output(self.digit1.bank, self.digit1.pinno, self.DIGIT_ON)
			elif digit == 2: 
				self.mcp.output(self.digit2.bank, self.digit2.pinno, self.DIGIT_ON)
			elif digit == 3:
				self.mcp.output(self.digit3.bank, self.digit3.pinno, self.DIGIT_ON)
			elif digit == 4:
				self.mcp.output(self.digit4.bank, self.digit4.pinno, self.DIGIT_ON)


			self.lightNumber(num % 10)
			num /= 10

			time.sleep(self.brightness/1000000)

			self.lightNumber(10)
			
			self.mcp.output(self.digit1.bank, self.digit1.pinno, self.DIGIT_OFF)
			self.mcp.output(self.digit2.bank, self.digit2.pinno, self.DIGIT_OFF)
			self.mcp.output(self.digit3.bank, self.digit3.pinno, self.DIGIT_OFF)
			self.mcp.output(self.digit4.bank, self.digit4.pinno, self.DIGIT_OFF)
			
			digit = digit - 1
			
		#time.sleep(20 / 1000)



	def lightNumber(self, num):
		if num == 0:
			self.mcp.output(self.segA.bank, self.segA.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segB.bank, self.segB.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segC.bank, self.segC.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segD.bank, self.segD.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segE.bank, self.segE.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segF.bank, self.segF.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segG.bank, self.segG.pinno, self.SEGMENT_OFF)
			self.mcp.output(self.dp.bank, self.dp.pinno, self.SEGMENT_OFF)
		elif num == 1:
			self.mcp.output(self.segA.bank, self.segA.pinno, self.SEGMENT_OFF)
			self.mcp.output(self.segB.bank, self.segB.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segC.bank, self.segC.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segD.bank, self.segD.pinno, self.SEGMENT_OFF)
			self.mcp.output(self.segE.bank, self.segE.pinno, self.SEGMENT_OFF)
			self.mcp.output(self.segF.bank, self.segF.pinno, self.SEGMENT_OFF)
			self.mcp.output(self.segG.bank, self.segG.pinno, self.SEGMENT_OFF)
			self.mcp.output(self.dp.bank, self.dp.pinno, self.SEGMENT_OFF)
		elif num == 2:
			self.mcp.output(self.segA.bank, self.segA.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segB.bank, self.segB.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segC.bank, self.segC.pinno, self.SEGMENT_OFF)
			self.mcp.output(self.segD.bank, self.segD.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segE.bank, self.segE.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segF.bank, self.segF.pinno, self.SEGMENT_OFF)
			self.mcp.output(self.segG.bank, self.segG.pinno, self.SEGMENT_ON)
			self.mcp.output(self.dp.bank, self.dp.pinno, self.SEGMENT_OFF)
		elif num == 3:
			self.mcp.output(self.segA.bank, self.segA.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segB.bank, self.segB.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segC.bank, self.segC.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segD.bank, self.segD.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segE.bank, self.segE.pinno, self.SEGMENT_OFF)
			self.mcp.output(self.segF.bank, self.segF.pinno, self.SEGMENT_OFF)
			self.mcp.output(self.segG.bank, self.segG.pinno, self.SEGMENT_ON)
			self.mcp.output(self.dp.bank, self.dp.pinno, self.SEGMENT_OFF)
		elif num == 4:
			self.mcp.output(self.segA.bank, self.segA.pinno, self.SEGMENT_OFF)
			self.mcp.output(self.segB.bank, self.segB.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segC.bank, self.segC.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segD.bank, self.segD.pinno, self.SEGMENT_OFF)
			self.mcp.output(self.segE.bank, self.segE.pinno, self.SEGMENT_OFF)
			self.mcp.output(self.segF.bank, self.segF.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segG.bank, self.segG.pinno, self.SEGMENT_ON)
			self.mcp.output(self.dp.bank, self.dp.pinno, self.SEGMENT_OFF)
		elif num == 5:
			self.mcp.output(self.segA.bank, self.segA.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segB.bank, self.segB.pinno, self.SEGMENT_OFF)
			self.mcp.output(self.segC.bank, self.segC.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segD.bank, self.segD.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segE.bank, self.segE.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segF.bank, self.segF.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segG.bank, self.segG.pinno, self.SEGMENT_ON)
			self.mcp.output(self.dp.bank, self.dp.pinno, self.SEGMENT_OFF)
		elif num == 6:
			self.mcp.output(self.segA.bank, self.segA.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segB.bank, self.segB.pinno, self.SEGMENT_OFF)
			self.mcp.output(self.segC.bank, self.segC.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segD.bank, self.segD.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segE.bank, self.segE.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segF.bank, self.segF.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segG.bank, self.segG.pinno, self.SEGMENT_ON)
			self.mcp.output(self.dp.bank, self.dp.pinno, self.SEGMENT_OFF)
		elif num == 7:
			self.mcp.output(self.segA.bank, self.segA.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segB.bank, self.segB.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segC.bank, self.segC.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segD.bank, self.segD.pinno, self.SEGMENT_OFF)
			self.mcp.output(self.segE.bank, self.segE.pinno, self.SEGMENT_OFF)
			self.mcp.output(self.segF.bank, self.segF.pinno, self.SEGMENT_OFF)
			self.mcp.output(self.segG.bank, self.segG.pinno, self.SEGMENT_OFF)
			self.mcp.output(self.dp.bank, self.dp.pinno, self.SEGMENT_OFF)
		elif num == 8:
			self.mcp.output(self.segA.bank, self.segA.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segB.bank, self.segB.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segC.bank, self.segC.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segD.bank, self.segD.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segE.bank, self.segE.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segF.bank, self.segF.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segG.bank, self.segG.pinno, self.SEGMENT_ON)
			self.mcp.output(self.dp.bank, self.dp.pinno, self.SEGMENT_OFF)
		elif num == 9:
			self.mcp.output(self.segA.bank, self.segA.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segB.bank, self.segB.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segC.bank, self.segC.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segD.bank, self.segD.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segE.bank, self.segE.pinno, self.SEGMENT_OFF)
			self.mcp.output(self.segF.bank, self.segF.pinno, self.SEGMENT_ON)
			self.mcp.output(self.segG.bank, self.segG.pinno, self.SEGMENT_ON)
			self.mcp.output(self.dp.bank, self.dp.pinno, self.SEGMENT_OFF)
		elif num == 10:
			self.mcp.output(self.segA.bank, self.segA.pinno, self.SEGMENT_OFF)
			self.mcp.output(self.segB.bank, self.segB.pinno, self.SEGMENT_OFF)
			self.mcp.output(self.segC.bank, self.segC.pinno, self.SEGMENT_OFF)
			self.mcp.output(self.segD.bank, self.segD.pinno, self.SEGMENT_OFF)
			self.mcp.output(self.segE.bank, self.segE.pinno, self.SEGMENT_OFF)
			self.mcp.output(self.segF.bank, self.segF.pinno, self.SEGMENT_OFF)
			self.mcp.output(self.segG.bank, self.segG.pinno, self.SEGMENT_OFF)
			self.mcp.output(self.dp.bank, self.dp.pinno, self.SEGMENT_OFF)


if __name__=='__main__':
	display = FourDigitSevenSegment()
	while True:
		display.displayNumber(2310)
