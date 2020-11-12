
from abc import ABC, abstractmethod
from digitalio import Direction, Pull
import RPi.GPIO as GPIO
# a generic pin regardless of location
class GenericPin(ABC):
    #Inital directions
    OUTPUT = 0
    INPUT_FLOAT = 1
    INPUT_PULL_UP = 2
    INPUT_PULL_DOWN = 3

    LOW = 0
    HIGH = 1

    #what to do when the pin is destructed
    ON_DESTRUCT_HOLD = -1 # hold last state
    ON_DESTRUCT_OUT_LOW = LOW # if output, go low
    ON_DESTRUCT_OUT_HIGH  = HIGH # if output, go high

    @abstractmethod
    def __init__(self, pinObj, initalDirection,
            destructorVariant=ON_DESTRUCT_OUT_LOW):
        self.pinObj = pinObj
        self.dir = initalDirection
        self.destructMode = destructorVariant

    def __del__(self):
        if self.isOutput() and self.destructMode != GenericPin.ON_DESTRUCT_HOLD:
            self.setValue(self.destructMode)

    def isInput(self):
        return not self.isOutput()

    def isOutput(self):
        return self.dir == GenericPin.OUTPUT
    
    @abstractmethod
    def switchToOutput(self):
        raise NotImplementedError

    @abstractmethod
    def switchToInput(self, mode=INPUT_FLOAT):
        raise NotImplementedError
    
    @abstractmethod
    def setValue(self, value):
        raise NotImplementedError

    @abstractmethod
    def getValue(self):
        raise NotImplementedError

class LocalPin(GenericPin):
    PinCounter = 0

    # pin OBJ should be the pin number
    def __init__(self, pinObj, initalDirection,
            destructorVariant=GenericPin.ON_DESTRUCT_OUT_LOW):
        
        if initalDirection in [GenericPin.INPUT_PULL_DOWN, GenericPin.INPUT_PULL_UP]:
            raise NotImplementedError("I got lazy")

        super().__init__(pinObj, initalDirection, destructorVariant)

        GPIO.setup(self.pinObj, GPIO.OUT if self.dir == GenericPin.OUTPUT else GPIO.IN)
        if(LocalPin.PinCounter == 0):
            GPIO.setmode(GPIO.BCM)
        LocalPin.PinCounter += 1
    
    def __del__(self):
        super().__del__()

        LocalPin.PinCounter -= 1
        if(LocalPin.PinCounter == 0):
            GPIO.cleanup()

    def switchToOutput(self):
        raise NotImplementedError("I got lazy")

    def switchToInput(self):
        raise NotImplementedError("I got lazy")

    def setValue(self, value):
        assert(self.isOutput())
        assert(value in [GenericPin.HIGH, GenericPin.LOW])
        GPIO.output(self.pinObj, 
                GPIO.LOW if value == GenericPin.LOW else GPIO.HIGH)
    
    def getValue(self):
        assert(self.isInput())
        return GPIO.input(self.pinObj)

    def __str__(self):
        return f"{self.pinObj}:{'Out' if self.isOutput() else 'In'}"

class MCP23017Pin(GenericPin):

    def __init__(self, pinObj, initalDirection,
            destructorVariant=GenericPin.ON_DESTRUCT_OUT_LOW):
        super().__init__(pinObj, initalDirection, destructorVariant)
        if initalDirection is GenericPin.OUTPUT:
            self.switchToOutput()
        else:
            self.switchToInput(initalDirection)

    def switchToOutput(self):
        self.dir = GenericPin.OUTPUT
        self.pinObj.direction = Direction.OUTPUT

    def switchToInput(self, mode=GenericPin.INPUT_FLOAT):
        self.pinObj.direction = Direction.INPUT
        self.dir = mode
        if(mode == GenericPin.INPUT_PULL_UP):
            pinObj.pull = Pull.UP
        elif(mode == GenericPin.INPUT_PULL_DOWN):
            pinObj.pull = Pull.DOWN

    def setValue(self, value):
        assert(self.isOutput())
        self.pinObj.value = (value == GenericPin.HIGH)

    def getValue(self):
        assert(self.isInput())
        return GenericPin.HIGH if self.pinObj is True else GenericPin.LOW