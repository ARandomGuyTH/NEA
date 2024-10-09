import pieces

#function takes in FEN notation as input and creates a game board using it
def create_board(FEN):
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
        temp_rank_list[x] = SEQUENCE_MAP[piece.lower()](colour = piece.isupper(), position = [x, y])
    board.append(temp_rank_list)   
  return board

#takes in the board as input and displays it in text form (used for testing)
def print_board(board):
  for rank in board:
    for piece in rank:
      print(piece, end="|")
    print()

#creates game board
WHITE = True
BLACK = False

#FEN chess notation for a starting board (means if INIT_SEQUENCE is changed the program can be used for any game state i.e. puzzles)
#White pieces are uppercase, black pieces are lower case
INIT_SEQUENCE = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
#Sequence map used for creating objects using FEN
SEQUENCE_MAP = {
  "r" : pieces.Rook,
  "n" : pieces.Knight,
  "b" : pieces.Bishop,
  "q" : pieces.Queen,
  "k" : pieces.Knight,
  "p" : pieces.Pawn
}

board = create_board(INIT_SEQUENCE)
