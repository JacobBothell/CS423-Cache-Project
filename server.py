import asyncio
import websockets
import time
import base64

class webApp(object):
    def __init__(self, socket,
                 sSend = 0, sRecieve = 0,
                 name = ""):
        self.socket = socket
        self.server = server

async def hello(websocket, path):
    stuff = webApp(socket = websocket)
    stuff.name = await websocket.recv()
    print("sending file")
    try:
        with open("./" + str(stuff.name), 'rb') as file:
            print("file open")
            await websocket.send(base64.b64encode(file.read()))
    except FileNotFoundError:
        await websocket.send("No File")


#main portion of the script
start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
