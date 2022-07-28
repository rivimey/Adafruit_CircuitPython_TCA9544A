# SPDX-FileCopyrightText: 2021 Carter Nelson for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example shows using TCA9544A to perform a simple scan for connected devices
import board
import adafruit_tca9544a

# Create I2C bus as normal
i2c = board.I2C()  # uses board.SCL and board.SDA

# Create the TCA9544A object and give it the I2C bus
tca = adafruit_tca9544a.TCA9544A(i2c)

for channel in range(4):
    if tca[channel].try_lock():
        print("Channel {}:".format(channel), end="")
        addresses = tca[channel].scan()
        # 0xF8 is address mask: 1110 xxx0 - where xxx is hw defined.
        print([hex(address) for address in addresses if (address & 0xF0) != 0xe0])
        tca[channel].unlock()
