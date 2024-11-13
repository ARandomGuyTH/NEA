import pieces

class Board:
  def __init__(self, FEN):
    #Colour represented as a boolean
    self.WHITE = True
    self.BLACK = False

    #Sequence map used for creating the boards using FEN
    self.SEQUENCE_MAP = {
      "r" : pieces.Rook,
      "n" : pieces.Knight,
      "b" : pieces.Bishop,
      "q" : pieces.Queen,
      "k" : pieces.King,
      "p" : pieces.Pawn
    }

    self.board = self.create_board(FEN)

  #function takes in FEN notation as input and creates a game board using it
  def create_board(self, FEN):
    board = []
    #position is (x,y) or (rank, file)
    #iterates through the ranks
    for y, rank in enumerate(FEN.split("/")):
      temp_rank_list = [None for x in range(8)]
      #iterates through the individual pieces
      for x, piece in enumerate(rank):
        #checks if a piece or value
        if piece.isnumeric():
          x += int(piece)
        else:
          #creates and object if upper case piece is white
          temp_rank_list[x] = self.SEQUENCE_MAP[piece.lower()](colour = piece.isupper(), position = (x, y))
      board.append(temp_rank_list)   
    return board

  #takes in the board as input and displays it in text form (used for testing)
  def print_board(self):
    for rank in self.board:
      for piece in rank:
        print(piece, end="|")
      print()


#FEN chess notation for a starting board (means if INIT_SEQUENCE is changed the program can be used for any game state i.e. puzzles)
#White pieces are uppercase, black pieces are lower case
INIT_SEQUENCE = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

board = Board(INIT_SEQUENCE)

board.print_board()