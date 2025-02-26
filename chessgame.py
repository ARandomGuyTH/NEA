import chessengine
from sys import exit
import pygame

#creates a board object
chess_board = chessengine.Board(chessengine.DEFAULT_FEN)
#chess_board = chessengine.Board("k7/8/8/8/8/1R6/2R6/K7")

#creates game screen
pygame.init()
SCREEN_SIZE = WIDTH, HEIGHT = (600, 600)
TIMER_SIZE = (100,600)
total_screen = pygame.display.set_mode((600+100, 600))
screen = pygame.Surface(SCREEN_SIZE)
screen.fill("white")
timer_screen = pygame.Surface(TIMER_SIZE)
timer_screen.fill("white")

#menu stuff
mediumFont = pygame.font.Font(None, 45)

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
pygame.display.set_icon(IMAGE_MAP["P"])

def show_move_previews(square_rect, square_size) -> None:
   """
   If a piece is selected shows all move previews and highlights that square
   """
   adjust = square_size / 2
   #highlights square
   pygame.draw.rect(screen, HIGHLIGHTED_SQUARE_COLOUR, square_rect)
   if chess_board.board[movefrom[0]][movefrom[1]]:
      #calls generate moves everyframe. Can be created when clicked.
      for move in move_previews:
        #calculate correct circle position
        circle_x, circle_y = move[1][0] * square_size + adjust, move[1][1] * square_size + adjust
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

def draw_main_menu(time : int) -> tuple:
  """
  creates main menu where player can select the side they want to play
  """
  #uses main menu image in order to display menu (easier then drawing using pygame)
  main_menu = pygame.image.load("assets/blobfish_with_timer.png").convert_alpha()
  main_menu = pygame.transform.scale(main_menu, (WIDTH, HEIGHT))
  screen.blit(main_menu, (0,0))

  timer_Time = mediumFont.render(f"{time:.0f}:00", True, (255, 255, 255)) #creates font
  timer_rect = timer_Time.get_rect(center = (300 , 550)) # creates rect around the font, moves to right spot
  screen.blit(timer_Time, timer_rect) #draws font onto screen


  #creates play as white button
  button_surface = pygame.Surface((235,102))  #create surface of size 232, 102
  button_surface.set_alpha(0)                #set transparent
  button_surface.fill((255,255,255))
  #creates and draws rect from surface
  white_button = screen.blit(button_surface, (50,355)) 

   #creates play as black button
  button_surface = pygame.Surface((235,102))  #create surface of size 232, 102
  button_surface.set_alpha(0)                #set transparent
  button_surface.fill((0,0,0))  
  #creates and draws rect from surface        
  black_button = screen.blit(button_surface, (600-50-232,355))

  #creates plus button
  button_surface = pygame.Surface((35,35))  #create surface of size 232, 102
  button_surface.set_alpha(0)                #set transparent
  button_surface.fill((255,255,255))
  #creates and draws rect from surface
  plus_button = screen.blit(button_surface, (405,532)) 

  #creates minus button
  button_surface = pygame.Surface((35,35))  #create surface of size 232, 102
  button_surface.set_alpha(0)                #set transparent
  button_surface.fill((255,255,255))
  #creates and draws rect from surface
  minus_button = screen.blit(button_surface, (165,532)) 

  return white_button, black_button, plus_button, minus_button

def draw_timer(black_time : int, white_time : int) -> None:
   """
   function takes in black's time and white's time.
   Draws the timer and time onto the screen.
   """
   #creates white timer
   white_timer = pygame.image.load("assets/chess_timer_white.png") #loads image
   white_timer = pygame.transform.scale(white_timer, (400, 100)) #resizes image
   white_timer = pygame.transform.rotate(white_timer, 90) #draws image
   timer_screen.blit(white_timer, (0,300)) # draws white timer onto screen

   black_timer = pygame.image.load("assets/chess_timer_black.png") #loads image
   black_timer = pygame.transform.scale(black_timer, (400, 100)) #resizes image
   black_timer = pygame.transform.rotate(black_timer, -90) #draws image
   timer_screen.blit(black_timer, (0,-100)) #draws black timer onto screen

   #creates time remaining text for black
   black_time_box = mediumFont.render(f"{int(black_time / 60)}:{int(black_time%60) :02d}", True, (255, 255, 255))#creates font
   black_time_box = pygame.transform.rotate(black_time_box, 90) #rotates font
   black_time_rect = black_time_box.get_rect(center = (50 , 200)) # creates rect around the font, moves to right spot
   timer_screen.blit(black_time_box, black_time_rect) #draws font onto screen

   #creates time remaining text for white
   white_time_box = mediumFont.render(f"{int(white_time / 60)}:{int(white_time%60) :02d}", True, (0, 0, 0))#creates font
   white_time_box = pygame.transform.rotate(white_time_box, 90) #rotates font
   white_time_rect = black_time_box.get_rect(center = (50 , 400))# creates rect around the font, moves to right spot
   timer_screen.blit(white_time_box, white_time_rect)#draws font onto screen

