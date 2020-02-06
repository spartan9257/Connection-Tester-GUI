from http.server import HTTPServer, BaseHTTPRequestHandler
from os import path
import cgi, csv, logging, socketserver, http.server


#To connect to the server localhost:8080
#Or ip_address:8080
PORT = 8080




#Class that handles HTTP GET and POST requests
class ServerHandler(http.server.SimpleHTTPRequestHandler):

    #Sends the index.html file in response to HTTP GET
    def do_GET(self):
        logging.error(self.headers)
        http.server.SimpleHTTPRequestHandler.do_GET(self)

#initializes the server
Handler = ServerHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()
