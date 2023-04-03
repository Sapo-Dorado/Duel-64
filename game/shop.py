from interfaces import WeaponItem, DefenseItem, MovementItem, Building
from constants import valid_position

def getDir(oldPos, newPos):
  oldX,oldY = oldPos
  newX,newY = newPos
  xDir = 0 if newX == oldX else (newX - oldX)/abs(newX - oldX)
  yDir = 0 if newY == oldY else (newY - oldY)/abs(newY - oldY)
  return (xDir, yDir)

def cardinalDirections(pos, distance):
  x,y = pos
  result = []
  for i in range(1,distance+1):
    result.append((x+i,y))
    result.append((x-i,y))
    result.append((x,y+i))
    result.append((x,y-i))

  return result

def removeInvalid(posList):
  return filter(valid_position, posList)

class NoWeapon(WeaponItem):
  def name(self):
    return "No Weapon"

  def description(self):
    return ""

  def attackRange(self, oldPos, newPos):
    return [newPos]

class Sword(WeaponItem):
  def name(self):
    return "Sword"
  
  def description(self):
    return "Increases attack range to include one additional block in the direction of movement."
  
  def base_price(self):
    return 5
  
  def attackRange(self, oldPos, newPos):
    xDir,yDir = getDir(oldPos, newPos)
    return removeInvalid([newPos, (newX + xDir, newY + yDir)])

class ThrowingStar(WeaponItem):
  def name(self):
    return "Throwing star"
  
  def description(self):
    return "Attacks in a Y shape pointing in the direction of movement. This adds two additional squares of range diagonally in front of you, and two in a straight line behind you."
  
  def base_price(self):
    return 7
  
  def attackRange(self, oldPos, newPos):
    xDir,yDir = getDir(oldPos, newPos)
    attack =[
      newPos,
      (newX - xDir, newY - yDir),
      (newX - (2*xDir), newY - (2*yDir)),
    ]
    if(xDir == 0):
      attack.append((newX + 1, newY + yDir))
      attack.append((newX - 1, newY + yDir))
    elif(yDir == 0):
      attack.append((newX + xDir, newY + 1))
      attack.append((newX + xDir, newY - 1))
    else:
      attack.append((newX + xDir, newY))
      attack.append((newX, newY + yDir))

    return removeInvalid(attack)

class NoMovement(MovementItem):
  def name(self):
    return "No Movement Item"

  def description(self):
    return ""
  
  def getPossibleSquares(self, pos):
    return removeInvalid(cardinalDirections(pos, 1))
  
class Boots(MovementItem):
  def name(self):
    return "Boots"
  
  def description(self):
    return "Increases potential movement range by one square in each cardinal direction."
  
  def base_price(self):
    return 5
  
  def getPossibleSquares(self, pos):
    return removeInvalid(cardinalDirections(pos, 2))

class Wings(MovementItem):
  def name(self):
    return "Wings"
  
  def description(self):
    return "Increases potential movement range by one square in each cardinal direction and one square in each diagonal direction."
  
  def base_price(self):
    return 7
  
  def getPossibleSquares(self, pos):
    x,y = pos
    squares = cardinalDirections(pos, 2)
    squares.append((x+1,y+1))
    squares.append((x+1,y-1))
    squares.append((x-1,y+1))
    squares.append((x-1,y-1))
    return removeInvalid(squares)

class NoDefense(DefenseItem):
  def name(self):
    return "No Defensive Item"
  
  def description(self):
    return ""

  def base_price(self):
    return 0
  
  def onDamage(self, player):
    player.kill()

class Mine(Building):
  def name(self):
    return "Mine"
  
  def description(self):
    return "Produces one gold per turn"
  
  def base_price(self):
    return 10
  
  def processTurn(self):
    self.getOwner().sendMoney(1)
