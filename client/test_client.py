import Pyro4


names_server = Pyro4.locateNS()
uri = names_server.lookup('obj')

obj = Pyro4.Proxy(uri)

print(obj.hello())
