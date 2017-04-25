import asyncio
import websockets
import time

class webApp(object):
    def __init__(self, socket,
                 sSend = 0, sRecieve = 0,
                 name = ""):
        self.socket = socket

async def hello(websocket, path):
    stuff = webApp(socket = websocket)
    stuff.name = await websocket.recv()
    stuff.sRecieve = time.time()
    print("< {}".format(stuff.name))

    greeting = "Hello {}!".format(stuff.name)
    print("sending server's send time")
    await websocket.send(str(time.time()))
    print("sending file")
    await websocket.send(greeting)
    print("> {}".format(greeting))
    print("sending server's recieve time")
    await websocket.send(str(stuff.sRecieve))


#main portion of the script
start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
