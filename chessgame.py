import chessengine
from sys import exit
import pygame

#creates a board object
chess_board = chessengine.Board(chessengine.DEFAULT_FEN)
#chess_board = chessengine.Board("k7/8/8/8/8/1R6/2R6/K7")

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
HIGHLIGHTED_SQUARE_COLOUR = (229, 212, 98)
ORANGE_COLOUR = (215, 151, 0)
pygame.display.set_caption("Blobfish")

#essential variables
square_rect = None
square_size = HEIGHT / 8

#loads the images into the game 
r_image = pygame.image.load("assets/blackrook.png").convert_alpha()
n_image = pygame.image.load("assets/blackknight.png").convert_alpha()
b_image = pygame.image.load("assets/blackbishop.png").convert_alpha()
q_image = pygame.image.load("assets/blackqueen.png").convert_alpha()
k_image = pygame.image.load("assets/blackking.png").convert_alpha()
p_image = pygame.image.load("assets/blackpawn.png").convert_alpha()
R_image = pygame.image.load("assets/whiterook.png").convert_alpha()
N_image = pygame.image.load("assets/whiteknight.png").convert_alpha()
B_image = pygame.image.load("assets/whitebishop.png").convert_alpha()
Q_image = pygame.image.load("assets/whitequeen.png").convert_alpha()
K_image = pygame.image.load("assets/whiteking.png").convert_alpha()
P_image = pygame.image.load("assets/whitepawn.png").convert_alpha()

#rescales the images to be the same size as the squares
rescale_size = (square_size, square_size)
r_image = pygame.transform.scale(r_image, rescale_size)
n_image = pygame.transform.scale(n_image, rescale_size)
b_image = pygame.transform.scale(b_image, rescale_size)
q_image = pygame.transform.scale(q_image, rescale_size)
k_image = pygame.transform.scale(k_image, rescale_size)
p_image = pygame.transform.scale(p_image, rescale_size)
R_image = pygame.transform.scale(R_image, rescale_size)
N_image = pygame.transform.scale(N_image, rescale_size)
B_image = pygame.transform.scale(B_image, rescale_size)
Q_image = pygame.transform.scale(Q_image, rescale_size)
K_image = pygame.transform.scale(K_image, rescale_size)
P_image = pygame.transform.scale(P_image, rescale_size)

#Sequence map used for getting images using FEN. Maps every character to a image filepath.
IMAGE_MAP = {
  "r" : r_image,
  "n" : n_image,
  "b" : b_image,
  "q" : q_image,
  "k" : k_image,
  "p" : p_image,
  "R" : R_image,
  "N" : N_image,
  "B" : B_image,
  "Q" : Q_image,
  "K" : K_image,
  "P" : P_image
}
pygame.display.set_icon(IMAGE_MAP["P"])

def show_move_previews(square_rect, square_size) -> None:
   """
   If a piece is selected shows all move previews and highlights that square
   """
   #highlights square
   pygame.draw.rect(screen, HIGHLIGHTED_SQUARE_COLOUR, square_rect)
   if chess_board.board[movefrom[0]][movefrom[1]]:
      #calls generate moves everyframe. Can be created when clicked.
      for move in move_previews:
        #calculate correct circle position
        circle_x, circle_y = move[1][0] * square_size, move[1][1] * square_size
        #draws circle on the screen
        pygame.draw.circle(screen, ORANGE_COLOUR, (circle_x, circle_y), 15, 2) #radius 15, thickness 2

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
  
    #squares is a 2D array containing all the squares. This can be used for checking mouse collision.
    squares.append(row)

  #highlights any selected pieces
  if not square_rect is None:
    show_move_previews(square_rect, square_size)
  
  for i in range(8):
    for j in range(8):
      square_position_x, square_position_y = j * square_size, i * square_size
      #draws the pieces onto the board
      if not chess_board.board[i][j] == None:
        #finds the image from the IMAGE_MAP dictionary
        piece_image = IMAGE_MAP[chess_board.board[i][j].FENKEY]
        #draws the image onto the screen
        screen.blit(piece_image, (square_position_x + 6, square_position_y + 6))
      
  return squares

def main() -> None:
  """
  Main function where the gameloop is held
  """
  can_move = False #checks if a piece can move or not
  global square_rect
  global movefrom
  global move_previews
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
                       square_rect = None
                       move_previews = []
                    else:
                      square_rect = squares[i][j]
                      movefrom = (i, j)
                      can_move = True

                      if chess_board.board[movefrom[0]][movefrom[1]]:
                        move_previews = chess_board.board[movefrom[0]][movefrom[1]].generate_moves(chess_board.board)
        
        #draw the board.
        screen.fill("white")
        squares = draw_board()


        pygame.display.update()
        #DeltaTime is the time between frames, will be used for timing
        DeltaTime = clock.tick(24)

if __name__ == "__main__":
    main()