import asyncio
import websockets
import sys
from time import sleep

DEFAULT_PORT = "20462"
DEFAULT_HOST = "192.168.0.199"

FALLBACK_PORT = DEFAULT_PORT
FALLBACK_HOST = "localhost"

def launchServer( connectionHandler, host=DEFAULT_HOST, port=DEFAULT_PORT):
    
    print(f"Starting Server at {host}:{port}")

    # log host and port to a file for the client
    with open("connectionData.js", "w") as f:
        print(f"myHost=\"{host}\";", file=f)
        print(f"myPort=\"{port}\";", file=f)

    server = websockets.server.serve(connectionHandler, host, port)
    # print(f"Server started?")
    return server