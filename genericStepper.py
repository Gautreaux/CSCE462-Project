
import asyncio

from gpioPin import GenericPin

class GenericStepper:
    MODE_COAST = 0
    MODE_BREAK = 1

    DIRECTION_STANDARD = 1
    DIRECTION_REVERSE = -1

    DISABLE = 0
    ENABLE = 1

    def __init__(self, enablePin, stepPin, dirPin, 
            breakMode=MODE_BREAK, 
            #direction=DIRECTION_STANDARD,
            enableState=ENABLE):
        self.enb = enablePin
        self.stp = stepPin
        self.dir = dirPin
        self.enableState = enableState
        self.breakMode = breakMode
        self.homed = False
        self.steps = 0

        self.enable(enableState)

    # perform one single step
    async def step(self, direction):
        if(self.enableState is GenericStepper.DISABLE):
            self.enable(GenericStepper.ENABLE)
        self.setDir(direction)
        self.steps += 1 if direction is GenericStepper.DIRECTION_STANDARD else -1
        self.stp.setValue(GenericPin.HIGH)
        await asyncio.sleep(.001) # 1ms sleep to stabilize
        self.stp.setValue(GenericPin.LOW)
        if(self.breakMode is GenericStepper.MODE_COAST):
            self.enable(GenericStepper.DISABLE)

    def enable(self, state):
        self.enb.setValue(GenericPin.LOW if state is GenericStepper.ENABLE else GenericPin.HIGH)
        self.enableState = state

    def setDir(self, direction):
        #TODO - could be lazy evaluate in case pin setValue takes time
        self.dir.setValue(GenericPin.LOW if direction is GenericStepper.DIRECTION_STANDARD else GenericPin.HIGH)

    def setHome(self):
        self.homed = False
        self.steps = 0

    #TODO - include speed parameter?
    async def RotateDegrees(self, direction, degrees):
        await self.RotateSteps(self, direction, int(degrees*(5/9)))

    #TODO - include speed parameter?
    async def RotateSteps(self, direction, steps):
        for i in range(steps):
            await self.step(direction)