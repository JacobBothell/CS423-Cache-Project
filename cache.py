import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer
import http.client
import time

#This class goes back to an origin server to fill
# a cache with data that was requested
class myClient:
    def __init__(self, server):
        self.server = server
        
    def getF(self, file):
        print("Opening socket")
        client = http.client.HTTPConnection(self.server)
        #cache does not need to use custom headers
        # so a standard request can be used
        # otherwise use .putrequest, .putheader, .endheader
        print("Sending request")
        #puts together request
        client.request("GET", "/CS423" + file)
        #recieves the response
        resp = client.getresponse()
        print("opening file")
        with open("./cache/" + file, "wb+") as file:
            print("Writing response to file")
            print(resp.status)
            file.write(resp.read())
        #cleanup
            resp.close()
        client.close()
        return

#This class will handles any incoming request
# that asks the cache for data
# specifically designed to transfer images
class myHandler(BaseHTTPRequestHandler):
	
    #Handler for the GET requests
    def do_GET(self):
        print("GET Recieved")
        #recieved time stamp
        Stime = time.time()
        #putting together the response headers
        self.send_response(200)
        self.send_header('Content-type','image/png')
        self.send_header('Server-Recieve-Time', Stime)
        #finishes the headers
        self.end_headers()
        #Send the response
        
        #tries to send response but if file fails to open
        # goes to origin server
        try:
            with open("./cache" + self.path, "rb") as file:
                print("sending file to client")
                #sends file to client
                self.wfile.write(file.read())
                print("file finished")
        except FileNotFoundError:
            print("going back to origin server")
            #go back to origin Server
            client = myClient("bothellj.ddns.net:8080")
            client.getF(self.path)
            with open("./cache" + self.path, "rb") as file:
                print("sending file to client")
                #sends file to client
                self.wfile.write(file.read())
        return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = http.server.HTTPServer(('localhost', 80), myHandler)
	print ('Started httpserver on port 80')
	
	#Wait forever for incoming http requests
	server.serve_forever()

except KeyboardInterrupt:
	print ('^C received, shutting down the web server')
	server.socket.close()

'''
OLD CODE

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
        async with websockets.connect(stuff.server, max_size = None) as serverSock:
            print("requesting file from server")
            await serverSock.send(stuff.name)
            F = await serverSock.recv()
            print(F)
            """
            with open("./cache/" + self.name, 'wb+') as webFile:
                print("file is open")
                webFile.write(base64.b64decode(F))
                webFile.close()
            """
                    
    #print("> {}".format(greeting))
    print("sending server's recieve time")
    await websocket.send(str(stuff.sRecieve))


#main portion of the script
start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
'''
