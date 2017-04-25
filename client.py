import asyncio
import websockets
import time
import base64

class webApp(object):
    def __init__(self, socket, file,
                 cSend = 0, cRecieve = 0, cEOF = 0, sSend = 0, sRecieve = 0,
                 server = "ws://localhost:"):
        self.socket = socket
        self.file = file
        self.server = server

    async def getF(self):
        '''
        goes out to find the file requested
        
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
        #opens the socket
        async with websockets.connect(self.server + str(self.socket), max_size = None) as websocket:
            self.cSend = time.time()
            print("sending name to server")
            await websocket.send(self.file)
            print("recieving server's send time")
            self.sSend = float(await websocket.recv())
            print("getting clinet recieve time")
            self.cRecieve = time.time()
            print("recieving file from server")
            F = await websocket.recv()
            
            #Checks if the file was found by the cache
            if F != "No File":
                #writes if file was found
                with open("./client/" + self.file, 'wb+') as webFile:
                    print("file is open")
                    #decodes file and writes
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
    
        name = input("What's the file name? ")
        print("making object")
        #makes the application object to get file
        stuff = webApp(socket = 8765, file = name)
        print("getF()")
        #gets file from web
        await stuff.getF()
        #prints confirmation of file
        print("> {}".format(stuff.file))

        #prints RTT
        await stuff.printRTT()



#main code
#asyncio used for thread processing
#runs the main function call for the basic program
loop = asyncio.get_event_loop()
loop.run_until_complete(hello())
loop.close()
