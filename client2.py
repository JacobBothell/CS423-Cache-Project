import os
import http.client
import time

#designed to go out to the web and fetch an object
# actually goes through a local cache server first
class myClient:

    def __init__(self, server):
        self.server = server

        #these are used for measuring
        # timing in the network
        self.t_1 = 0
        self.t_2 = 0
        self.t_3 = 0
        self.t_4 = 0

    def clientStats(self, file):
        #this prints out the stats to show that
        # the application works and some features about it

        #this proves that our time collection methods are
        # in the correct places and are capturing correct values
        #  will be close but not perfectly the same
        RTT = self.t_4 - self.t_1
        RTT_2 = (self.t_2 - self.t_1) + (self.t_3 - self.t_2) + (self.t_4 - self.t_3)
        print("RTT Conformation: " + str(RTT) + " = " + str(RTT_2))

        #this prints the throughput of the network
        # with reguards to the file sent
        throughputSize = os.stat("./client/" + file).st_size
        throughputTime = self.t_4 - self.t_1
        throughput = throughputSize / throughputTime
        print("Throughput of network: " + str(throughput) + "B/s")

    def getF(self, file):
        #all times in this method are epoch time
        # it is assumed that the machines (client and cache)
        # have correct time (time zone will not matter?)
        
        print("Opening socket")
        client = http.client.HTTPConnection(self.server)
        #cache does not need to use custom headers
        # so a standard request can be used
        # otherwise use .putrequest, .putheader, .endheader
        
        print("Sending request")
        #time of req sending
        self.t_1 = time.time()
        #puts together the request
        client.request("GET", "/" + file)
        
        #recieves the response
        resp = client.getresponse()
        print("opening file")
        with open("./client/" + file, "wb+") as oFile:
            print("Writing response to file")
            print(resp.status, resp.reason)
            #these are the server response times
            self.t_2 = float(resp.getheader("Server-Recieve-Time"))
            self.t_3 = float(resp.getheader("Server-Send-Time"))
            oFile.write(resp.read())
            
        #cleanup
            oFile.close()
            resp.close()
        #get finish time
        self.t_4 = time.time()
        client.close()
        self.clientStats(file)
        return

#Main Program creates client object
# then gets file from cache on local machine
client = myClient("localhost")
file = input("What file would you like: ")
client.getF("16A.jpg")

"""
OLD CODE

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
"""
