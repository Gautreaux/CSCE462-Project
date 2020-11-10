
import asyncio
import websockets

#utilizes lambda capture to pass variables into connection handler
def buildConnectionHandler(inboundQ, outboundQ):

    # async def consumer_handler(websocket, path):
    #     print("Consumer started")
    #     try:
    #         print("New connection received.")
    #         async for message in websocket:
    #             print(f"MSG: {message}")
    #             inboundQ.put(message)

    #         #this part is executed after the websocket is closed by the client
    #         #if the socket is closed by the server (i.e. ctrl-c) this is not executed
    #         print("Connection lost.")
    #     except websockets.exceptions.ConnectionClosedError:
    #         #when the websocket is closed in some abnormal fashion
    #         print("Connection closed abnormally.")

    # async def producer_handler(websocket, path):
    #     print("Producer started")
    #     while True:

    #         from threading import Event
    #         # wait forever for an event that will never come
    #         Event().wait()

    #         # t = outboundQ.get()
    #         # print(f"Sending {t}")
    #         # websocket.send(t)
    pass

async def consumer(message):
    print(message)

async def producer():
    await asyncio.sleep(2)
    return "Apple"

async def producer_handler(websocket, path):
    while True:
        message = await producer()
        await websocket.send(message)

async def consumer_handler(websocket, path):
    try:
        async for message in websocket:
            await consumer(message)
        #this part is executed after the websocket is closed by the client
        #if the socket is closed by the server (i.e. ctrl-c) this is not executed
        print("Connection closed by client.")
    except websockets.exceptions.ConnectionClosedError:
        #when the websocket is closed in some abnormal fashion
        print("Connection closed abnormally.")

async def handler(websocket, path):
    print("Generic handler started")
    consumer_task = asyncio.ensure_future(
        consumer_handler(websocket, path))
    producer_task = asyncio.ensure_future(
        producer_handler(websocket, path))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    print("Generic handler exiting")
    for task in pending:
        task.cancel()

    # return handler
