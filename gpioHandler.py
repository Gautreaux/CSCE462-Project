
from time import sleep

def gpioHandler(multiSema, exitEvent, instructionQ, producerQ):
    # TODO - gpio setup

    print("GPIO setup complete")

    while(True):
        k = multiSema.acquire()
        print(k)
        if k == exitEvent.key:
            print("GPIO thread exit triggered")
            break

        
        print(f"New instruction: {instructionQ.get()}")
        producerQ.put("GPIO THINGY")
        print(f"Done with put")
    
    #called when the exit event is triggered
    print("GPIO exit completed")