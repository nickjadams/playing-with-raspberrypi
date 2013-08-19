#!/usr/bin/python

from playing.pi.gpio.i2c.Adafruit_I2C import Adafruit_I2C

#Constants
TC74 = 0x48			# Address of the TC74 on the I2C bus
REGISTER = 0x00	# The register where the temperature is read from
UNITS = u'\u2103'

bus = Adafruit_I2C(address=TC74)

def readTemp():
	return bus.readS8(REGISTER)

if __name__=='__main__':
	print str(readTemp()) + UNITS



