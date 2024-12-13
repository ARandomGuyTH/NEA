#default class that all pieces inherit from

#direction for all sliding pieces. Directions are (x, y), values should be 1 (forward), -1 (backwards), or 0 (doesnt move)
diagonal_slide_direction = ((1, 1), (1, -1), (-1, 1), (-1, -1))
straight_slide_direction = ((1, 0), (-1, 0), (0, 1), (0, -1))
queen_slide_direction = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))

#default class that all pieces inherit from
class Piece:
  """
  Piece class all pieces inherit from.
  """
  def __init__(self, colour : bool, position : tuple, FENkey : str) -> None:
    self.COLOUR = colour #piece colour
    self.position = position #keeps track of the position of the piece on the board
    self.FENKEY = FENkey #key used for finding appropriate image
    self.has_moved = False #checks if a piece has moved or not (for pawns, kings and rooks)

  def __str__(self) -> str:
    """
    returns the colour and name of the piece
    """
    #determines piece colour
    if self.COLOUR:
      colour = "white"
    else:
      colour = "black"
    
    return f"{colour} {self.__class__.__name__}" #returns the colour and piece as a f string
  
  def update_position(self, position : tuple) -> bool:
    """
    Takes in a tuple of length 2 and updatest the position of the piece to that position.
    If a pawn reaches the final rank will allow for promotion.
    """
    self.position = position
    #false indicates a pawn will not be promoted
    return False

  def check_piece(self, position : tuple, board : list) -> bool:
    """
    Takes in a move (position) and a board and checks if a same coloured piece exists in that spot.
    Returns False if there is, True if not.
    If True the piece can move to that spot.
    """
    #checks if there is a piece in that position
    if not board[position[1]][position[0]]:
      return True
    
    #checks if a piece in that position is the opposite colour
    if board[position[1]][position[0]].COLOUR != self.COLOUR:
      return True
    
    return False
  
  def generate_pawn_moves(self, board : list) -> list:
    """
    Generates every move a pawn can make.
    """
    curr_x, curr_y = self.position

    #if the pawn is white it moves up the board (negative)
    if self.COLOUR:
      movement = -1
    #if the pawn is black it moves down the board (positive)
    else:
      movement = 1

    moves = []

    #checks for single pushing pawns
    moveto = (curr_x, curr_y + movement)
    if board[moveto[1]][moveto[0]] is None:
      move = (self.position, moveto)
      moves.append(move)

      #checks for double pushing pawn
      if not self.has_moved:
        moveto = (curr_x, curr_y + movement * 2)
        if board[moveto[1]][moveto[0]] is None:
          move = (self.position, moveto)
          moves.append(move)
      
    #checks if a piece is in the left diagonal (can take)
    if self.position[0] != 0:
      if board[curr_y + movement][curr_x - 1] is not None:
        moveto = (curr_x - 1, curr_y + movement)
        if self.check_piece(moveto, board):
          move = (self.position, moveto)
          moves.append(move)
    
    #checks if a piece is in the right diagonal (can take)
    if self.position[0] != 7:
      if board[curr_y + movement][curr_x + 1] is not None:
        moveto = (curr_x + 1, curr_y + movement)
        if self.check_piece(moveto, board):
          move = (self.position, moveto)
          moves.append(move)
    
    return moves

  def generate_sliding_moves(self, board : list, direction : tuple) -> list:
    """
    Generates sliding piece moves. direction should be the directions the pieces can move.
    For example, (1, -1) is top right, (1, 0) is right, etc.
    """
    moves = []

    #adjustment used for determining side checked (right left down up)
    for adjust_x, adjust_y in direction:
      search_x, search_y = self.position
      search_x += adjust_x
      search_y +=  adjust_y
      #iterates until the end of the board
      while search_x in range(0, 8) and search_y in range(0, 8):
        #checks if a piece has been reached
        if board[search_y][search_x] is None:
          #if there is no piece the move can be made
          moveto = (search_x, search_y)
          move = (self.position, moveto)
          moves.append(move)
          
          search_x += adjust_x
          search_y +=  adjust_y
        
        else:
          #if there is a piece we need to check if the piece can be taken
          moveto = (search_x, search_y)
          if self.check_piece(moveto, board):
            #if the piece can be taken the move can be made
            move = (self.position, moveto)
            moves.append(move)
          #the loop needs to be break to avoid piece jumping
          break

    return moves
  
  def generate_adjacent_moves(self, board : list) -> list:
    """
    Genereates adjacent moves (squares next to a piece). For Kings.
    """
    curr_x, curr_y = self.position

    moves = []

    #loop through all adjacent squares
    for x in range(3):
      for y in range(3):
        #check if the squares are on the board
        if curr_x - 1 + x in range(0,8) and curr_y - 1 + y in range(0, 8):
          moveto = (curr_x - 1 + x, curr_y - 1 + y)
          #check if the move can be made
          if self.check_piece(moveto, board):
            move = (self.position, moveto)
            moves.append(move)
    
    return moves
  
  def generate_knight_moves(self, board : list) -> list:
    """
    Generate knight moves (L shape, can jump pieces).
    """
    curr_x, curr_y = self.position

    moves = []

    offset = [-2, -1, 1, 2]
    for x_offset in offset:
      for y_offset in offset:
        #absolute of x_offset can't equal y_offset
        if x_offset != y_offset and -x_offset != y_offset:
          moveto = (curr_x + x_offset, curr_y + y_offset)
          if moveto[0] in range(0,8) and moveto[1] in range(0, 8):
            if self.check_piece(moveto, board):
              move = (self.position, moveto)
              moves.append(move)
    
    return moves  
