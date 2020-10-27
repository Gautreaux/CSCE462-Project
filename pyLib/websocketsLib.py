
from websocketsADT import WebsocketsServer

import asyncio
import threading
from time import sleep
import websockets

#see websocketsADT
class WebsocketsServer462(WebsocketsServer):
    DEFAULT_HOST = '192.168.0.199'
    DEFAULT_PORT = '20462'

    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        # print(f"Constructor called with {host}:{port}")
        self.host = host
        self.port = port
        self.status = 'not_started'
        self.thread_thread = None
        self.thread_server = None
        self.thread_loop = None

    def __del__(self):
        self.close()

    def __str__(self):
        return f"462 Websockets server {self.status} on {self.host}:{self.port}"

    def start(self):
       
        
        self.thread_loop = asyncio.new_event_loop()
        self.thread_server = websockets.serve(self.on_connection, self.host, self.port)
        #TODO - bind checking?
        self.thread_loop.run_until_complete(self.thread_server)
        self.status = 'server_running' 
        
        t = threading.Thread(target=self.thread_loop.run_forever)
        t.start()
        self.thread_thread = t
    
    def close(self):
        if self.thread_server is None:
            return
        
        #attempt normal close
        try:
            self.thread_server.ws_server.close()
        except:
            print("WS close failed")
            pass

        try:
            self.thread_loop.stop()
            self.thread_loop.close()
        except:
            print("Async loop close failed")
            pass

        #wait 2 seconds to join
        self.thread_thread.join(2)

        if self.thread_thread.is_alive():
            #force kill
            self.thread_thread.stop()

        self.thread_thread = None
        self.thread_loop = None
        self.thread_server = None
        self.status = 'closed'


    async def on_connection(self, websocket, path):
        try:
            async for message in websocket:
                print(f"MSG: {message}")
            print("Websocket closed normally")
        except websockets.exceptions.ConnectionClosedError:
            print("Websocket closed abnormally")



if __name__ == '__main__':
    w = WebsocketsServer462()
    print(w)
    w.start()
    print(w)
    sleep(5)
    print("Beginning nominal close procedure")
    w.close()
    print(__name__)