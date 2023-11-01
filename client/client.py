import time
import Pyro4


names_server = Pyro4.locateNS()

server_uri = names_server.lookup('server')
server = Pyro4.Proxy(server_uri)

test_uri = names_server.lookup('test')
test = Pyro4.Proxy(test_uri)

# board_uri = names_server.lookup('board')
# board = Pyro4.Proxy(board_uri)


class Client:
    def show_menu(self):
        print(server.show_menu())

    def test(self):
        test.add('iago')
        print(test.show_players())
        time.sleep(10)


Client().test()
