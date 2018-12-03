# This is the master server

from xmlrpc.server import SimpleXMLRPCServer
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

server = SimpleXMLRPCServer(('localhost', 9000), logRequests=True)

# Example function

def return_square(num):
	return num*num
	
server.register_function(return_square)

try:
    print('Use Control-C to exit')
    server.serve_forever()
except KeyboardInterrupt:
    print('Exiting')
    
