import chessengine
import sys
import pygame

#creates game screen
pygame.init()
SCREEN_SIZE = (600, 600)
screen = pygame.display.set_mode(SCREEN_SIZE)

def main():
    #game loop
    while True:
        #checks if a player has exited the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

if __name__ == "__main__":
    main()