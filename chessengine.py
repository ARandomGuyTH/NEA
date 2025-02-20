import pieces
from copy import deepcopy
import random
  
#FEN chess notation for a starting board (means if INIT_SEQUENCE is changed the program can be used for any game state i.e. puzzles)
#White pieces are uppercase, black pieces are lower case
DEFAULT_FEN =  "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

#Colour represented as a boolean
WHITE = True
BLACK = False

#Sequence map used for creating the boards using FEN. Maps every character to a class using a dictionary
SEQUENCE_MAP = {
      "r" : pieces.Rook,
      "n" : pieces.Knight,
      "b" : pieces.Bishop,
      "q" : pieces.Queen,
      "k" : pieces.King,
      "p" : pieces.Pawn
    }

class Board:
  """
  Board class 
  """
  def __init__(self, FEN: str):

    #creates board
    self.board = self.create_board(FEN)

    #by default white moves first
    self.current_turn = WHITE

    self.find_kings()

  def create_board(self, FEN : str) -> list:
    """
    Takes in FEN as input. Returns the appropriate Board as a 2D list.
    """
    board = []
    #position is (x,y) or (file, rank)
    #iterates through the ranks
    for y, rank in enumerate(FEN.split("/")):
      temp_rank_list = [None for x in range(8)]
      #iterates through the individual pieces
      x = 0
      for piece in rank:
        #checks if a piece or value
        if piece.isnumeric():
          x += int(piece)
        else:
          #creates and object if upper case piece is white
          temp_rank_list[x] = SEQUENCE_MAP[piece.lower()](piece.isupper(), (x, y), piece)
          x += 1

      board.append(temp_rank_list)   
    return board
  
  def find_kings(self , board=None) -> None:
    """
    will find the kings on the board and return their coordinates.
    Firstly, the white king's position, then the black's
    """
    if board is None:
      board = self.board

    #iterates through every piece on the board
    for rank in board:
      for piece in rank:
        #checks if the piece is king
        if isinstance(piece, pieces.King):
          #checks if the piece is white or Black
          if piece.COLOUR:
            #stores a reference to the White King
            self.white_king = piece
          else:
            #stores a reference to the Black King
            self.black_king = piece

  #takes in the board as input and displays it in text form (used for testing)
  def print_board(self) -> None:
    """
    prints the board as text.
    """
    for rank in self.board:
      for piece in rank:
        print(piece, end=" | ")
      print()
  
  def update_board(self, movefrom : tuple, moveto : tuple) -> bool:
    """
    given a move (x,y), (x,y) move that piece.
    moves should be tuples
    First tuple, coord of square containing piece to move. Second, coord of square to move it to.
    top left 0,0. bottom right 8,8.
    """
    #unpacks tuple for x and y coords
    mofrx, mofry = movefrom
    motox, motoy = moveto
    selected_piece = self.board[mofrx][mofry]
    #checks if a piece is in that spot
    if self.validate_move(movefrom, moveto):
      if not self.incheck(movefrom, moveto):
        #swaps the pieces positions and updates the piece object
        self.board[mofrx][mofry], self.board[motox][motoy] = None, self.board[mofrx][mofry]
        self.board = self.board[motox][motoy].update_position((motoy, motox), self.board)
        self.board[motox][motoy].has_moved = True

        self.update_turn()
        return True
    #returning bool if it has happened may be useful?
    return False
  
  def validate_move(self, movefrom : tuple, moveto : tuple, board=None) -> bool:
    """
    Takes in a move, and checks if the move is valid or not.
    """

    if board is None:
      board = self.board

    mofrx, mofry = movefrom
    motox, motoy = moveto
    selected_piece = board[mofrx][mofry]

    #checks if a piece is being selected
    if selected_piece is None:
      return False
    
    #checks if a piece is being moved on the correct turn
    if selected_piece.COLOUR != self.current_turn:
      return False
    
    if mofrx == motox and mofry == motoy:
      return False
    
    if ((mofry, mofrx), (motoy, motox)) not in selected_piece.generate_moves(board):
      return False

    #and to check for if the move creates checks.

    #True is returned if the move is valid
    return True
  
  def update_turn(self) -> None:
    """
    when called, alternates who's turn it is. Returns the updated value
    """
    if self.current_turn:
      #if the current turn is white change it to black
      self.current_turn = BLACK
 
    else:
      #if the current turn is black change it to white
      self.current_turn = WHITE
    
    #moves = self.generate_legal_moves()

    #if not moves:
    #  print("GAME OVER!")
    
    #returning the updated value may be useful later
    return self.current_turn
  
  def generate_legal_moves(self, board=None):
    """
    function generates all the moves a given player can make
    Iterates through every piece, checks if the piece is the right player's
    If so extends the moves list to include their moves
    """

    #ensures function can be used easily for both 
    if board is None:
      board = self.board

    moves = []


    for rank in self.board:
      for piece in rank:
        if piece:
          if piece.COLOUR == self.current_turn:
              for move in piece.generate_moves(self.board):
                temp = move
                move = ((temp[0][1], temp[0][0]), (temp[1][1], temp[1][0]))
                if not self.incheck(move[0], move[1]):
                  print(move)

                #if not self.incheck(move[0], move[1]):
                  #moves.append(move)
                  moves.append(move)


    return moves

  def incheck(self, movefrom : tuple, moveto : tuple) -> bool:
    """
    given a move will check if that move results in check.
    """
    #I make a deep copy of the current position to revert back to
    current_board = deepcopy(self.board)
    #unpack the move
    mofrx, mofry = movefrom
    motox, motoy = moveto

    #by default the move is valid until a check is found
    valid = True

    #I update the position to the position being searched for cehcks
    current_board[mofrx][mofry], current_board[motox][motoy] = None, current_board[mofrx][mofry]
    current_board = current_board[motox][motoy].update_position((motoy, motox), self.board)

    #Update the king references
    self.find_kings(current_board)

    #check whos turn it is and searches using that side's king
    #if the king is in check check_detection returns True and the move isn't valid
    if self.current_turn:
      if self.white_king.check_detection(self.board):
        valid = False
    
    else:
      if self.black_king.check_detection(self.board):
        valid = False

    #return back to original position
    self.find_kings()

    #returns if the move is valid or not
    return not valid

  def select_ai_move(self):
    moves = self.generate_legal_moves()
    return random.choice(moves)

  def force_move(self, movefrom : tuple, moveto : tuple, board=None) -> None:
    #unpacks tuple for x and y coords
    mofrx, mofry = movefrom
    motox, motoy = moveto

    #swaps the pieces positions and updates the piece object
    self.board[mofrx][mofry], self.board[motox][motoy] = None, self.board[mofrx][mofry]
    self.board = self.board[motox][motoy].update_position((motoy, motox), self.board)

    self.update_turn()


def main() -> None:
  """
  main function for testing.
  """
  INIT_SEQUENCE =  "r3k2r/8/8/8/8/8/8/R3K2R"
  board = Board(INIT_SEQUENCE)
  board.print_board()
  print("-" * 8)

  #board.force_move((7, 4), (7, 6))
  board.force_move((7,4), (7,2))

  #board.force_move((0, 4), (0,6))
  board.force_move((0, 4), (0,2))

  print("-" * 8)
  board.print_board()

if __name__ == "__main__":
  main()