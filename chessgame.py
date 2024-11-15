import chessengine
from sys import exit
import pygame

#creates a board object
chess_board = chessengine.Board(chessengine.default_FEN)

#creates game screen
pygame.init()
SCREEN_SIZE = WIDTH, HEIGHT = (600, 600)
screen = pygame.display.set_mode(SCREEN_SIZE)
screen.fill("white")

#clock used for timing
clock = pygame.time.Clock()

#blank background 
background = pygame.Surface((600,600))
background_rect = background.get_rect(topleft=(0,0))
background.fill("white")

#square colours
black_square_colour = (150, 77, 55)
white_square_colour = (255, 233, 197)


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


def draw_board():
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
      pygame.draw.rect(screen, white_square_colour if (i + j) % 2 == 0 else black_square_colour, rect)

      #draws the pieces onto the board
      if not chess_board.board[i][j] == None:
        #finds the image from the IMAGE_MAP dictionary
        piece_image = IMAGE_MAP[chess_board.board[i][j].FENkey]
        #draws the image onto the screen
        screen.blit(piece_image, (square_position_x + 6, square_position_y + 6))


def main():
    #game loop
    while True:
        #checks for player inputs
        for event in pygame.event.get():
            #checks if the player has exited the game
            if event.type == pygame.QUIT:
                exit()
        
        screen.fill("white")
        draw_board()


        pygame.display.update()
        #DeltaTime is the time between frames, will be used for timing
        DeltaTime = clock.tick()

if __name__ == "__main__":
    main()