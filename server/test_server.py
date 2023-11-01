import Pyro4


@Pyro4.expose
class HelloWorld:
    def hello(self):
        return 'Hello World'


daemon = Pyro4.Daemon()

uri = daemon.register(HelloWorld)
names_server = Pyro4.locateNS()
names_server.register('obj', uri)

daemon.requestLoop()
