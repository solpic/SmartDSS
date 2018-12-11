from xmlrpc.client import *
    
proxy = None

# Init proxy
def init_proxy():
    global proxy
    proxy = ServerProxy('http://localhost:9000')

def get_proxy():
    if proxy==None:
        init_proxy()
    return proxy



# Example
# proxy = get_proxy('http://localhost:9000')
# print(proxy.return_square(10)) // prints 100
# blah
