# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example shows using two TSL2491 light sensors attached to TCA9544A channels 0 and 1.
# Use with other I2C sensors would be similar.
import time
import board
import adafruit_tsl2591
import adafruit_tca9544a

# Create I2C bus as normal
i2c = board.I2C()  # uses board.SCL and board.SDA

# Create the TCA9544A object and give it the I2C bus
tca = adafruit_tca9544a.TCA9544A(i2c)

# For each sensor, create it using the TCA9544A channel instead of the I2C object
tsl1 = adafruit_tsl2591.TSL2591(tca[0])
tsl2 = adafruit_tsl2591.TSL2591(tca[1])

# After initial setup, can just use sensors as normal.
while True:
    print(tsl1.lux, tsl2.lux)
    time.sleep(0.1)
