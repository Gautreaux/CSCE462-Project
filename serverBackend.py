import asyncio
import websockets
import sys
from time import sleep

DEFAULT_PORT = "20462"
DEFAULT_HOST = "192.168.0.199"

def launchServer(connectionHandler, host=DEFAULT_HOST, port=DEFAULT_PORT):
    
    print(f"Starting Server at {host}:{port}")

    #TODO - log host and port to a file for the client

    server = websockets.serve(connectionHandler, host, port)
    try:
        asyncio.get_event_loop().run_until_complete(server)
        return True
    except OSError as e:
        return False