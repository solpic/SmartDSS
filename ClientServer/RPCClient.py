from xmlrpc.client import *

def get_proxy(host):
	if(proxy!=None)
		proxy = ServerProxy(host)
	return proxy
	
proxy = None


# Example
# proxy = get_proxy('http://localhost:9000')
# print(proxy.return_square(10)) // prints 100
# blah
