from xmlrpc.client import *

def get_proxy(host):
	return ServerProxy(host)

# Example
# proxy = get_proxy('http://localhost:9000')
# print(proxy.return_square(10)) // prints 100