def draw_win_lose(winner : bool,type : str) -> pygame.Rect:
  #creates plus button
  background = pygame.Surface((500,350))  #create surface of size 232, 102
  background.set_alpha(200)                #set transparent
  background.fill((255,253,208))
  #creates and draws rect from surface
  screen.blit(background, (50,125))

  #creates plus button
  background = pygame.Surface((35,35))  #create surface of size 232, 102
  background.set_alpha(100)                #set transparent
  background.fill((255,253,208))
  #creates and draws rect from surface
  screen.blit(background, (300,300))


def main() -> None:
  """
  Main function where the gameloop is held
  """
  can_move = False #checks if a piece can move or not
  global square_rect
  global movefrom
  global move_previews
  
  white_button : pygame.rect.Rect
  black_button : pygame.rect.Rect

  game_ended = False
  end_reason = ""
  
  squares = []
  timer_selector_time = 10
  
  #if True, human is white side. If false, human is black side.
  human_player_colour : bool
  in_main_menu = True
  #game loop
  black_remaining_time = 10.00 * 60
  white_remaining_time = 10.00 * 60
  while True:
    #checks for player inputs
    for event in pygame.event.get():
        #checks if the player has exited the game
        if event.type == pygame.QUIT:
            exit()
        #checks for mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
          pos = pygame.mouse.get_pos() # get mouse position

          if in_main_menu:
            if white_button.collidepoint(pos):
              human_player_colour = True
              in_main_menu = False
              
            elif black_button.collidepoint(pos):
              human_player_colour = False
              in_main_menu = False
            
            elif plus_button.collidepoint(pos):
                if timer_selector_time < 10:
                  timer_selector_time += 1
                elif timer_selector_time < 30:
                  timer_selector_time += 5
                elif timer_selector_time < 60:
                  timer_selector_time += 10

            elif minus_button.collidepoint(pos):
                if timer_selector_time <= 0:
                  pass
                elif timer_selector_time <= 10:
                  timer_selector_time -= 1
                elif timer_selector_time <= 30:
                  timer_selector_time -= 5
                elif timer_selector_time <= 60:
                  timer_selector_time -= 10
                  
          elif human_player_colour == chess_board.current_turn and not game_ended:
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
        total_screen.fill("white")
        

        if in_main_menu:
           white_button, black_button, plus_button, minus_button = draw_main_menu(timer_selector_time)
           black_remaining_time = timer_selector_time * 60
           white_remaining_time = timer_selector_time * 60
        
        elif not game_ended:
          squares = draw_board()

          if chess_board.current_turn:
            #subtracts time from white
            white_remaining_time -= DeltaTime * 0.001
            if white_remaining_time <= 0:
              game_ended = True
              end_reason = "timeout"
              winner = False
          
          else:
            #subtracts time from black
            black_remaining_time -= DeltaTime * 0.001
            if black_remaining_time <= 0:
              game_ended = True
              end_reason = "timeout"
              winner = True

          if human_player_colour != chess_board.current_turn: #if it is ai turn
            move = chess_board.select_ai_move()
            valid = chess_board.update_board(move[0], move[1])
            print(valid)

          #else:
          #  move = chess_board.select_ai_move()
          #  valid = chess_board.update_board(move[0], move[1])
        
        else:
          squares = draw_board()
          draw_win_lose(winner, end_reason)

        draw_timer(black_remaining_time ,white_remaining_time)
        
        total_screen.blit(screen, (0, 0))
        total_screen.blit(timer_screen, (600, 0))


        pygame.display.update()
        #DeltaTime is the time between frames, will be used for timing
        DeltaTime = clock.tick(24) #time between frames in ms

if __name__ == "__main__":
    main()