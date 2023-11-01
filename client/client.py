import time
import sys
import zmq
from colorama import Fore, init
from decouple import config

init()

player = f'p{sys.argv[1]}'
opponent = 'p1' if player == 'p2' else 'p2'
context = zmq.Context()

host = config('HOST')
port = config('PORT')

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect(f'tcp://{host}:{port}')


class RPCClient:
    def __init__(self) -> None:
        self.msg = None
        self.endgame = False

    def read_message(self):
        message = socket.recv()
        self.msg = bytes.decode(message)
        if self.msg == 'wait':
            self.wait_turn()
        elif self.msg == 'game over':
            self.endgame = True
        return self.msg

    def send_message(self, message=''):
        msg = f'{player}-{message}'
        socket.send(msg.encode())

    def wait_turn(self):
        while self.msg == 'wait':
            print('waiting', end='\r')
            self.send_message()
            message = socket.recv()
            self.msg = bytes.decode(message)
            time.sleep(0.5)

    def request_coordinates(self):
        global player
        print(Fore.RESET + f"Requesting shot coordinates from player {player}\n")

        y = None
        x = None
        while True:
            row_letter = input(Fore.RESET + "Enter the letter of the row:")
            if len(row_letter) != 1:
                print(Fore.RESET + "You must enter only 1 letter\n")
                continue

            y = ord(row_letter.upper()) - 65

            if y >= 0 and y <= 10:
                break
            else:
                print("Invalid row\n")

        while True:
            try:
                x = int(input(Fore.RESET + "Enter the column number: "))
                if x >= 0 and x <= 10:
                    x = x - 1
                    break
                else:
                    print(Fore.RESET + "Invalid column\n")
            except:
                print(Fore.RESET + "Enter a valid number.\n")

        return f'{x},{y}'


client = RPCClient()
while True:
    client.send_message()
    message = client.read_message()
    print(message, end='\r')
    if message == 'waiting second player ...':
        continue
    print('\n')
    while True:
        client.send_message()  # Mensagem para descobrir se é a vez do jogador
        print(
            client.read_message()
        )  # resposta cai no loop até que seja a vez do jogador
        if client.endgame:
            break
        coordinates = client.request_coordinates()
        client.send_message(coordinates)  # envia jogada
        print(client.read_message())  # recebe feedback
        if client.endgame:
            break
    break
