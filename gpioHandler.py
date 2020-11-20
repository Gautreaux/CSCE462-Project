
import asyncio
import board

from gpioInterface import *
from gpioPin import GenericPin
from gpioProtocol import MCP23017Protocol

from genericStepper import GenericStepper
from genericLimit import GenericLimit
from genericAxis import GenericAxis

def getMotorId(charID):
    return ord(charID) - ord('A')

def gpioInit():
    with GPIOController() as controller:
        mcpProtocol = MCP23017Protocol()
        controller.registerProtocol(mcpProtocol)
        
        print(f"Available gpio protocols: {controller.getProtocols()}")

        motorSets = [
            # (dir, step, enable)
            # (green, yellow, white)
            ("local:17", "local:27","local:22"), # A
            ("local:14", "local:15","local:18"), # B
            ("local:10", "local:09","local:11"), # C
            ("local:00", "local:05","local:06"), # D
            ("local:13", "local:19","local:26"), # E
            ("local:16", "local:20","local:21"), # F
            ("local:08", "local:07","local:01"), # G
            ("local:23", "local:24","local:25"), # H
        ]
        limitButtons = [
            f"{mcpProtocol.prefix}:14", # A
            f"{mcpProtocol.prefix}:15", # B
            f"{mcpProtocol.prefix}:12", # C
            f"{mcpProtocol.prefix}:10", # D
            f"{mcpProtocol.prefix}:8", # E
            f"{mcpProtocol.prefix}:9", # F
            f"{mcpProtocol.prefix}:11", # G
            f"{mcpProtocol.prefix}:13", # H
        ]

        assert(len(limitButtons) == len(motorSets))

        pinSets = [None]*len(limitButtons)
        motorsSet = [None]*len(limitButtons)
        buttonPins = [None]*len(limitButtons)
        limitsSet = [None]*len(limitButtons)
        axisSet = [None]*len(limitButtons) # The gantrys should be on one axis

        for i in range(len(limitButtons)):
            pinSets[i] = (
                controller.registerPin(motorSets[i][0], GenericPin.OUTPUT),
                controller.registerPin(motorSets[i][1], GenericPin.OUTPUT),
                controller.registerPin(motorSets[i][2], GenericPin.OUTPUT),
            )

            motorsSet[i] = GenericStepper(*(pinSets[i]))

            buttonPins[i] = controller.registerPin(limitButtons[i], GenericPin.INPUT_PULL_UP)

            limitsSet[i] = GenericLimit(buttonPins[i])

            axisSet[i] = GenericAxis(limitsSet[i], motorsSet[i])

        print("GPIO initalized")
    return (motorSets, pinSets, motorsSet, buttonPins, limitsSet, axisSet)


async def pushFunction(outboundQ, gpio):
    motorSets = gpio[0]
    pinSets = gpio[1]
    motorsSet = gpio[2]
    buttonPins = gpio[3]
    limitsSet = gpio[4]
    axisSet = gpio[5]

    lastStates = [None]*len(limitsSet)
    lastEnabled = [None]*len(motorSets)

    try:
        while True:
            for i in range(len(limitsSet)):
                lbl = chr(i + ord('A'))

                v = limitsSet[i].isPressed()
                if v != lastStates[i]:
                    lastStates[i] = v
                    await outboundQ.put(f"L {lbl} {'+' if v else '-'}")

                e = motorsSet[i].isEnabled()
                if e != lastEnabled[i]:
                    lastEnabled[i] = e
                    await outboundQ.put(f"ENBL {lbl} {'+' if v else '-'}")
            
            await asyncio.sleep(.25)
    except asyncio.CancelledError:
        print("PUSH CANCEL")
    finally:
        pass
    return

async def gpioHandler(inboundQ, outboundQ, gpio):
    motorSets = gpio[0]
    pinSets = gpio[1]
    motorsSet = gpio[2]
    buttonPins = gpio[3]
    limitsSet = gpio[4]
    axisSet = gpio[5]

    try:
        while True:
            t = await inboundQ.get()
            tokens = t.split(" ")

            # await outboundQ.put(f"L A {'+' if limit.isPressed() else '-'}")
            # print(t)

            if(tokens[0] == 'ECHO'):
                m = t[t.find(' ')+1:]
                print(f"Echoing t: {m}" )
                await outboundQ.put(t)
            elif(tokens[0] == 'ENBL'):
                motor = motorsSet[getMotorId(tokens[1])]
                motor.enable(GenericStepper.ENABLE if tokens[2] == '+' else GenericStepper.DISABLE)
                print(f"Processed ENBL: {t}")
            elif(tokens[0] == 'HOME'):
                axis = axisSet[getMotorId(tokens[1])]
                #THIS is bad b/c its not interruptable
                #FIXME
                await axis.home(GenericStepper.DIRECTION_REVERSE)
            elif(tokens[0] == 'M'):
                motor = motorsSet[getMotorId(tokens[1])]
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