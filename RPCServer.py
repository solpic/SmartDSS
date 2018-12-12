# This is the master server

from xmlrpc.server import SimpleXMLRPCServer
from DocumentDB import *
import logging

# Example function
def return_square(num):
    return num*num

def register_all_functions(server):
    #import Users1
    db = DocumentDBServer()
    server.register_function(return_square)
    server.register_instance(DocumentDBServer())
    #from Users1 import Users
    #server.register_instance(Users(db.conn, db.c))
    
    
# Set up logging
def run_server(host, port):
    logging.basicConfig(level=logging.DEBUG)

    server = SimpleXMLRPCServer((host, port), logRequests=True, allow_none=True)
        
    register_all_functions(server)

    try:
        print('Use Control-C to exit')
        server.serve_forever()
    except KeyboardInterrupt:
        print('Exiting')
        
        
if __name__ == '__main__':
    #On AWS INSTANCE
    run_server("0.0.0.0", 80)
