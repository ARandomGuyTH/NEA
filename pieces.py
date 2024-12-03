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

  def generate_diagonal_moves(self) -> set:
    """
    Generates diagonal moves. For Queen's and Bishops.
    """
    raise NotImplementedError
  
  def generate_straight_moves(self, board : list) -> list:
    """
    Generates straight moves. For Queen's and Rooks.
    """
    curr_x, curr_y = self.position

    moves = []

    #searches left
    search_x = curr_x
    while search_x >= 0 and board[curr_y][search_x] is None:
      search_x -= 1
      if self.check_piece((search_x, curr_y), board):
        move = (self.position, (search_x, curr_y))
        moves.append(move)
    
    return moves
  
  def generate_adjacent_moves(self) -> set:
    """
    Genereates adjacent moves (squares next to a piece). For Kings.
    """
    raise NotImplementedError
  
  def generate_knight_moves(self) -> set:
    """
    Generate knight moves (L shape, can jump pieces).
    """
    raise NotImplementedError
  
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

class Knight(Piece):
  pass

class Rook(Piece):
  def generate_moves(self, board : list) -> list:
      """
      Will generate all moves a Rook can make.
      Moves will be a list of all possible moves.
      A move will be a tuple of 2 tuples, containing the position to move from in the first tuple.
      And, the position to move to in the second tuple.
      """
      moves = self.generate_straight_moves(board)
      return moves


class Bishop(Piece):
  pass
class Queen(Piece):
  pass

class King(Piece):
  pass

if __name__ == "__main__":
  print(1 * True)