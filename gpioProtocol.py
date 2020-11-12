
from abc import ABC, abstractmethod
from adafruit_mcp230xx.mcp23017 import MCP23017
import board
import busio

from gpioPin import *

class PinAddress():
    @staticmethod
    def isValidAddress(addr) -> bool:
        if addr.count(':') != 1:
            return False

        t = addr.rfind(':')
        return t not in [0,len(addr)-1, -1]
    
    @staticmethod
    def getPrefix(addr):
        assert(PinAddress.isValidAddress(addr))
        return addr.split(":")[0]
    
    @staticmethod
    def getPin(addr):
        assert(PinAddress.isValidAddress(addr))
        return int(addr.split(":")[1])

    @staticmethod
    def getParts(addr):
        assert(PinAddress.isValidAddress(addr))
        k = addr.split(":")
        return (k[0], int(k[1]))
    
    @staticmethod
    def getPinBatch(addrlist):
        return list(map(PinAddress.getPin, addrlist))

# a generic protocol for interfacing with a GPIO element
#tracks the pins required
class GenericProtocol(ABC):
    def __init__(self, requiredPins):
        self.pins = requiredPins
        #TODO - build the prefix of the required pins
        self.prefix = "GenericProcol" 

    def __str__(self):
        return self.prefix

    # call once the pins have been marked reserve by the controller
    # return ture if iniatlized properly
    @abstractmethod
    def initalize(self) -> bool:
        raise NotImplementedError 

    @abstractmethod
    def registerPin(self, pinNumber, initalDir, destructor) -> GenericPin:
        raise NotImplementedError

# protocol for interfacing with the local pins
class LocalProtocol(GenericProtocol):
    def __init__(self, requiredPins=[]):
        if(requiredPins != []):
            print(f"Warning: expected no pins for local protocol. Got {requiredPins}")
        super().__init__(requiredPins)
        self.prefix = "local"
    
    def initalize(self) -> bool:
        return True

    def registerPin(self, pinNumber, initalDir, destructor) -> LocalPin:
        return LocalPin(pinNumber, initalDir, destructor)

# protocol for interfacing with the MCP23017 pins
class MCP23017Protocol(GenericProtocol):
    DEFAULT_I2C = 32
    DEFAULT_SCL_PP = f"local:{board.SCL}"
    DEFAULT_SDA_PP = f"local:{board.SDA}"

    def __init__(self, requiredPins=[DEFAULT_SCL_PP, DEFAULT_SDA_PP], 
            i2cAddress=DEFAULT_I2C):
        super().__init__(requiredPins)
        self.addr = i2cAddress
        self.prefix = f"MCP23017@{i2cAddress}"
        self.mcp = None
    
    def initalize(self) -> bool:
        if self.mcp is not None:
            raise RuntimeError(f"{self.prefix} initalized multiple times")
            
        i2c = busio.I2C(*PinAddress.getPinBatch(self.pins))
        self.mcp = MCP23017(i2c)
        return True

    def registerPin(self, pinNumber, initalDir, destructor) -> MCP23017Pin:
        return MCP23017Pin(self.mcp.get_pin(pinNumber), initalDir, destructor)
        raise NotImplementedError