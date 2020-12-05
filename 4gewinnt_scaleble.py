import os
import random
import threading


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


transpose = lambda l, m: list(map(list, zip(*list(map(lambda x: x[::-1], list(map(lambda x: list(x+[0]*m)[:m], l)))))))


class Board:
    def __init__(self, x, y):
        self.states = []
        self.max_height = x
        for i in range(y):
            self.states.append([])

    def print_board(self):
        cod = transpose(self.states, self.max_height)
        p_moves = self.possible_moves()
        a = 0
        clear()
        for i in range(len(cod)):
            for k, j in enumerate(cod[i]):
                if [k, i] not in p_moves:
                    print(str(j if j != 0 else " ") + "  | ", end="")
                elif j == 0:
                    print(str(a+1 if a >= 9 else str(a+1)+" ") + " | ", end="")
                    a += 1
            print("")

    def make_turn(self, num, player):
        num -= 1
        if self.is_valid_turn(num):
            self.states[self.possible_moves()[num][0]].append(player.symbol)
            return True
        else:
            return False

    def is_valid_turn(self, num):
        j = 0
        for i in self.states:
            if len(i) != self.max_height:
                j += 1
        if num <= j:
            return True
        return False

    def possible_moves(self):
        moves = []
        for i, j in enumerate(self.states):
            if len(j) < self.max_height:
                moves.append([i, 0])
        return moves

    def is_full(self):
        cod = transpose(self.states, self.max_height)
        for i in range(len(cod)):
            for j in cod[i]:
                if j == 0:
                    return False
        return True

    def is_win(self, player):
        rows = self.rows()
        for row in rows:
            j = 0
            for i in row:
                if i == player.symbol:
                    j += 1
                    if j == 4:
                        return True
                else:
                    j = 0
        return False

    def rows(self):
        cods = transpose(self.states, self.max_height)
        rows = self.states + cods
        for i in range(len(self.states)):
            for j in range(2):
                row = []
                for x, y in zip(range(i, len(self.states)-i), range(len(cods)) if j == 0 else range(len(cods)-1, -1, -1)):
                    row.append(cods[y][x])
                if len(row) >= 4:
                    rows.append(row)
        for i in range(len(cods)):
            for j in range(2):
                row = []
                for x, y in zip(range(0, len(self.states)) if j == 0 else range(len(self.states)-1, -1, -1), range(i, len(cods))):
                    row.append(cods[y][x])
                if len(row) >= 4:
                    rows.append(row)
        return rows


class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    def play(self, possible_moves):
        a = 0
        while a == 0:
            try:
                print("player " + self.symbol + ": ")
                number = int(input("Where do you want to place your sign?: "))
                if number > len(possible_moves) or number <= 0:
                    print("number has to be between 1-", len(possible_moves))
                    continue
                if board.make_turn(number, self):
                    a = 1
                else:
                    print("wrong turn")
            except ValueError:
                print("please enter a number")

    def is_win(self, board):
        if board.is_win(self):
            return True
        return False


class Bot(Player):
    def play(self, cells, possible_moves):
        if len(possible_moves) > 1:
            board.make_turn(random.randint(1, len(possible_moves)), self)
        else:
            board.make_turn(1, self)


class botthread(threading.Thread):
    is_won = False
    def __init__(self, bot, board):
        threading.Thread.__init__(self)
        self.bot = bot
        self.board = board

    def run(self):
        if not self.board.is_full():
            self.bot.play(transpose(self.board.states, self.board.max_height), self.board.possible_moves())
        if bot.is_win(board):
            botthread.is_won = self.bot.symbol

if __name__ == '__main__':
    players = []
    bots = []
    a = 0
    while a == 0:
        try:
            player_c = int(input("number of Players: "))
            if player_c < 0 or player_c > 26:
                print("there should be between 0-26 players")
                continue
            bot_c = int(input("number of Bots: "))
            if bot_c < 0 or bot_c > 26:
                print("there should be between 0-26 players")
                continue
            if bot_c+player_c == 0:
                print("there has to be at least one player/bot")
                continue
            x = int(input("x size of board: "))
            y = int(input("y size of board: "))
            if (x < 4 and y < 4) and (x <= 0 or y <= 0):
                print("x or y size not right check: is one of them higher then 4 and both higher then 0")
                continue
            a = 1
        except ValueError:
            print("input must be an integer")

    board = Board(x, y)
    for i in range(player_c):
        players.append(Player(chr(65+i)))
    for i in range(bot_c):
        bots.append(Bot(chr(97+i)))
    board.print_board()
    while not board.is_full():
        for player in players:
            if not board.is_full():
                player.play(board.possible_moves())
            board.print_board()
            if player.is_win(board):
                board.print_board()
                print("congratulation: player ", player.symbol, " has won")
                exit()
        for bot in bots:
            thread = botthread(bot, board)
            thread.start()
        board.print_board()
        if botthread.is_won:
            board.print_board()
            print("congratulation: bot ", botthread.is_won, " has won")
            exit()
    board.print_board()
    print("its a tie")
