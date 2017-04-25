import asyncio
import websockets
import time
import base64

#TODO: move code into this container
class webApp(object):
    def __init__(self, socket,
                 sSend = 0, sRecieve = 0,
                 name = "", server = "//bothellj.ddns.net:8080"):
        self.socket = socket
        self.server = server

#TODO: make this a smaller function
async def hello(websocket, path):
    stuff = webApp(socket = websocket)
    stuff.name = await websocket.recv()
    stuff.sRecieve = time.time()
    print("< {}".format(stuff.name))

    print("sending server's send time")
    await websocket.send(str(time.time()))
    print("sending file")
    #looks for file in cache
    #   gets data from server otherwise
    try:
        with open("./cache/" + str(stuff.name), 'rb') as file:
            print("file open")
            #encoding for data transfer
            await websocket.send(base64.b64encode(file.read()))
    except FileNotFoundError:
    #TODO: this dosen't work yet...
        #supposed to go back to server and get files
        print("opening server socket")
        async with websockets.connect(stuff.server, max_size = None, klass = "HTTP") as serverSock:
            print("requesting file from server")
            await serverSock.send("./CS423/" + stuff.name)
            F = await serverSock.recv()
            print(F)
            '''
            with open("./cache/" + self.name, 'wb+') as webFile:
                print("file is open")
                webFile.write(base64.b64decode(F))
                webFile.close()
            '''
                    
    #print("> {}".format(greeting))
    print("sending server's recieve time")
    await websocket.send(str(stuff.sRecieve))


#main portion of the script
start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
