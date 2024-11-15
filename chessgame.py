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


def draw_board():
  #creates the squares on the board
  square_size = WIDTH / 8
  squares = []
  for i in range(8):
    row = []
    for j in range(8):
      #creates rectangle
      rect = pygame.Rect( j * square_size, i * square_size, square_size, square_size)
      #draws the rectangle onto the screen
      pygame.draw.rect(screen, "white" if (i + j) % 2 == 0 else "black", rect)
  
      #draws the pieces onto the board
      


def main():
    #game loop
    while True:
        #checks for player inputs
        for event in pygame.event.get():
            #checks if the player has exited the game
            if event.type == pygame.QUIT:
                exit()
        
        draw_board()


        pygame.display.update()
        #DeltaTime is the time between frames, will be used for timing
        DeltaTime = clock.tick()

if __name__ == "__main__":
    main()