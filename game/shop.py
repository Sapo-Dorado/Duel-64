from game.interfaces import WeaponItem, DefenseItem, MovementItem, Building, NoDefense, NoMovement, NoWeapon
from game.constants import removeInvalid, cardinalDirections
import game.constants as constants

class BasicShop:
  def __init__(self):
    self.items = [Sword(), ThrowingStar(), Boots(), Wings(), Shield(), UpgradedShield(), Mine()]
    self.constructors = [Sword, ThrowingStar, Boots, Wings, Shield, UpgradedShield, Mine]
  
  def extractItem(self, idx):
    item = self.items[idx]
    self.items[idx] = self.constructors[idx]()
    return item
  
  def getItems(self):
    return self.items

def getDir(oldPos, newPos):
  oldX,oldY = oldPos
  newX,newY = newPos
  xDir = 0 if newX == oldX else (newX - oldX)//abs(newX - oldX)
  yDir = 0 if newY == oldY else (newY - oldY)//abs(newY - oldY)
  return (xDir, yDir)


class Sword(WeaponItem):
  def name(self):
    return constants.SWORD
  
  def description(self):
    return constants.SWORD_DESC
  
  def base_price(self):
    return 5
  
  def attackRange(self, oldPos, newPos):
    newX, newY = newPos
    xDir,yDir = getDir(oldPos, newPos)
    return removeInvalid([newPos, (newX + xDir, newY + yDir)])

class ThrowingStar(WeaponItem):
  def name(self):
    return constants.THROWING_STAR
  
  def description(self):
    return constants.THROWING_STAR_DESC
  
  def base_price(self):
    return 9
  
  def attackRange(self, oldPos, newPos):
    newX,newY = newPos
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

class Boots(MovementItem):
  def name(self):
    return constants.BOOTS 
  
  def description(self):
    return constants.BOOTS_DESC
  
  def base_price(self):
    return 5
  
  def getPossibleSquares(self, pos):
    return removeInvalid(cardinalDirections(pos, 2))

class Wings(MovementItem):
  def name(self):
    return constants.WINGS
  
  def description(self):
    return constants.WINGS_DESC
  
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

class Mine(Building):
  def name(self):
    return constants.MINE
  
  def description(self):
    return constants.MINE_DESC
  
  def base_price(self):
    return 10
  
  def processTurn(self):
    self.getOwner().sendMoney(1)
    return []

class Shield(DefenseItem):
  def name(self):
    return constants.SHIELD
  
  def description(self):
    return constants.SHIELD_DESC
  
  def base_price(self):
    return 5

  def onDamage(self, player):
    player.setPos(player.getStartingPosition())
    player.setDefense(NoDefense())
    player.setWeapon(NoWeapon())
    player.setMovement(NoMovement())

class UpgradedShield(DefenseItem):
  def name(self):
    return constants.UPGRADED_SHIELD
  
  def description(self):
    return constants.UPGRADED_SHIELD_DESC
  
  def base_price(self):
    return 10

  def onDamage(self, player):
    player.setPos(player.getStartingPosition())
    player.setDefense(NoDefense())