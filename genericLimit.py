import asyncio

from gpioPin import GenericPin

class GenericLimit:
    def __init__(self, limitPin, pushedOnHighSignal=False):
        #pushedOnHigh:
        #   generally true if pullDown and false if pullUp
        self.pin = limitPin
        self.pushedOnHighSignal = pushedOnHighSignal

    def isPressed(self) -> bool:
        state = True if self.pin.getValue() is GenericPin.HIGH else False
        return not (self.pushedOnHighSignal ^ state )  # xnor