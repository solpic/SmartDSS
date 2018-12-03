from xmlrpc.client import *

proxy = ServerProxy('http://localhost:9000')
print(proxy.return_square(10))
