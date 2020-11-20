
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
        # mcpProtocol = MCP23017Protocol()
        # controller.registerProtocol(mcpProtocol)
        
        print(f"Available gpio protocols: {controller.getProtocols()}")

        # testPin = controller.registerPin("local:10", 
        #     GenericPin.OUTPUT, GenericPin.ON_DESTRUCT_OUT_LOW)
        # tsetPin2 = controller.registerPin(f"{mcpProtocol.prefix}:3",
        #     GenericPin.OUTPUT, GenericPin.ON_DESTRUCT_OUT_LOW)

        # testRedPin = controller.registerPin(f"{mcpProtocol.prefix}:7",
        #         GenericPin.OUTPUT, GenericPin.ON_DESTRUCT_OUT_LOW)
        # testGrnPin = controller.registerPin(f"{mcpProtocol.prefix}:6")
        # testBluPin = controller.registerPin(f"{mcpProtocol.prefix}:5")

        # await asyncio.sleep(.5)
        # testRedPin.setValue(GenericPin.HIGH)
        # await asyncio.sleep(.5)
        # testRedPin.setValue(GenericPin.LOW)
        # await asyncio.sleep(.5)
        # testRedPin.setValue(GenericPin.HIGH)

        try:
            # dirPin = controller.registerPin("local:17", GenericPin.OUTPUT)
            # stepPin = controller.registerPin("local:27", GenericPin.OUTPUT)
            # enablePin = controller.registerPin("local:22", GenericPin.OUTPUT)

            dirPin = controller.registerPin("local:10", GenericPin.OUTPUT)
            stepPin = controller.registerPin("local:9", GenericPin.OUTPUT)
            enablePin = controller.registerPin("local:11", GenericPin.OUTPUT)
        except:
            print("Pin error")
        else:
            print("Pin OK")

        try: 
            motor = GenericStepper(enablePin, stepPin, dirPin)
        except:
            print("Motor error")
        else:
            print("Motor OK")
        #
        # # print("Rotating 400 steps:")
        # await motor.RotateSteps(GenericStepper.DIRECTION_STANDARD, 400)
        # await asyncio.sleep(1)
        # await motor.RotateSteps(GenericStepper.DIRECTION_REVERSE, 400)

        # buttonPin = controller.registerPin(f"{mcpProtocol.prefix}:8", GenericPin.INPUT_PULL_UP)
        # limit = GenericLimit(buttonPin)

        # while True:
        #     print(f"Pushed: {limit.isPressed()}")
        #     await asyncio.sleep(1)

        # axis = GenericAxis(limit, motor)
        # await axis.home()

        print("GPIO initalized")
        try:
            while True:
                t = await inboundQ.get()
                tokens = t.split(" ")

                if(tokens[0] == 'ECHO'):
                    m = t[t.find(' ')+1:]
                    print(f"Echoing t: {m}" )
                    await outboundQ.put(t)
                elif(tokens[0] == 'ENBL'):
                    #TODO - utilize motor id parameter
                    motor.enable(GenericStepper.ENABLE if tokens[2] == '+' else GenericStepper.DISABLE)
                    print(f"Processed ENBL: {t}")
                elif(tokens[0] == 'HOME'):
                    #TODO - implement
                    print("Home command not implemented.")
                elif(tokens[0] == 'M'):
                    #TODO - utilize motor id parameter
                    await motor.RotateSteps(
                            GenericStepper.DIRECTION_STANDARD if tokens[2] == "+" 
                            else GenericStepper.DIRECTION_REVERSE,
                            int(tokens[3]))
                else:
                    print(f"Unrecognized Command: {t}")
        except asyncio.CancelledError:
            print("GPIO CANCEL")
        finally:
            pass
        return