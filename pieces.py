#default class that all pieces inherit from
class Piece:
  def __init__(self, colour, position):
    self.colour = colour #piece colour
    self.position = position #keeps track of the position of the piece on the board
  
  def __str__(self):
    #determines the colour of the piece
    if self.colour:
      colour = "white"
    else:
      colour = "black"
      
    return f"{colour} {self.__class__.__name__}" #returns the colour and piece as a f string
    
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
