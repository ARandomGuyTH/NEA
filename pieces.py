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
  
  def generate_moves(self) -> set:
    """
    Will generate all moves a piece can make. Different for each piece.
    """
    pass
  
  def generate_pawn_moves(self) -> set:
    """
    Generates every move a pawn can make.
    """
    raise NotImplementedError
  
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
