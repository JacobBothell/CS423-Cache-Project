import asyncio
import websockets
import time
import base64

class webApp(object):
    def __init__(self, socket, file,
                 cSend = 0, cRecieve = 0, cEOF = 0, sSend = 0, sRecieve = 0):
        self.socket = socket
        self.file = file

    async def getF(self):
        '''
        General Algorithm:
            open file
            mark client send time
            ask cache for file
            recieve the server's send time
            mark client recieve time
            recieve the file
            recieve the server's recieve time
            mark client EOF time
        '''
        async with websockets.connect('ws://localhost:' + str(self.socket), max_size = None) as websocket:
            self.cSend = time.time()
            print("sending name to server")
            await websocket.send(self.file)
            print("recieving server's send time")
            self.sSend = float(await websocket.recv())
            print("getting clinet recieve time")
            self.cRecieve = time.time()
            print("recieving file from server")
            F = await websocket.recv()
            if F != "No File":
                with open("./client/" + self.file, 'wb+') as webFile:
                    print("file is open")
                    webFile.write(base64.b64decode(F))
                    webFile.close()
            else:
                print(F)
            self.cEOF = time.time()
            print("recieving server's recieve time")
            self.sRecieve = float(await websocket.recv())
            #close socket
            websocket.close()


    async def printRTT(self):
        '''
        Prints the RTT for the last file transfer
        '''
        
        print("Round Trip Time " + str(self.cRecieve - self.cSend) + " seconds")
        

async def hello():
    
        name = input("What's your name? ")
        print("making object")
        stuff = webApp(socket = 8765, file = name)
        print("getF()")
        await stuff.getF()
        print("> {}".format(stuff.file))

        await stuff.printRTT()

loop = asyncio.get_event_loop()
loop.run_until_complete(hello())
loop.close()
