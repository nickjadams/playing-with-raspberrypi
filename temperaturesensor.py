#!/usr/bin/python

from gpio.i2c.Adafruit_I2C import Adafruit_I2C

bus = Adafruit_I2C(address=0x48)
print bus.readS8(0)

