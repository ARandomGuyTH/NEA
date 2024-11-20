import chessengine
from sys import exit
import pygame

#creates a board object
chess_board = chessengine.Board(chessengine.DEFAULT_FEN)

#creates game screen
pygame.init()
SCREEN_SIZE = WIDTH, HEIGHT = (600, 600)
screen = pygame.display.set_mode(SCREEN_SIZE)
screen.fill("white")

#clock used for timing
clock = pygame.time.Clock()

#square colours
BLACK_SQUARE_COLOUR = (150, 77, 55)
WHITE_SQUARE_COLOUR = (255, 233, 197)

#essential variables


#Sequence map used for getting images using FEN. Maps every character to a image filepath.
#functions are called once at start I think not every time.
IMAGE_MAP = {
  "r" : pygame.image.load("assets/blackrook.png").convert_alpha(),
  "n" : pygame.image.load("assets/blackknight.png").convert_alpha(),
  "b" : pygame.image.load("assets/blackbishop.png").convert_alpha(),
  "q" : pygame.image.load("assets/blackqueen.png").convert_alpha(),
  "k" : pygame.image.load("assets/blackking.png").convert_alpha(),
  "p" : pygame.image.load("assets/blackpawn.png").convert_alpha(),
  "R" : pygame.image.load("assets/whiterook.png").convert_alpha(),
  "N" : pygame.image.load("assets/whiteknight.png").convert_alpha(),
  "B" : pygame.image.load("assets/whitebishop.png").convert_alpha(),
  "Q" : pygame.image.load("assets/whitequeen.png").convert_alpha(),
  "K" : pygame.image.load("assets/whiteking.png").convert_alpha(),
  "P" : pygame.image.load("assets/whitepawn.png").convert_alpha()
}

#This may be innefficient as I may be calling the load function every time?
#furthermore I can create the squares once, not every frame.
def draw_board() -> list:
  """
  Creates and then draws all the squares and pieces.
  Then returns a 2D array containing all the squares as pygame rects.
  """
  #creates the squares on the board
  square_size = WIDTH / 8
  squares = []
  for i in range(8):
    row = []
    for j in range(8):
      #creates rectangle
      square_position_x, square_position_y = j * square_size, i * square_size
      rect = pygame.Rect(square_position_x, square_position_y, square_size, square_size)
      #draws the rectangle onto the screen.
      pygame.draw.rect(screen, WHITE_SQUARE_COLOUR if (i + j) % 2 == 0 else BLACK_SQUARE_COLOUR, rect)
      #appends it to the row for using later.
      row.append(rect)

      #draws the pieces onto the board
      if not chess_board.board[i][j] == None:
        #finds the image from the IMAGE_MAP dictionary
        piece_image = IMAGE_MAP[chess_board.board[i][j].FENKEY]
        #draws the image onto the screen
        screen.blit(piece_image, (square_position_x + 6, square_position_y + 6))
      
    #squares is a 2D array containing all the squares. This can be used for checking mouse collision.
    squares.append(row)
  return squares

def main() -> None:
  """
  Main function where the gameloop is held
  """
  can_move = False #checks if a piece can move or not
  #game loop
  while True:
        #checks for player inputs
        for event in pygame.event.get():
            #checks if the player has exited the game
            if event.type == pygame.QUIT:
                exit()
            #checks for mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
              pos = pygame.mouse.get_pos()
              for i in range(8):
                for j in range(8):
                  if squares[i][j].collidepoint(pos):
                    if can_move:
                       moveto = (i, j)
                       chess_board.update_board(movefrom, moveto)
                       can_move = False
                    else:
                      movefrom = (i, j)
                      can_move = True
        
        #draw the board.
        screen.fill("white")
        squares = draw_board()


        pygame.display.update()
        #DeltaTime is the time between frames, will be used for timing
        DeltaTime = clock.tick()

if __name__ == "__main__":
    main()