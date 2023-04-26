from machine import I2C
import struct


class M5_8Encoder:
    ENCODERS = const(8)
    LEDS = const(9)

    def __init__(
        self,
        i2c: I2C,
        address: int = 0x41,
    ):
        self.address = address
        self._i2c = i2c

    def _read(self, mem_addr: int, num_bytes: int):
        self._i2c.writeto(self.address, bytes([mem_addr]))
        return self._i2c.readfrom(self.address, num_bytes)

    def _write(self, mem_addr: int, data: bytes):
        self._i2c.writeto_mem(self.address, mem_addr, data)

    def read_counter(self, counter: int):
        if not (0 <= counter < self.ENCODERS):
            raise ValueError(
                f"Invalid counter number {counter} (valid values: 0-{self.ENCODERS - 1})"
            )

        val = self._read(4 * counter, 4)
        return struct.unpack("<i", val)[0]

    def read_all_counters(self):
        return [self.read_counter(i) for i in range(self.ENCODERS)]

    def read_increment(self, counter: int):
        if not (0 <= counter < self.ENCODERS):
            raise ValueError(
                f"Invalid increment number {counter} (valid values: 0-{self.ENCODERS - 1})"
            )

        val = self._read(0x20 + 4 * counter, 4)
        return struct.unpack("<i", val)[0]

    def read_all_increments(self):
        return [self.read_increment(i) for i in range(self.ENCODERS)]

    def set_led(self, led: int, color: bytes):
        if not (0 <= led < self.ENCODERS):
            raise ValueError(
                f"Invalid led number {led} (valid values: 0-{self.LEDS - 1})"
            )

        if len(color) != 3:
            raise ValueError(
                f"Colour must be a bytearray of lenth 3 (not {len(color)})"
            )

        self._write(0x70 + 3 * led, color)
