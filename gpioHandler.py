
import asyncio
import board

from gpioInterface import *
from gpioPin import GenericPin
from gpioProtocol import MCP23017Protocol

from genericStepper import GenericStepper
from genericLimit import GenericLimit
from genericAxis import GenericAxis

async def gpioHandler(inboundQ, outboundQ):
    # controller = GPIOController()
    async with GPIOController() as controller:
        mcpProtocol = MCP23017Protocol()
        controller.registerProtocol(mcpProtocol)
        
        print(f"Available gpio protocols: {controller.getProtocols()}")

        # testPin = controller.registerPin("local:10", 
        #     GenericPin.OUTPUT, GenericPin.ON_DESTRUCT_OUT_LOW)
        # tsetPin2 = controller.registerPin(f"{mcpProtocol.prefix}:3",
        #     GenericPin.OUTPUT, GenericPin.ON_DESTRUCT_OUT_LOW)

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

        enablePin = controller.registerPin("local:10", GenericPin.OUTPUT)
        dirPin = controller.registerPin("local:9", GenericPin.OUTPUT)
        stepPin = controller.registerPin("local:11", GenericPin.OUTPUT)

        motor = GenericStepper(enablePin, stepPin, dirPin)

        # print("Rotating 400 steps:")
        await motor.RotateSteps(GenericStepper.DIRECTION_STANDARD, 400)
        await asyncio.sleep(1)
        await motor.RotateSteps(GenericStepper.DIRECTION_REVERSE, 400)

        buttonPin = controller.registerPin(f"{mcpProtocol.prefix}:8", GenericPin.INPUT_PULL_UP)
        limit = GenericLimit(buttonPin)

        # while True:
        #     print(f"Pushed: {limit.isPressed()}")
        #     await asyncio.sleep(1)

        axis = GenericAxis(limit, motor)
        await axis.home()

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