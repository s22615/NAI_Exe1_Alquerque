from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax

"""Legend of the map

     # - board wall(cannot be passed)
     B - black pawns on the board
     W - white pawns on the board
     X - empty space/possible move for player pawn

"""

MAP = """
BBBBB
BBBBB
BBXWW
WWWWW
WWWWW
"""

MAP = [list(x) for x in MAP.split("\n") if x]

class Alquerque( TwoPlayerGame ):
    """Rules of this arabic game
        -> http://wikipedia.org/wiki/Alquerque

        ! IMPORTANT !
        - Make sure you have at least python 3.10
        - All pawns are marked by Matrix (mathematics).
        That means every one of them have positioned by two digits ##. First by rows and second by columns.
        - There is no multiple pawn beat
    """

    def __init__(self, players=None):
        self.players = players
        self.player_1_pawns = 12 # players starts with 12 pawns
        self.player_2_pawns = 12 # players starts with 12 pawns
        self.current_player = 1 # player 1 starts
        self.board = MAP

    """Description of the possible_moves function

     Parameters:
     argument1 (self): [BLANK]

     Returns:
     String: Returning possible moves like Choose pawn, Move pawn, Beat enemy pawn

    """

    def validate_move(self, player_symbol, opponent_symbol, cord_y, cord_x):
        all_moves = []
        rdy_cord = str(cord_y) + str(cord_x)

        if cord_x > 0 and self.board[cord_y][cord_x-1] != player_symbol: # left
            if self.board[cord_y][cord_x-1] != opponent_symbol:
                all_moves.append(rdy_cord + ' - move left')
            else:
                if cord_x-1 > 0 and self.board[cord_y][cord_x-2] != opponent_symbol and self.board[cord_y][cord_x-2] != player_symbol:
                    all_moves.append(rdy_cord + ' - beat left')

        if cord_x+1 < len(self.board)-1 and self.board[cord_y][cord_x+1] != player_symbol: # right
            if self.board[cord_y][cord_x+1] != opponent_symbol:
                all_moves.append(rdy_cord + ' - move right')
            else:
                if cord_x+2 < len(self.board)-1 and self.board[cord_y][cord_x+2] != opponent_symbol and self.board[cord_y][cord_x+2] != player_symbol:
                    all_moves.append(rdy_cord + ' - beat right')

        if cord_y>0 and self.board[cord_y-1][cord_x] != player_symbol: # up
            if self.board[cord_y-1][cord_x] != opponent_symbol:
                all_moves.append(rdy_cord + ' - move up')
            else:
                if cord_y-1>0 and self.board[cord_y-2][cord_x] != opponent_symbol and self.board[cord_y-2][cord_x] != player_symbol:
                    all_moves.append(rdy_cord + ' - beat up')

        if cord_y < len(self.board)-1 and self.board[cord_y+1][cord_x] != player_symbol: # down
            if self.board[cord_y+1][cord_x] != opponent_symbol:
                all_moves.append(rdy_cord + ' - move down')
            else:
                if cord_y+1 < len(self.board) - 1 and self.board[cord_y + 2][cord_x] != opponent_symbol and self.board[cord_y + 2][cord_x] != player_symbol:
                    all_moves.append(rdy_cord + ' - beat down')

        if cord_y > 0 and cord_x > 0 and self.board[cord_y - 1][cord_x - 1] != player_symbol: # left-up
            if self.board[cord_y-1][cord_x-1] != opponent_symbol:
                all_moves.append(rdy_cord + ' - move left-up')
            else:
                if cord_y-1 > 0 and cord_x-1 > 0 and self.board[cord_y-2][cord_x-2] != opponent_symbol and self.board[cord_y-2][cord_x-2] != player_symbol:
                    all_moves.append(rdy_cord + ' - beat left-up')

        if cord_x+1 < len(self.board)-1 and cord_y > 0 and self.board[cord_y-1][cord_x+1] != player_symbol: # right-up
            if self.board[cord_y-1][cord_x+1] != opponent_symbol:
                all_moves.append(rdy_cord + ' - move right-up')
            else:
                if cord_x+1 < len(self.board)-1 and cord_y-1 > 0 and self.board[cord_y-2][cord_x+2] != opponent_symbol and self.board[cord_y-2][cord_x+2] != player_symbol:
                    all_moves.append(rdy_cord + ' - beat right-up')

        if cord_y+1 < len(self.board)-1 and cord_x+1 < len(self.board)-1 and self.board[cord_y+1][cord_x+1] != player_symbol: # right-down
            if self.board[cord_y+1][cord_x+1] != opponent_symbol:
                all_moves.append(rdy_cord + ' - move right-down')
            else:
                if cord_y+1 < len(self.board)-1 and cord_x+1 < len(self.board)-1 and self.board[cord_y+2][cord_x+2] != opponent_symbol and self.board[cord_y+2][cord_x+2] != player_symbol:
                    all_moves.append(rdy_cord + ' - beat right-down')

        if cord_y+1 < len(self.board)-1 and cord_x+1 < len(self.board)-1 and self.board[cord_y+1][cord_x-1] != player_symbol: # left-down
            if self.board[cord_y+1][cord_x-1] != opponent_symbol:
                all_moves.append(rdy_cord + ' - move left-down')
            else:
                if cord_y+1 < len(self.board)-1 and cord_x+1 < len(self.board)-1 and self.board[cord_y+2][cord_x-2] != opponent_symbol and self.board[cord_y+2][cord_x-2] != player_symbol:
                    all_moves.append(rdy_cord + ' - beat left-down')

        return list(all_moves)

    def process_opponent_score(self, pawn_symbol):
        if pawn_symbol == 'W':
            self.player_2_pawns -= 1
        else:
            self.player_1_pawns -= 1

    def recognize_move(self, move, pawn_symbol):
        cords = list(move[:2])
        f_cords = [int(x) for x in cords] # fixed cords casted to int
        move_type = 'beat' if 'beat' in move else 'move'
        direction = move.replace(move[:10], '')

        match direction:
            case 'left':
                if move_type == 'move':
                    self.board[f_cords[0]][f_cords[1]] = 'X'
                    self.board[f_cords[0]][f_cords[1]-1] = pawn_symbol
                else:
                    self.board[f_cords[0]][f_cords[1]] = 'X'
                    self.board[f_cords[0]][f_cords[1]-1] = 'X'
                    self.board[f_cords[0]][f_cords[1]-2] = pawn_symbol
                    self.process_opponent_score(pawn_symbol)
            case 'right':
                if move_type == 'move':
                    self.board[f_cords[0]][f_cords[1]] = 'X'
                    self.board[f_cords[0]][f_cords[1]+1] = pawn_symbol
                else:
                    self.board[f_cords[0]][f_cords[1]] = 'X'
                    self.board[f_cords[0]][f_cords[1]-1] = 'X'
                    self.board[f_cords[0]][f_cords[1]-2] = pawn_symbol
                    self.process_opponent_score(pawn_symbol)
            case 'up':
                if move_type == 'move':
                    self.board[f_cords[0]][f_cords[1]] = 'X'
                    self.board[f_cords[0]-1][f_cords[1]] = pawn_symbol
                else:
                    self.board[f_cords[0]][f_cords[1]] = 'X'
                    self.board[f_cords[0]-1][f_cords[1]] = 'X'
                    self.board[f_cords[0]-2][f_cords[1]] = pawn_symbol
                    self.process_opponent_score(pawn_symbol)
            case 'down':
                if move_type == 'move':
                    self.board[f_cords[0]][f_cords[1]] = 'X'
                    self.board[f_cords[0]+1][f_cords[1]] = pawn_symbol
                else:
                    self.board[f_cords[0]][f_cords[1]] = 'X'
                    self.board[f_cords[0]+1][f_cords[1]] = 'X'
                    self.board[f_cords[0]+2][f_cords[1]] = pawn_symbol
                    self.process_opponent_score(pawn_symbol)
            case 'left-up':
                if move_type == 'move':
                    self.board[f_cords[0]][f_cords[1]] = 'X'
                    self.board[f_cords[0]-1][f_cords[1]-1] = pawn_symbol
                else:
                    self.board[f_cords[0]][f_cords[1]] = 'X'
                    self.board[f_cords[0]-1][f_cords[1]-1] = 'X'
                    self.board[f_cords[0]-2][f_cords[1]-2] = pawn_symbol
                    self.process_opponent_score(pawn_symbol)
            case 'left-down':
                if move_type == 'move':
                    self.board[f_cords[0]][f_cords[1]] = 'X'
                    self.board[f_cords[0]+1][f_cords[1]-1] = pawn_symbol
                else:
                    self.board[f_cords[0]][f_cords[1]] = 'X'
                    self.board[f_cords[0]+1][f_cords[1]-1] = 'X'
                    self.board[f_cords[0]+2][f_cords[1]-2] = pawn_symbol
                    self.process_opponent_score(pawn_symbol)
            case 'right-up':
                if move_type == 'move':
                    self.board[f_cords[0]][f_cords[1]] = 'X'
                    self.board[f_cords[0]-1][f_cords[1]+1] = pawn_symbol
                else:
                    self.board[f_cords[0]][f_cords[1]] = 'X'
                    self.board[f_cords[0]-1][f_cords[1]+1] = 'X'
                    self.board[f_cords[0]-2][f_cords[1]+2] = pawn_symbol
                    self.process_opponent_score(pawn_symbol)
            case 'right-down':
                if move_type == 'move':
                    self.board[f_cords[0]][f_cords[1]] = 'X'
                    self.board[f_cords[0]+1][f_cords[1]+1] = pawn_symbol
                else:
                    self.board[f_cords[0]][f_cords[1]] = 'X'
                    self.board[f_cords[0]+1][f_cords[1]+1] = 'X'
                    self.board[f_cords[0]+2][f_cords[1]+2] = pawn_symbol
                    self.process_opponent_score(pawn_symbol)

    def possible_moves(self):
        moves = []
        verified = []

        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.current_player == 1:
                    if self.board[y][x] == 'W':
                        verified = self.validate_move('W', 'B', y, x)
                else:
                    if self.board[y][x] == 'B':
                        verified = self.validate_move('B', 'W', y, x)

                if verified:
                    for move in verified:
                        moves.append(move)

                    verified.clear()

        return list(moves)

    def make_move(self, move):
        if self.current_player == 1:
            self.recognize_move(move, 'W')
        else:
            self.recognize_move(move, 'B')

    def display_map(self):
        current_map = ''
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if x != len(self.board[y])-1:
                    current_map += self.board[y][x]
                    current_map += '-'
                else:
                    current_map += self.board[y][x]
                    current_map += "\n"
        return current_map

    def win(self):
        if self.player_1_pawns == 0 or self.player_2_pawns == 0:  # player 1 or player 2 lost all his pawns ?
            return

    def is_over(self): return self.win()  # Game stops when someone wins.

    def show(self):
        print(self.display_map())
        print("Player 1 pawns - %d | Player 2 pawns - %d" % (self.player_1_pawns, self.player_2_pawns))
        print("---------------------------------")
        print("Don't know moves? Type: show moves")
        print("Want to quit? Type: quit")

    def scoring(self): return 100 if game.win() else 0  # For the AI

# Start a match (and store the history of moves when it ends)
ai = Negamax(4) # The AI will think 4 moves in advance
game = Alquerque( [ Human_Player(), AI_Player(ai) ] )
history = game.play()