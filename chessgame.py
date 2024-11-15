import chessengine
from sys import exit
import pygame

#creates a board object
chess_board = chessengine.Board(chessengine.default_FEN)

#creates game screen
pygame.init()
SCREEN_SIZE = (600, 600)
screen = pygame.display.set_mode(SCREEN_SIZE)
screen.fill("white")

#clock used for timing
clock = pygame.time.Clock()

#blank background 
background = pygame.Surface((600,600))
background_rect = background.get_rect(topleft=(0,0))
background.fill("white")


#image=pygame.image.load("blank.png").convert_alpha()
#image=pygame.transform.scale(image,(165,165))

class Square(pygame.sprite.Sprite):
  def __init__(self, pos, coord):
    super().__init__()
    #self.image = image
    #self.rect=self.image.get_rect(bottomright=pos)
    #self.value=-1
    #self.coord=coord
    #cross=pygame.image.load("cross.png").convert_alpha()
    #cross=pygame.transform.scale(cross,(165,165))
    #circle=pygame.image.load("circle.png").convert_alpha()
    #circle=pygame.transform.scale(circle,(165,165))
    #self.img_list=[cross,circle]

def update(self):
   pass

#creates squares group that will be used for mouse controls
#by using a group I can update all squares at once
Squares = pygame.sprite.Group()

#creates squares on board
for x in range(8):
  for y in range(8):
    #doesnt work rn lol
    #Squares.add(Square((x*-170+555,y*-170+555),(x,y)))
    pass

def main():
    #game loop
    while True:
        #checks for player inputs
        for event in pygame.event.get():
            #checks if the player has exited the game
            if event.type == pygame.QUIT:
                pygame.exit()
                exit()

        #updates all squares
        Squares.update()
        Squares.draw(screen)

        pygame.display.update()
        #DeltaTime is the time between frames, will be used for timing
        DeltaTime = clock.tick()

if __name__ == "__main__":
    main()