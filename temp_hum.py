#!/usr/bin/python
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import sys
import Adafruit_DHT
import time
import csv

# Set up sensor type and pin
sensor = Adafruit_DHT.DHT22
pin = 4


file = open("data.csv", "w")

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
for i in range(0,10):
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        temperature_f = temperature * 1.8 +32
        i = 0
        if humidity is not None and temperature is not None:
                        timestamp = time.strftime('%b %d, %Y  %I:%M:%S %P')
                        temp_hum = 'Temp={0:0.1f}*F  Humidity={1:0.1f}%'.format(temperature_f, humidity)
                        print time.strftime('%b %d, %Y  %I:%M:%S %P')
                        print 'Temp={0:0.1f}*F  Humidity={1:0.1f}%'.format(temperature_f, humidity)
                        file.write(timestamp, temp_hum)
                        i += 1
                        time.sleep(5)
        else:
                print 'Failed to get reading. Try again!'
                break
file.close()
