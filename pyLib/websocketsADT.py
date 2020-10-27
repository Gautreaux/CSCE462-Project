
from abc import ABC, abstractmethod
import websockets

class WebsocketsServer(ABC):

    def __int__(self, *args, **kwargs):
        pass
        
    def __del__(self):
        pass

    def __str__(self):
        print(str(WebsocketsServer))     

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    async def on_connection(self, websocket, path):
        try:
            async for message in websocket:
                print(f"MSG: {message}")
            print("Websocket closed normally")
        except websockets.exceptions.ConnectionClosedError:
            print("Websocket closed abnormally")

if __name__ == '__main__':
    print(__name__)