class Pawn(Piece):
  def generate_moves(self, board : list) -> list:
    """
    Will generate all moves a pawn can make.
    Moves will be a list of all possible moves.
    A move will be a tuple of 2 tuples, containing the position to move from in the first tuple.
    And, the position to move to in the second tuple.
    """
    moves = self.generate_pawn_moves(board)
    return moves
  
  def update_position(self, position : tuple) -> bool:
    """
    Takes in a tuple of length 2 and updatest the position of the piece to that position.
    If a pawn reaches the final rank will allow for promotion.
    """
    self.position = position
    #false indicates a pawn will not be promoted
    return True

class Knight(Piece):
  def generate_moves(self, board : list) -> list:
    """
    Will generate all moves a Rook can make.
    Moves will be a list of all possible moves.
    A move will be a tuple of 2 tuples, containing the position to move from in the first tuple.
    And, the position to move to in the second tuple.
    """
    moves = self.generate_knight_moves(board)
    return moves

class Rook(Piece):
  def generate_moves(self, board : list) -> list:
      """
      Will generate all moves a Rook can make.
      Moves will be a list of all possible moves.
      A move will be a tuple of 2 tuples, containing the position to move from in the first tuple.
      And, the position to move to in the second tuple.
      """
      moves = self.generate_sliding_moves(board, straight_slide_direction)
      return moves

class Bishop(Piece):
  def generate_moves(self, board : list) -> list:
    """
    Will generate all moves a Bishop can make.
    Moves will be a list of all possible moves.
    A move will be a tuple of 2 tuples, containing the position to move from in the first tuple.
    And, the position to move to in the second tuple.
    """
    moves = self.generate_sliding_moves(board, diagonal_slide_direction)
    return moves

class Queen(Piece):
  def generate_moves(self, board : list) -> list:
    """
    Will generate all moves a Queen can make.
    Moves will be a list of all possible moves.
    A move will be a tuple of 2 tuples, containing the position to move from in the first tuple.
    And, the position to move to in the second tuple.
    """
    moves = self.generate_sliding_moves(board, queen_slide_direction)
    return moves


class King(Piece):
  def generate_moves(self, board : list) -> list:
    """
    Will generate all moves a King can make.
    Moves will be a list of all possible moves.
    A move will be a tuple of 2 tuples, containing the position to move from in the first tuple.
    And, the position to move to in the second tuple.
    """
    moves = self.generate_adjacent_moves(board)
    return moves

  def check_moves(self, board : list, moves : list, piece : Piece) -> bool:
    """
    given a list of moves and a type of piece
    Will determine if that piece, of an opposite colour to the king appears.
    """
    for move in moves:
      #iterates through all the moves
      moveto = move[1]
      #checks if the target square has an instance of a specific class. 
      #(if the target square is a specific piece i.e - Queen)
      if isinstance(board[moveto[1]][moveto[0]], piece):
        return True


  def check_detection(self, board : list) -> bool:
    """
    checks if the king is in check. Returns True if the king is.
    """
    #only need to check the last move for rooks bishops and queens!!!!
    #!!!!OPTIMISE LATER!!!
    #generates rook moves and checks for rooks and queens
    moves = self.generate_sliding_moves(board, diagonal_slide_direction)
    if self.check_moves(board, moves, Bishop):
      return True
    if self.check_moves(board, moves, Queen):
      return True

    #generates bishop moves and checks for bishops and queens
    moves = self.generate_sliding_moves(board, straight_slide_direction)
    if self.check_moves(board, moves, Rook):
      return True
    if self.check_moves(board, moves, Queen):
      return True
    
    #generates knight moves and checks for knights
    moves = self.generate_knight_moves(board)
    if self.check_moves(board, moves, Knight):
      return True
    
    #generates Pawn moves and checks for Pawns
    moves = self.generate_pawn_moves(board)
    if self.check_moves(board, moves, Pawn):
      return True

    #generates King moves and checks for Kings
    moves = self.generate_adjacent_moves(board)
    if self.check_moves(board, moves, King):
      return True
    
    #if no checks found returns False to indicate king not in check
    return False
    

    
    
if __name__ == "__main__":
  print(1 * True)