# This is the master server

from xmlrpc.server import SimpleXMLRPCServer
import logging


# Example function
def return_square(num):
	return num*num

# Set up logging
def run_server(host, port):
	logging.basicConfig(level=logging.DEBUG)

	server = SimpleXMLRPCServer((host, port), logRequests=True)
		
	server.register_function(return_square)

	try:
		print('Use Control-C to exit')
		server.serve_forever()
	except KeyboardInterrupt:
		print('Exiting')
		
