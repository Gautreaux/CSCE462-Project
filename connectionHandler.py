
import asyncio
import websockets

#utilizes lambda capture to pass variables into connection handler
def buildConnectionHandler(signaledQueue):

    async def connectionHandler(websocket, path):
        try:
            print("New connection received.")
            async for message in websocket:
                print(f"MSG: {message}")
                signaledQueue.put(message)

            #this part is executed after the websocket is closed by the client
            #if the socket is closed by the server (i.e. ctrl-c) this is not executed
            print("Connection lost.")
        except websockets.exceptions.ConnectionClosedError:
            #when the websocket is closed in some abnormal fashion
            print("Connection closed abnormally.")
    return connectionHandler
