import board
import busio

import time
import RPi.GPIO as GPIO
import threading

from digitalio import Direction, Pull
from adafruit_mcp230xx.mcp23017 import MCP23017
i2c = busio.I2C(board.SCL, board.SDA)

mcp = MCP23017(i2c)
pinR = mcp.get_pin(7)
pinG = mcp.get_pin(6)
pinB = mcp.get_pin(5)

pinL = [pinR, pinG, pinB]

for pin in pinL:
    pin.direction = Direction.OUTPUT
    pin.switch_to_output(value=True)
    pin.value=False
threadRunning = True
def rbgledThread():
    

    def stateGenerator(period):
        s1 = 0
        s2 = 0
        s3 = 0

        while threadRunning:
            if s1 is 0:
                s1 = 1
            else:
                s1 = 0
                if s2 is 0:
                    s2 = 1
                else:
                    s2 = 0
                    if s3 is 0:
                        s3 = 1
                    else:
                        s3 = 0
            time.sleep(period)
            yield [s3, s2, s1]
        return

    try:
        for state in stateGenerator(.5):
            pinR.value = (state[0] is 1)
            pinB.value = (state[1] is 1)
            pinG.value = (state[2] is 1)
    finally:
        pinR.value = False
        pinB.value = False
        pinG.value = False


try:
    t = threading.Thread(target=rbgledThread)
    t.start()

    pinButton = mcp.get_pin(8)
    # pinButton.direction = Direction.OUTPUT
    # pinButton.switch_to_output(value=True)
    # pinButton.value=True
    pinButton.direction = Direction.INPUT
    pinButton.pull = Pull.UP
    lastButtonState = False

    while True:
        v = pinButton.value
        if v != lastButtonState:
            print("Pressed" if not v else "Released")
            lastButtonState = v
        time.sleep(.05)

finally:
    threadRunning = False
    pinR.value = False
    pinB.value = False
    pinG.value = False