
from time import sleep

def gpioHandler(multiSema, exitEvent, instructionQ):
    # TODO - gpio setup

    print("GPIO setup complete")

    while(True):
        k = multiSema.acquire()
        print(k)
        if k == exitEvent.key:
            print("GPIO thread exit triggered")
            break

        print(f"New instruction: {instructionQ.get()}")
    
    #called when the exit even is triggered
    print("GPIO exit completed")