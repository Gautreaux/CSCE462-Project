
import asyncio
import board

from gpioInterface import *
from gpioPin import GenericPin
from gpioProtocol import MCP23017Protocol

async def gpioHandler(inboundQ, outboundQ):
    # controller = GPIOController()
    async with GPIOController() as controller:
        mcpProtocol = MCP23017Protocol()
        controller.registerProtocol(mcpProtocol)
        
        print(f"Available gpio protocols: {controller.getProtocols()}")

        testPin = controller.registerPin("local:10", 
            GenericPin.OUTPUT, GenericPin.ON_DESTRUCT_OUT_LOW)
        tsetPin2 = controller.registerPin(f"{mcpProtocol.prefix}:3",
            GenericPin.OUTPUT, GenericPin.ON_DESTRUCT_OUT_LOW)

        testRedPin = controller.registerPin(f"{mcpProtocol.prefix}:7",
                GenericPin.OUTPUT, GenericPin.ON_DESTRUCT_OUT_LOW)
        # testGrnPin = controller.registerPin(f"{mcpProtocol.prefix}:6")
        # testBluPin = controller.registerPin(f"{mcpProtocol.prefix}:5")

        await asyncio.sleep(.5)
        testRedPin.setValue(GenericPin.HIGH)
        await asyncio.sleep(.5)
        testRedPin.setValue(GenericPin.LOW)
        await asyncio.sleep(.5)
        testRedPin.setValue(GenericPin.HIGH)

        print("GPIO initalized")
        try:
            while True:
                t = await inboundQ.get()
                print(f"Echoing t: {t}" )
                await outboundQ.put(t)
        except asyncio.CancelledError:
            print("GPIO CANCEL")
        finally:
            pass
        return