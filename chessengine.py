import pieces
from copy import deepcopy
import random
  
#FEN chess notation for a starting board (means if INIT_SEQUENCE is changed the program can be used for any game state i.e. puzzles)
#White pieces are uppercase, black pieces are lower case
DEFAULT_FEN =  "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

#Colour represented as a boolean
WHITE = True
BLACK = False

#Sequence map used for creating the boards using FEN. Maps every character to a class using a dictionary
SEQUENCE_MAP = {
      "r" : pieces.Rook,
      "n" : pieces.Knight,
      "b" : pieces.Bishop,
      "q" : pieces.Queen,
      "k" : pieces.King,
      "p" : pieces.Pawn
    }

class Board:
  """
  Board class 
  """
  def __init__(self, FEN: str):

    #creates board
    self.board = self.create_board(FEN)

    #by default white moves first
    self.current_turn = WHITE

    self.find_kings()
    self.AI_making_move = False

    self.nodes_searched = 0

  def create_board(self, FEN : str) -> list:
    """
    Takes in FEN as input. Returns the appropriate Board as a 2D list.
    """
    board = []
    #position is (x,y) or (file, rank)
    #iterates through the ranks
    for y, rank in enumerate(FEN.split("/")):
      temp_rank_list = [None for x in range(8)]
      #iterates through the individual pieces
      x = 0
      for piece in rank:
        #checks if a piece or value
        if piece.isnumeric():
          x += int(piece)
        else:
          #creates and object if upper case piece is white
          temp_rank_list[x] = SEQUENCE_MAP[piece.lower()](piece.isupper(), (x, y), piece)
          x += 1

      board.append(temp_rank_list)   
    return board
  
  def find_kings(self , board=None) -> None:
    """
    will find the kings on the board and return their coordinates.
    Firstly, the white king's position, then the black's
    """
    if board is None:
      board = self.board

    #iterates through every piece on the board
    for rank in board:
      for piece in rank:
        #checks if the piece is king
        if isinstance(piece, pieces.King):
          #checks if the piece is white or Black
          if piece.COLOUR:
            #stores a reference to the White King
            self.white_king = piece
          else:
            #stores a reference to the Black King
            self.black_king = piece

  #takes in the board as input and displays it in text form (used for testing)
  def print_board(self) -> None:
    """
    prints the board as text.
    """
    for rank in self.board:
      for piece in rank:
        print(piece, end=" | ")
      print()
  
  def update_board(self, movefrom : tuple, moveto : tuple) -> bool:
    """
    given a move (x,y), (x,y) move that piece.
    moves should be tuples
    First tuple, coord of square containing piece to move. Second, coord of square to move it to.
    top left 0,0. bottom right 8,8.
    """
    #unpacks tuple for x and y coords
    mofrx, mofry = movefrom
    motox, motoy = moveto
    selected_piece = self.board[mofrx][mofry]
    #checks if a piece is in that spot
    if self.validate_move(movefrom, moveto):
      if not self.incheck(movefrom, moveto):
        #swaps the pieces positions and updates the piece object
        self.board[mofrx][mofry], self.board[motox][motoy] = None, self.board[mofrx][mofry]
        self.board = self.board[motox][motoy].update_position((motoy, motox), self.board)
        self.board[motox][motoy].has_moved = True

        self.update_turn()
        return True
    #returning bool if it has happened may be useful?
    return False
  
  def validate_move(self, movefrom : tuple, moveto : tuple, board=None) -> bool:
    """
    Takes in a move, and checks if the move is valid or not.
    """

    if board is None:
      board = self.board

    mofrx, mofry = movefrom
    motox, motoy = moveto
    selected_piece = board[mofrx][mofry]
    #checks if a piece is being selected
    if selected_piece is None:
      return False
    
    #checks if a piece is being moved on the correct turn
    if selected_piece.COLOUR != self.current_turn:
      return False
    
    if mofrx == motox and mofry == motoy:
      return False
    
    if ((mofry, mofrx), (motoy, motox)) not in selected_piece.generate_moves(board):
      return False

    #and to check for if the move creates checks.

    #True is returned if the move is valid
    return True
  
  def update_turn(self) -> None:
    """
    when called, alternates who's turn it is. Returns the updated value
    """
    if self.current_turn:
      #if the current turn is white change it to black
      self.current_turn = BLACK
 
    else:
      #if the current turn is black change it to white
      self.current_turn = WHITE
    
    #moves = self.generate_legal_moves()

    #if not moves:
    #  print("GAME OVER!")
    
    #returning the updated value may be useful later
    return self.current_turn
  
  def generate_legal_moves(self, board=None):
    """
    function generates all the moves a given player can make
    Iterates through every piece, checks if the piece is the right player's
    If so extends the moves list to include their moves
    """

    #ensures function can be used easily for both 
    if board is None:
      board = self.board

    moves = []


    for rank in board:
      for piece in rank:
        if piece:
          if piece.COLOUR == self.current_turn:
              for move in piece.generate_moves(board):
                movefry, movefrx = move[0]
                movetoy, movetox = move[1]

                if not self.incheck((movefrx, movefry), (movetox, movetoy), board):
                  moves.append(((movefrx, movefry), (movetox, movetoy)))

    return moves
  
  def score_move(self, move, board=None):
      if board is None:
        board = self.board
      
      movefrx, movefry = move[0]
      motox, motoy = move[1]
      
      if board[motox][motoy]: #check if the move invovles taking a piece
        #prioritises capturing high value pieces with low value
        return -10 * board[motox][motoy].value + board[movefrx][movefry].value
      
      return 0


  def quickSort(self, array, leftptr, righptr, board):
    if leftptr < righptr: #if array contains at least 2 elements
      partitionptr = self.partition(array, leftptr, righptr, board) #finds pointer position
      self.quickSort(array, leftptr, partitionptr - 1, board) #sort elements to the left of the partition
      self.quickSort(array, partitionptr + 1, righptr, board) #sort elements to the right of the partition
  
  def partition(self, array, leftptr, rightptr, board):
    i = leftptr
    j = rightptr - 1

    pivot = self.score_move(array[rightptr], board)

    while i < j: #while the pointers have not crossed
      while i < rightptr and self.score_move(array[i], board) < pivot:
        #keep incrimenting until end of section reached or value at pointer i is less then pivot
        i += 1

      while j > leftptr and self.score_move(array[j], board) >= pivot:
        #keep deincrimenting until end of section reached or value at pointer j is greater then pivot
        j -= 1
      
      if i < j: #if pointers have not crossed swap the elements
        array[i], array[j] = array[j], array[i]
      
    if self.score_move(array[i], board) > pivot: #if i and j cross if value of i is greater then pivot swap the elements
      array[i], array[rightptr] = array[rightptr], array[i]
    
    return i # i is where array is split to continue to divide and conquer

  def incheck(self, movefrom : tuple, moveto : tuple, board=None) -> bool:
    """
    given a move will check if that move results in check.
    """
    if board is None:
      board = self.board

    #I make a deep copy of the current position to revert back to
    current_board = deepcopy(board)
    #unpack the move
    mofrx, mofry = movefrom
    motox, motoy = moveto

    #by default the move is valid until a check is found
    valid = True

    #I update the position to the position being searched for checks
    current_board[mofrx][mofry], current_board[motox][motoy] = None, current_board[mofrx][mofry]
    current_board = current_board[motox][motoy].update_position((motoy, motox), current_board) #THIS IS CAUSING PROBLEMS MAKING MOVES!!!!!

    #Update the king references
    self.find_kings(current_board)

    #check whos turn it is and searches using that side's king
    #if the king is in check check_detection returns True and the move isn't valid
    if self.current_turn:
      if self.white_king.check_detection(current_board):
        valid = False
    
    else:
      if self.black_king.check_detection(current_board):
        valid = False

    #return back to original position
    self.find_kings(current_board)

    #returns if the move is valid or not
    return not valid

  def select_ai_move(self):
    if self.terminal():
      return None
    
    original_turn = self.current_turn
    
    current_best_move = ((0, 0), (0, 0))
    board = deepcopy(self.board)
    current_greatest_utility = float('-inf')

    moves = self.generate_legal_moves(board) #generate all moves
    self.quickSort(moves, 0, len(moves) - 1, board) #move ordering

      
    if self.current_turn:
      for move in moves:
        v = self.minimise(self.force_move(move[0], move[1], deepcopy(board)), 4, float('-inf'), float('inf'))

        if v > current_greatest_utility:
            current_greatest_utility = v
            current_best_move = move
    
    else:
      for move in moves:
        v = self.maximise(self.force_move(move[0], move[1], deepcopy(board)), 4, float('-inf'), float('inf'))
        v = v * -1

        if v > current_greatest_utility:
            current_greatest_utility = v
            current_best_move = move
    
    self.current_turn = original_turn #reset turn
    
    return current_best_move

  def force_move(self, movefrom : tuple, moveto : tuple, board=None) -> None:
    if board is None:
      board = self.board
    #unpacks tuple for x and y coords
    mofrx, mofry = movefrom
    motox, motoy = moveto

    #swaps the pieces positions and updates the piece object
    board[mofrx][mofry], board[motox][motoy] = None, board[mofrx][mofry]
    board = board[motox][motoy].update_position((motoy, motox), board)

    self.update_turn()

    return board

  def terminal(self, board=None):
    """
    checks if the game has ended or not
    """
    if board is None:
      board = self.board

    winner = self.winner()

    if winner is None:
      #if no winner or draw game has not ended
      return False

    return True
  
  def evaluate(self, board=None):
    if board is None:
      board = self.board
    
    evaluation = 0

    for rank in board:
      for piece in rank:
        if piece:
          if piece.COLOUR:
            evaluation += piece.pst[piece.position[0]][piece.position[1]] + piece.value
            #evaluation += piece.value
          
          else:
            evaluation -= piece.pst[7 - piece.position[0]][piece.position[1]] + piece.value
            #evaluation -= piece.value

    return evaluation

  def winner(self, board=None):
    if board is None:
      board = self.board

    if self.generate_legal_moves(board):
      return None #none if no one wins
    
    self.find_kings(board)

    #check whos turn it is and searches using that side's king
    #if the king is in check check_detection returns True and the move isn't valid
    if self.current_turn:
      if self.white_king.check_detection(board):
        return BLACK
    
    else:
      if self.black_king.check_detection(board):
        return WHITE

      return -1 #else draw so neither side wins.

  def minimise(self, board, depth, alpha, beta):
    self.current_turn = BLACK
    depth -= 1 #limit depth to not take too much time
    if self.terminal(board):
      #checks if game ends returns winner
      v =  9999 if self.winner(board) == 1 else 0 if self.winner(board) == -1  else -9999
      return v

    elif depth <= 0: #if depth reached return approximate value
      return self.evaluate(board)

    v = float('inf') #worse case +inf (very big)

    moves = self.generate_legal_moves(board) #generate all moves
    self.quickSort(moves, 0, len(moves) - 1, board) #move ordering

    for move in moves: #for each move player can make
      #if move eval is smaller then current best move, current best move is eval
      v = min(v, self.maximise(self.force_move(move[0], move[1], deepcopy(board)), depth, alpha, beta))
      
      if v < alpha: #if move smaller then best maxi move eval
        break #prune branch

      #if if move smaller then best mini move eval move eval is best mini move eval
      beta = min(beta, v)
    
    return v #return to be used in maximise
  
  def maximise(self, board, depth, alpha, beta):
    self.current_turn = WHITE
    depth -= 1 #limit depth to not take too much time
    if self.terminal(board):
      #checks if game ends returns winner
      v =  9999 if self.winner(board) == 1 else 0 if self.winner(board) == -1  else -9999
      return v

    elif depth <= 0: #if depth reached return approximation
      return self.evaluate(board)

    v = float('-inf') #worse case -inf (very small)
    
    moves = self.generate_legal_moves(board) #sort all moves
    self.quickSort(moves, 0, len(moves) - 1, board) #move ordering

    for move in moves: #for each move player can make
      #if move eval is bigger then current best move, current best move is eval
      v = max(v, self.minimise(self.force_move(move[0], move[1], deepcopy(board)), depth, alpha, beta))
      
      if v > beta: #if move bigger then best mini move eval
        break #prune branch

       #if if move bigger then best maxi move eval move eval is best maxi move eval
      alpha = max(alpha, v)
    
    return v  #return to be used in minimise

def main() -> None:
  """
  main function for testing.
  """
  INIT_SEQUENCE =  "r3k2r/8/8/8/8/8/8/R3K2R"
  board = Board(INIT_SEQUENCE)
  board.print_board()
  print("-" * 8)

  #board.force_move((7, 4), (7, 6))
  board.force_move((7,4), (7,2))

  #board.force_move((0, 4), (0,6))
  board.force_move((0, 4), (0,2))

  print("-" * 8)
  board.print_board()

if __name__ == "__main__":
  main()
