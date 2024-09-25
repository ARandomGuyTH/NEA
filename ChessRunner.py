import pygame
import pieces
#creates game UI
pygame.init()
SCREEN_SIZE = (800, 800)
screen = pygame.display.set_mode(SCREEN_SIZE)

#creates game board
board = []
WHITE = 1
BLACK = 0
#FEN chess notation for a starting board (means if INIT_SEQUENCE is changed the program can be used for any game state i.e. puzzles)
#White pieces are uppercase, black pieces are lower case
INIT_SEQUENCE = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
SEQUENCE_MAP = {
  "r" : pieces.Rook,
  "n" : pieces.Knight,
  "b" : pieces.Bishop,
  "q" : pieces.Queen,
  "k" : Pieces.Knight,
  "b" : Pieces.Bishop
}
#position is (x,y) or (rank, file)
#iterates through the ranks
for y, rank in enumerate(INIT_SEQUENCE.split("/")):
  temp_rank_list = [None for x in range(8)]
  #iterates through the individual pieces
  for x, piece in enumerate(rank):
    if piece.isnumeric():
      x += int(piece)
    else:
      temp_rank_list[x] = SEQUENCE_MAP[piece.lower()](colour = piece.isupper(), position = [x, y])
    
      
  
  
  
  
  
    
  
