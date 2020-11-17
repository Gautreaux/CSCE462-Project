
import asyncio

from genericStepper import GenericStepper

class GenericAxis():
    def __init__(self, limitSwitch, motor, motor2=None):
        self.limit = limitSwitch
        self.motor = motor
        self.motor2 = motor2

    # move to the home position
    #   should be along the motor negative direction
    async def home(self):
        while (self.limit.isPressed() is False):
            await self.motor.step(GenericStepper.DIRECTION_REVERSE)
            if(self.motor2 is not None):
                await self.motor2.step(GenericStepper.DIRECTION_REVERSE)

        self.motor.setHome()
        if(self.motor2 is not None):
            self.motor2.setHome()

    #TODO - move some distance
    def moveMM(self):
        raise NotImplementedError