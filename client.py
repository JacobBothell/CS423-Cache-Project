import asyncio
import websockets
import time

class webApp(object):
    def __init__(self, socket,
                 cSend = 0, cRecieve = 0, sSend = 0, sRecieve = 0,
                 name = "jacob"):
        self.socket = socket
        self.name = name
        

async def hello():
    async with websockets.connect('ws://localhost:8765') as websocket:
    
        name = input("What's your name? ")
        print("making object")
        stuff = webApp(socket = websocket, cSend = time.time())
        print("sending")
        await websocket.send(stuff.name)
        print("> {}".format(name))
        
        stuff.sRecieve = await websocket.recv()
        print("getting time")
        stuff.cRecieve = time.time()
        print("time {}".format(stuff.sRecieve))
        greeting = await websocket.recv()
        print("< {}".format(greeting))

asyncio.get_event_loop().run_until_complete(hello())
