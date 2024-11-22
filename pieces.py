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
  
  def generate_moves(self, board : list) -> list:
    """
    Will generate all moves a piece can make. Different for each piece.
    Moves will be a list of all possible moves.
    A move will be a tuple of 2 tuples, containing the position to move from in the first tuple.
    And, the position to move to in the second tuple.
    """
    pass
  
  def generate_pawn_moves(self, board : list) -> list:
    """
    Generates every move a pawn can make.
    """
    moves = []

    #checks for double pushing pawn
    if self.has_moved == False:
      move = (self.position, (self.position[0], self.position[1] + 2))
      moves.append(move)
    

  def generate_diagonal_moves(self) -> set:
    """
    Generates diagonal moves. For Queen's and Bishops.
    """
    raise NotImplementedError
  
  def generate_straight_moves(self) -> set:
    """
    Generates straight moves. For Queen's and Rooks.
    """
    raise NotImplementedError
  
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
  pass
class Knight(Piece):
  pass

class Rook(Piece):
  pass
class Bishop(Piece):
  pass
class Queen(Piece):
  pass

class King(Piece):
  pass

if __name__ == "__main__":
  print(1 * True)