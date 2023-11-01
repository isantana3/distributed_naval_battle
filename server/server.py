from email.policy import default
from board import *
from colorama import Fore, init
from decouple import config
import time
import zmq

init()

host = config('HOST')
port = config('PORT')

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(f'tcp://{host}:{port}')

total_players = 0
player = 'p1'
winner = ''
loser = ''
end_message = ''


class BattleShipUI:
    def __init__(
        self,
        rows=10,
        columns=10,
        number_of_ships=5,
        first_player_name="P1",
        second_player_name="P2",
    ):
        self.first_board_game = Board(10, 10, 5)
        self.second_board_game = Board(10, 10, 5)
        self.rows = 10
        self.columns = 10

        self.first_player_name = first_player_name
        self.second_player_name = second_player_name

        self.players_data = dict()
        self.auxiliary_y = ""

        self.number_attemps_first_player = 0
        self.number_attemps_second_player = 0
        self.missed_shoot = "-"
        self.successful_shoot = "*"

    def player_opponent(self, player):
        answer = " "
        if player == self.first_player_name:
            answer = self.second_player_name
        else:
            answer = self.first_player_name
        return answer

    def print_horizontal_divider(self):
        horizontal_driver = ''
        for _ in range(self.columns + 1):
            horizontal_driver += "----"
        horizontal_driver += "-\n"
        return horizontal_driver

    def increase_letter(self, letter):
        return chr(ord(letter) + 1)

    def print_numbers_row(self):
        row = Fore.CYAN + "|   "
        for x in range(1, self.columns + 1):
            row += f"| {x} "
        row += Fore.CYAN + "|"
        return row

    def print_board(self, board, show_boats, current_player):
        result = Fore.RESET + f" {current_player}'s Sea: \n"
        result += self.print_numbers_row() + "\n"
        letter = "A"
        for y in range(self.columns):
            result += self.print_horizontal_divider() + "\n"
            result += Fore.CYAN + f"| {letter} "
            for x in range(self.columns):
                cell = board[y][x]
                real_value = cell
                if (
                    not show_boats
                    and real_value != SEA
                    and real_value != self.missed_shoot
                    and real_value != self.successful_shoot
                ):
                    real_value = " "
                if real_value == self.successful_shoot:
                    result += Fore.CYAN + f"| {Fore.RED+real_value} "
                else:
                    result += Fore.CYAN + f"| {Fore.YELLOW+real_value} "
            letter = self.increase_letter(letter)
            result += Fore.CYAN + "|\n"  # Line jump
        result += self.print_horizontal_divider()
        return result

    def print_boards_with_boats(self, board_player1, board_player2):
        board_with_boats = Fore.RESET + " Showing location of both players' ships:\n"
        board_with_boats += self.print_board(
            board_player1, True, self.first_player_name
        )
        board_with_boats += self.print_board(
            board_player2, True, self.second_player_name
        )
        return board_with_boats

    def request_coordinates(self, player):
        print(Fore.RESET + f"Requesting shot coordinates from player {player}\n")

        y = None
        x = None
        while True:
            row_letter = input(Fore.RESET + "Enter the letter of the row:")
            if len(row_letter) != 1:
                print(Fore.RESET + "You must enter only 1 letter\n")
                continue

            self.auxiliary_y = row_letter
            y = ord(row_letter) - 65

            if y >= 0 and y <= 10:
                break
            else:
                print("Invalid row\n")

        while True:
            try:
                x = int(input(Fore.RESET + "Enter the column number: "))
                if y >= 0 and y <= 10:
                    x = x - 1
                    break
                else:
                    print(Fore.RESET + "Invalid column\n")
            except:
                print(Fore.RESET + "Enter a valid number.\n")

        return x, y

    def print_aditional_data(self, x, name_player):
        result = (
            Fore.RED
            + "----------------------------------------------------------------------------------------------------------------------\n"
        )
        result += (
            Fore.RED
            + "                                                    SCORE BOARD                                                       \n"
        )
        result += (
            Fore.WHITE
            + f"{name_player}'s Scoreboard: {self.players_data[name_player]}\n"
        )
        result += (
            Fore.WHITE
            + f"{name_player}'s currently coordinates = column: {self.auxiliary_y}, row: {x+1}\n"
        )
        result += (
            Fore.RED
            + "----------------------------------------------------------------------------------------------------------------------\n"
        )

        return result

    def indicate_win(self, player):
        return Fore.GREEN + f"End of game {player} is the winner"


