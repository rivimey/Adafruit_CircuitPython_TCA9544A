# SPDX-FileCopyrightText: 2018 Carter Nelson for Adafruit Industries
# SPDX-FileCopyrightText: 2022 Ruth Ivimey-Cook adapted from TCA9548A module.
#
# SPDX-License-Identifier: MIT

"""
`adafruit_tca9544a`
====================================================

CircuitPython driver for the TCA9544A I2C Multiplexer.

* Author(s): Carter Nelson

Implementation Notes
--------------------

**Hardware:**

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

* Adafruit's Bus Device library:
  https://github.com/adafruit/Adafruit_CircuitPython_BusDevice

"""

from micropython import const

_DEFAULT_ADDRESS = const(0x70)

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/rivimey/Adafruit_CircuitPython_TCA9544A.git"


class TCA9544A_Channel:
    """Helper class to represent an output channel on the TCA9544A and take care
    of the necessary I2C commands for channel switching. This class needs to
    behave like an I2CDevice."""

    def __init__(self, tca, channel):
        self.tca = tca
        # NB: channel to select is bit0/bit1 and bit2=1 to connect chan.
        # NB: bit2=0 means no channel connected.
        self.channel_switch = bytearray([(channel & 0x3) | 0x4])
        # print("> channel_switch: ", self.channel_switch)

    def try_lock(self):
        """Pass through for try_lock."""
        # print("> try_lock(addr={}):".format(self.tca.address))
        if self.tca.i2c.try_lock():
            self.tca.i2c.writeto(self.tca.address, self.channel_switch)
            return True
        return False

    def unlock(self):
        """Pass through for unlock."""
        # NB: write '0' results in no channel connected.
        self.tca.i2c.writeto(self.tca.address, b"\x00")
        # print("> unlock()")
        return self.tca.i2c.unlock()

    def readfrom_into(self, address, buffer, **kwargs):
        """Pass through for readfrom_into."""
        if address == self.tca.address:
            raise ValueError("Device address must be different than TCA9544A address.")
        # print("> readfrom_into(addr={}):".format(address))
        result = self.tca.i2c.readfrom_into(address, buffer, **kwargs)
        # print(">         ... result={}):".format(buffer))
        return result

    def writeto(self, address, buffer, **kwargs):
        """Pass through for writeto."""
        if address == self.tca.address:
            raise ValueError("Device address must be different than TCA9544A address.")
        # print("> writeto(addr={}, data={}, len={}):".format(address, buffer, len(buffer)))
        return self.tca.i2c.writeto(address, buffer, **kwargs)

    def writeto_then_readfrom(self, address, buffer_out, buffer_in, **kwargs):
        """Pass through for writeto_then_readfrom."""
        # In linux, at least, this is a special kernel function call
        if address == self.tca.address:
            raise ValueError("Device address must be different than TCA9544A address.")
        # print("> writeto_then_readfrom(addr={}, data={}):".format(address, buffer_out))
        result = self.tca.i2c.writeto_then_readfrom(address, buffer_out, buffer_in, **kwargs)
        # print(">                          ... result={}):".format(buffer_in))
        return result

    def scan(self):
        """Perform an I2C Device Scan"""
        return self.tca.i2c.scan()


class TCA9544A:
    """Class which provides interface to TCA9544A I2C multiplexer.
    Device has 3 bits of address on pins, top 4 are fixed, so 0x70-0x77.
    Default address set to 0x70.
    """

    def __init__(self, i2c, address=_DEFAULT_ADDRESS):
        self.i2c = i2c
        self.address = address
        self.channels = [None] * 4

    def __len__(self):
        return 4

    def __getitem__(self, key):
        if not 0 <= key <= 3:
            raise IndexError("Channel must be an integer in the range: 0-3.")
        if self.channels[key] is None:
            self.channels[key] = TCA9544A_Channel(self, key)
        return self.channels[key]

    @property
    def interrupts(self):
        """Get the interrupt status. There is no mask, and values are not latched. """
        creg = self.controlreg
        return (creg & 0xF0) >> 4

    @property
    def controlreg(self):
        """Get the interrupt status. There is no mask, and values are not latched. """
        creg = bytearray([0x0])
        if self.i2c.try_lock():
            self.i2c.readfrom_into(self.address, creg)
            self.i2c.unlock()
        return int(creg[0])

