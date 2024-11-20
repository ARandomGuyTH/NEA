import pieces

  
#FEN chess notation for a starting board (means if INIT_SEQUENCE is changed the program can be used for any game state i.e. puzzles)
#White pieces are uppercase, black pieces are lower case
DEFAULT_FEN =  "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

#Colour represented as a boolean
WHITE = True
BLACK = False

#by default white goes first (chess rule)
turn = WHITE

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

  def create_board(self, FEN : str) -> list:
    """
    Takes in FEN as input. Returns the appropriate Board as a 2D list.
    """
    board = []
    #position is (x,y) or (rank, file)
    #iterates through the ranks
    for y, rank in enumerate(FEN.split("/")):
      temp_rank_list = [None for x in range(8)]
      #iterates through the individual pieces
      x = 0
      for piece in enumerate(rank):
        #checks if a piece or value
        if piece.isnumeric():
          x += int(piece)
        else:
          #creates and object if upper case piece is white
          temp_rank_list[x] = SEQUENCE_MAP[piece.lower()](piece.isupper(), (x, y), piece)
          x += 1
      board.append(temp_rank_list)   
    return board

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
    #checks if a piece is in that spot
    if not self.board[mofrx][mofry] is None:
      #swaps the pieces positions and updates the piece object
      self.board[mofrx][mofry], self.board[motox][motoy] = None, self.board[mofrx][mofry]
      self.board[motox][motoy].position = (motox, motoy)
      self.board[motox][motoy].has_moved = True

      return True
    #returning bool if it has happened may be useful?
    return False

def main() -> None:
  """
  main function for testing.
  """
  INIT_SEQUENCE =  "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
  board = Board(INIT_SEQUENCE)
  board.print_board()

if __name__ == "__main__":
  main()