#default class that all pieces inherit from
class Piece:
  image : str
  def __init__(self, colour : bool, position : list):
    self.colour = colour #piece colour
    self.position = position #keeps track of the position of the piece on the board
    self.pp = self.image[0] if self.colour else self.image[1]

  def __str__(self):
    #determines the colour of the piece
    if self.colour:
      colour = "white"
    else:
      colour = "black"
    
    return f"{self.pp}"
    #return f"{colour} {self.__class__.__name__}" #returns the colour and piece as a f string
    
class Pawn(Piece):
  #class variable to store the filepath of the image.
  image = ("hi", "sus")

class Knight(Piece):
  #class variable to store the filepath of the image.
  image = ("hi", "sus")

class Rook(Piece):
  #class variable to store the filepath of the image.
  image = ("hi", "sus")
class Bishop(Piece):
  #class variable to store the filepath of the image.
  image = ("hi", "sus")
class Queen(Piece):
  #class variable to store the filepath of the image.
  image = ("hi", "sus")

class King(Piece):
  #class variable to store the filepath of the image.
  image = ("hi", "sus")
