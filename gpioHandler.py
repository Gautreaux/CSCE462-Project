
import asyncio

async def gpioHandler(inboundQ, outboundQ):
    print("GPIO inialiized")
    try:
        while True:
            t = await inboundQ.get()
            print(f"Echoing t: {t}" )
            await outboundQ.put(t)
    except asyncio.CancelledError:
        print("GPIO CANCEL")
    finally:
        #TODO - gpio cleanup
        pass
    return