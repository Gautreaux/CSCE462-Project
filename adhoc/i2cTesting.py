import board
import busio

import time

from digitalio import Direction
from adafruit_mcp230xx.mcp23017 import MCP23017
i2c = busio.I2C(board.SCL, board.SDA)

mcp = MCP23017(i2c)

pin0 = mcp.get_pin(7)
pin0.direction = Direction.OUTPUT
pin0.switch_to_output(value=True)

pin0.value = True

while True:
    print("HIGH")
    pin0.value = True
    time.sleep(.5)
    pin0.value = False
    time.sleep(.5)