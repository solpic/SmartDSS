# This is the master server

from xmlrpc.server import SimpleXMLRPCServer
from DocumentDB import *
import logging


# Example function
def return_square(num):
    return num*num

def register_all_functions(server):
    server.register_function(return_square)
    server.register_instance(doc_db)
    
    
# Set up logging
def run_server(host, port):
    logging.basicConfig(level=logging.DEBUG)

    server = SimpleXMLRPCServer((host, port), logRequests=True)
        
    register_all_functions(server)

    try:
        print('Use Control-C to exit')
        server.serve_forever()
    except KeyboardInterrupt:
        print('Exiting')
        
        
def main():
    run_server("localhost", 9000)

if __name__ == '__main__':
    main()
