#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import sys
import zmq

# if sys.argv[1] == '1':
# 	port = PORT1
# elif sys.argv[1] == '2':
# 	port = PORT2
# else:
# 	print("Wrong arguments")
# 	exit()

port = sys.argv[1]
context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

#  Do 10 requests, waiting each time for a response
for request in range(10):
    print(f"Sending request {request} … {port}")
    socket.send(port.encode())

    #  Get the reply.
    message = socket.recv()
    print(f"Received reply {request} [ {message} ]")
