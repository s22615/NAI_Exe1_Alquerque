from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax

"""Author
    Sebastian Mackiewicz - PJAIT student
"""

"""Installation
     - Make sure you have at least python 3.10(I was using the latest ver 3.12 but 3.10 should do the trick)
     - Game using easyAI framework so before running it type: pip install easyAI
"""

"""Rules
    - http://wikipedia.org/wiki/Alquerque
    - All pawns are marked by Matrix (mathematics). That means every one of them have positioned by two digits ##. 
      First by rows and second by columns. For example 11.
    - There is no multiple pawn beat
    - On begging of each round I highly recommend to type: show moves.
"""

"""Legend of the map
     B - black pawns on the board (AI pawns)
     W - white pawns on the board (Player pawns)
     X - empty space/possible move for each player pawns
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

    def __init__(self, players=None):
        self.players = players
        self.player_1_pawns = 12 # players starts with 12 pawns
        self.player_2_pawns = 12 # players starts with 12 pawns
        self.current_player = 1 # player 1 starts
        self.board = MAP

    def validate_move(self, player_symbol, opponent_symbol, cord_y, cord_x):
        """Description of the validate_move function
             Parameters:
             self: reference to the current instance of the class
             player_symbol (string): Symbol of current player pawns
             opponent_symbol (string): Symbol of current opponent pawns
             cord_y (int): Placement number that describes rows
             cord_x (int): Placement number that describes columns

             Returns:
             List: Returning all possible moves that can be performed in player's turn
        """

        all_moves = []  # list for all possible moves that can be performed in this player's turn
        rdy_cord = str(cord_y) + str(cord_x)  # combined coordinates of current pawn

        if cord_x > 0 and self.board[cord_y][cord_x-1] != player_symbol:  # checking move left
            if self.board[cord_y][cord_x-1] != opponent_symbol:
                all_moves.append(rdy_cord + ' - move left')
            else:
                if cord_x-1 > 0 and self.board[cord_y][cord_x-2] != opponent_symbol and self.board[cord_y][cord_x-2] != player_symbol:  # checking beat left
                    all_moves.append(rdy_cord + ' - beat left')

        if cord_x+1 < len(self.board)-1 and self.board[cord_y][cord_x+1] != player_symbol:  # checking move right
            if self.board[cord_y][cord_x+1] != opponent_symbol:
                all_moves.append(rdy_cord + ' - move right')
            else:
                if cord_x+2 < len(self.board)-1 and self.board[cord_y][cord_x+2] != opponent_symbol and self.board[cord_y][cord_x+2] != player_symbol:  # checking beat right
                    all_moves.append(rdy_cord + ' - beat right')

        if cord_y>0 and self.board[cord_y-1][cord_x] != player_symbol:  # checking move up
            if self.board[cord_y-1][cord_x] != opponent_symbol:
                all_moves.append(rdy_cord + ' - move up')
            else:
                if cord_y-1>0 and self.board[cord_y-2][cord_x] != opponent_symbol and self.board[cord_y-2][cord_x] != player_symbol:  # checking beat up
                    all_moves.append(rdy_cord + ' - beat up')

        if cord_y < len(self.board)-1 and self.board[cord_y+1][cord_x] != player_symbol:  # checking move down
            if self.board[cord_y+1][cord_x] != opponent_symbol:
                all_moves.append(rdy_cord + ' - move down')
            else:
                if cord_y+1 < len(self.board) - 1 and self.board[cord_y + 2][cord_x] != opponent_symbol and self.board[cord_y + 2][cord_x] != player_symbol:  # checking beat down
                    all_moves.append(rdy_cord + ' - beat down')

        if cord_y > 0 and cord_x > 0 and self.board[cord_y - 1][cord_x - 1] != player_symbol:  # checking move left-up
            if self.board[cord_y-1][cord_x-1] != opponent_symbol:
                all_moves.append(rdy_cord + ' - move left-up')
            else:
                if cord_y-1 > 0 and cord_x-1 > 0 and self.board[cord_y-2][cord_x-2] != opponent_symbol and self.board[cord_y-2][cord_x-2] != player_symbol:  # checking beat left-up
                    all_moves.append(rdy_cord + ' - beat left-up')

        if cord_x+1 < len(self.board)-1 and cord_y > 0 and self.board[cord_y-1][cord_x+1] != player_symbol:  # checking move right-up
            if self.board[cord_y-1][cord_x+1] != opponent_symbol:
                all_moves.append(rdy_cord + ' - move right-up')
            else:
                if cord_x+1 < len(self.board)-1 and cord_y-1 > 0 and self.board[cord_y-2][cord_x+2] != opponent_symbol and self.board[cord_y-2][cord_x+2] != player_symbol:  # checking beat right-up
                    all_moves.append(rdy_cord + ' - beat right-up')

        if cord_y+1 < len(self.board)-1 and cord_x+1 < len(self.board)-1 and self.board[cord_y+1][cord_x+1] != player_symbol:  # checking move right-down
            if self.board[cord_y+1][cord_x+1] != opponent_symbol:
                all_moves.append(rdy_cord + ' - move right-down')
            else:
                if cord_y+1 < len(self.board)-1 and cord_x+1 < len(self.board)-1 and self.board[cord_y+2][cord_x+2] != opponent_symbol and self.board[cord_y+2][cord_x+2] != player_symbol:  # checking beat right-down
                    all_moves.append(rdy_cord + ' - beat right-down')

        if cord_y+1 < len(self.board)-1 and cord_x+1 < len(self.board)-1 and self.board[cord_y+1][cord_x-1] != player_symbol:  # checking move left-down
            if self.board[cord_y+1][cord_x-1] != opponent_symbol:
                all_moves.append(rdy_cord + ' - move left-down')
            else:
                if cord_y+1 < len(self.board)-1 and cord_x+1 < len(self.board)-1 and self.board[cord_y+2][cord_x-2] != opponent_symbol and self.board[cord_y+2][cord_x-2] != player_symbol:  # checking beat left-down
                    all_moves.append(rdy_cord + ' - beat left-down')

        return list(all_moves)

    def process_opponent_score(self, pawn_symbol):
        """Description of the process_opponent_score function
             Parameters:
             self: reference to the current instance of the class
             pawn_symbol (string): Symbol of current player pawns
        """

        if pawn_symbol == 'W':
            self.player_2_pawns -= 1
        else:
            self.player_1_pawns -= 1

    def recognize_move(self, move, pawn_symbol):
        """Description of the recognize_move function
             Parameters:
             self: reference to the current instance of the class
             move (string): String that contains current pawn coordinates, type of move (move or beat), direction of move
             pawn_symbol (string): Symbol of current player pawns
        """

        cords = list(move[:2])  # list of two digits that represents row and col of current pawn
        f_cords = [int(x) for x in cords]  # fixed coordinates cast to int
        move_type = 'beat' if 'beat' in move else 'move'  # setting type of move
        direction = move.replace(move[:10], '')  # getting direction of the move

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
        """Description of the possible_moves function
             Parameters:
             self: reference to the current instance of the class

             Returns:
             List: Returning all possible moves that can be performed in player's turn
        """

        moves = []  # list for all possible moves that can be performed in this player's turn
        verified = []  # list of verified moves that can be performed in this player's turn

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
        """Description of the make_move function
             Parameters:
             self: reference to the current instance of the class
             move (string): String that contains current pawn coordinates, type of move (move or beat), direction of move
        """

        if self.current_player == 1:
            self.recognize_move(move, 'W')
        else:
            self.recognize_move(move, 'B')

    def display_map(self):
        """Description of the display_map function
             Parameters:
             self: reference to the current instance of the class

             Returns:
             String: Returning visual interpretation of the current map
        """

        current_map = ''  # string of visual interpretation of the current map
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
        """Description of the win function
             Parameters:
             self: reference to the current instance of the class

             Returns:
             None: Returning none if conditions fulfilled
        """

        if self.player_1_pawns == 0 or self.player_2_pawns == 0:  # player 1 or player 2 lost all his pawns ?
            return

    def is_over(self):
        """Description of the is_over function
             Parameters:
             self: reference to the current instance of the class

             Returns:
             Function: Calling function win() if this function was called
        """

        return self.win()  # Game stops when someone wins.

    def show(self):
        """Description of the is_over function
             Parameters:
             self: reference to the current instance of the class
        """

        print(self.display_map())
        print("Player 1 pawns - %d | Player 2 pawns - %d" % (self.player_1_pawns, self.player_2_pawns))
        print("---------------------------------")
        print("Don't know moves? Type: show moves")
        print("Want to quit? Type: quit")

    def scoring(self):
        """Description of the is_over function
             Parameters:
             self: reference to the current instance of the class

             Returns:
             Number: Returns score number conditions fulfilled else returns 0
        """
        return 100 if game.win() else 0  # For the AI

# Start a match (and store the history of moves when it ends)
ai = Negamax(4)  # The AI will think 4 moves in advance
game = Alquerque([Human_Player(), AI_Player(ai)])  # creating instance of the game
history = game.play()
