
from gpioPin import *
from gpioProtocol import *

class DuplicateProtocolException(Exception):
    pass

class ReservedPinException(Exception):
    pass

# allows for a generic interface with the GPIO pins
# protocol allows for off-board communication
#   by simply reserving the pins and allowing the pin to continue
# address format:
#   prefix:pin
class GPIOController():
    INITALIZED = False

    def __init__(self):
        if GPIOController.INITALIZED:
            raise RuntimeError("GPIO Controller already initalized")
        GPIOController.INITALIZED = True

        self.pinDict = {}  # path pin pairs for all reserved pins
        self.protocolPins = set() # pins for all protocols, can be reused by more protocols
        self.protocolDict = {}  # stored protocols registered
        self.registerProtocol(LocalProtocol())

    def __del__(self):
        # print("Controller DEL")
        for pp in self.pinDict:
            pin = self.pinDict[pp]
            del pin

        GPIOController.INITALIZED = False

    #given a generic protocol, register the required pins
    def registerProtocol(self, protocol):
        if protocol.prefix in self.protocolDict:
            raise DuplicateProtocolException(protocol)

        #checking the pins
        for pin in protocol.pins:
            prefix = PinAddress.getPrefix(pin)
            if prefix not in self.protocolDict:
                raise RuntimeError(f"Cannot intalize {protocol}, "
                            f"required pin {pin} not available in controller")

        for pin in protocol.pins:
            if pin in self.pinDict:
                raise ReservedPinException(pin)
        
        # we know the pins required are avilable
        self.protocolDict[protocol.prefix] = protocol

        # register the pins so that they cant be reused
        #   but can be reused for other modules
        for pin in protocol.pins:
            if pin not in self.protocolPins:
                self.protocolPins.add(pin)
        
        if protocol.initalize() is False:
            raise RuntimeError(f"Protocol {protocol} failed initalization")

    def registerPin(self, address, initalDir, 
            destructorVariant=GenericPin.ON_DESTRUCT_OUT_LOW) -> GenericPin:
        if address in self.pinDict:
            raise ReservedPinException(pin)
    
        (prefix, pinNumber) = PinAddress.getParts(address)
        if prefix not in self.protocolDict:
            raise RuntimeError(f"Protocol {protocol} not registered in controller")

        p = self.protocolDict[prefix].registerPin(pinNumber, initalDir, destructorVariant)
        self.pinDict[address] = p
        return p

    def getProtocols(self) -> list:
        return list(map(lambda x: x, self.protocolDict))

    async def __aenter__(self):
        # print("Controller enter")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # print("Contoller exit")
        # called after del of self
        pass