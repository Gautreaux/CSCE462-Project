import asyncio
import websockets
import sys
from signal import SIGINT, SIGTERM
from time import sleep

DEFAULT_PORT = "20462"
DEFAULT_HOST = "192.168.0.199"


async def connectionHandler(websocket, path):
    try:
        print("New connection received.")
        async for message in websocket:
            print(f"MSG: {message}")

        #this part is executed after the websocket is closed by the client
        #if the socket is closed by the server (i.e. ctrl-c) this is not executed
        print("Connection lost.")
    except websockets.exceptions.ConnectionClosedError:
        #when the websocket is closed in some abnormal fashion
        print("Connection closed abnormally.")

#if the python module has been launched as the main one
if __name__ == "__main__":
    #first, we allow for command line arguments formatted such:
    #   server.py <hostname> <port> <motor-interface-value>
    #   where hostname and port are optional
    try:
        port = sys.argv[2]
    except IndexError:
        #The user did not provide an port argument
        port = DEFAULT_PORT

    try:
        host = sys.argv[1]
    except IndexError:
        host = DEFAULT_HOST

    print(f"Starting Server at {host}:{port}")

    #This outer while loop "solves" the race condition.
    #More on this at the end of the file.
    failCtr = 0
    while(True):
        #start the server
        server = websockets.serve(connectionHandler, host, port)

        try:
            #since the connection is asynchronous, we need to hold the program until its finished
            # under normal circumstances, this means we wait forever
            asyncio.get_event_loop().run_until_complete(server)
            print("server started successfully.")
            failCtr = -1
            asyncio.get_event_loop().run_forever()
            #any code down here would not be reachable until the server closes its socket
            # under normal circumstances, this means this code is unreachable

        except KeyboardInterrupt:
            #the interrupt was fired (ctrl-c), time to exit
            #note, the interrupt wont happen till the next async event happens
            print("Exiting via KeyboardInterrupt")
            exit(-1)
        except OSError as e:
            failCtr+=1
            if(failCtr % 10 == 0):
                print("The server startup failed too many times")
                print("\tThis may be a result of too many packages slowing down the loading of the network interface.")
                print(f"\t{e}")
            else:
                sleep(5)

#About the race condition:
#The pi has to load packages that give it the ability to accept incoming connections
#These packages take time to load (both on the pi and within the actual wifi chip)
#In other threads, the pi continues loading other packages
#One of these other packages is the rc.local script
#Which launches this python program in the background
#It is a frequent occurrence that rc.local happens before the wifi fully loads
#Which causes a bind failure and an exception

#In the long term, it would be better to register the server as a service that is dependent on wifi
#Thus, the kernel will not launch it until the wifi is ready, preventing error
#Futhermore, in the case of a crash, the kernel should be able to relaunch the program