class RPCServer:
    def read_message(self):
        message = socket.recv()
        return bytes.decode(message)

    def send_message(self, message):
        socket.send(message.encode())

    def wait_players(self):
        global total_players

        while total_players < 2:
            msg = server.read_message()
            msg = msg.split('-')
            if msg[0] == player:
                total_players = 1
                response = 'waiting second player ...'
            else:
                total_players = 2
                response = "let's start"

            server.send_message(response)

    def player_turn(self, msg_player):
        global player
        if msg_player == player:
            return True
        else:
            server.send_message('wait')

    def att_turn(self):
        global player
        if player == 'p1':
            player = 'p2'
        else:
            player = 'p1'


game = BattleShipUI()
server = RPCServer()

server.wait_players()
game.players_data['p1'] = 0
game.players_data['p2'] = 0

list_of_key = list(game.players_data.keys())

name_first_player = list_of_key[0]
name_second_player = list_of_key[1]
game.first_player_name = name_first_player
game.second_player_name = name_second_player
board_first_player, board_second_player = (
    game.first_board_game.get_initial_board(),
    game.second_board_game.get_initial_board(),
)
board_first_player = game.first_board_game.randomly_assign_ships()
board_second_player = game.second_board_game.randomly_assign_ships()
current_shift = name_first_player
while True:
    print(f" {player} Turn ")
    msg = server.read_message()
    msg_player, msg = msg.split('-')

    if end_message:
        return_message = end_message
        if total_players > 0:
            if player == loser:
                total_players -= 1
                loser = ''
                server.send_message(return_message)
            elif player == winner:
                winner = ''
                total_players -= 1
                server.send_message(return_message)
            else:
                server.send_message('game over')
            current_shift = game.player_opponent(current_shift)
            server.att_turn()
            continue
        else:
            server.send_message('game over')
            player = 'p1'
            end_message = ''
            break

    if not server.player_turn(msg_player):
        continue

    enemy_board = board_first_player
    player_board = board_second_player
    if current_shift == name_first_player:
        enemy_board = board_second_player
        player_board = board_first_player

    if msg == '':
        result = Fore.RESET + f" {current_shift} Turn "
        result += game.print_board(
            player_board, True, game.player_opponent(current_shift)
        )
        result += game.print_board(
            enemy_board, False, game.player_opponent(current_shift)
        )
        server.send_message(result)

    else:
        x, y = msg.split(',')
        if current_shift == name_first_player:
            successful, is_repeated = game.first_board_game.shoot(
                int(x), int(y), enemy_board
            )
        else:
            successful, is_repeated = game.second_board_game.shoot(
                int(x), int(y), enemy_board
            )
        return_message = game.print_board(player_board, True, current_shift)
        return_message += game.print_board(
            enemy_board, False, game.player_opponent(current_shift)
        )
        if is_repeated == True:
            return_message = (
                Fore.RESET
                + "This Position shot before, Please insert new coordinates again"
            )
        else:
            if successful:
                return_message += Fore.RESET + "successful shot"
                game.players_data[current_shift] = game.players_data[current_shift] + 1
                return_message += game.print_aditional_data(int(x), current_shift)
                if game.first_board_game.all_sunken_ships(enemy_board):
                    return_message += game.indicate_win(current_shift)
                    return_message += game.print_boards_with_boats(
                        board_first_player, board_second_player
                    )
                    print(return_message)
                    end_message = return_message
                    winner = current_shift
                    loser = game.player_opponent(current_shift)

            else:
                return_message += Fore.RESET + "Failure shoot"
                current_shift = game.player_opponent(current_shift)
                server.att_turn()

        server.send_message(return_message)
