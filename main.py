
import asyncio
import threading
from time import sleep
from queue import Queue


from connectionHandler import buildConnectionHandler
from gpioHandler import gpioHandler
from serverBackend import launchServer
from synchronization import *

from queue import SimpleQueue


if __name__ == "__main__":
    multiSema = MultiSemaphore()
    exitEvent = SignaledEvent(multiSema)
    instructionQueue = SignaledQueue(multiSema)

    producerQueue = SimpleQueue()

    gpioThread = threading.Thread(target=gpioHandler, 
        args=[multiSema, exitEvent, instructionQueue, producerQueue])
    gpioThread.start()

    while(True):
        serverRes = launchServer(buildConnectionHandler(instructionQueue, producerQueue))
        if serverRes is True:
            #server started sucessfully,
            print("Server started sucessfully")
            break
        else:
            print("Server failed to start")
            sleep(5)
    

    #last bit
    try:
        asyncio.get_event_loop().run_forever()
        #any code down here would not be reachable until the server closes its socket
        # under normal circumstances, this means this code is unreachable  
    except KeyboardInterrupt:
        print("Keyboard interrupt caught, exiting.")
        exitEvent.trigger()