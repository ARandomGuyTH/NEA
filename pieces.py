class Piece:
  def __init__(self, colour, position):
    self.colour = colour
    self.position = position
  
  def __str__(self):
    return if self.colour: "white" else: "black", {self.__class__}"
    
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
    
  
