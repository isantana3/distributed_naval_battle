#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

player = '1'
while True:
    message = socket.recv()
    msg = bytes.decode(message)
    print(f"Received request: {message}")

    if msg != player:
        response = 'not your turn'
    else:
        response = f'player {player} turn'
        if player == '1':
            player = '2'
        else:
            player = '1'
    time.sleep(2)
    socket.send(response.encode())
