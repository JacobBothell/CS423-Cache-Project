import asyncio
import websockets
import time

class webApp(object):
    def __init__(self, socket,
                 cSend = 0, cRecieve = 0, sSend = 0, sRecieve = 0,
                 name = ""):
        self.socket = socket

async def hello(websocket, path):
    stuff = webApp(socket = websocket)
    recv = await websocket.recv()
    stuff.sRecieve = time.time()
    stuff.name = recv
    print("< {}".format(stuff.name))

    greeting = "Hello {}!".format(stuff.name)
    print("sending time")
    await websocket.send(str(stuff.sRecieve))
    print("sending greeting")
    await websocket.send(greeting)
    print("> {}".format(greeting))


#main portion of the script
start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
