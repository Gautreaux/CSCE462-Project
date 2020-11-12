
import asyncio


from connectionHandler import buildConnectionHandler
from gpioHandler import gpioHandler
from serverBackend import *
from util import *


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()

        inboundQ = asyncio.Queue()
        outboundQ = asyncio.Queue()

        gpio_coro = gpioHandler(inboundQ, outboundQ)

        server_coro = launchServer(buildConnectionHandler(inboundQ, outboundQ),
                host = DEFAULT_HOST if isRaspi() else FALLBACK_HOST,
                port = DEFAULT_PORT if isRaspi() else FALLBACK_PORT)

        # Kind of want one to cancel the other if it ends but whatever
        loop.run_until_complete(server_coro)
        loop.run_until_complete(gpio_coro)
        loop.run_forever()

        #any code down here would not be reachable until the server closes its socket
        # under normal circumstances, this means this code is unreachable
    except KeyboardInterrupt:
        print("Keyboard interrupt caught, exiting.")
        all_tasks = asyncio.Task.all_tasks(loop=loop)
        for task in all_tasks:
            task.cancel()
        loop.run_until_complete(
            asyncio.gather(
                *all_tasks,
                loop=loop,
                return_exceptions=True # all tasks get a chance to finish
            )
        )
        # raise
    finally:
        loop.close()
    print("Clean shutdown occurred")

    # any final cleanup
    # will not be run until after webserver stops