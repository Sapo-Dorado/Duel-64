from abc import ABC, abstractmethod
from game.constants import STARTING_MONEY, DISTANCE_FEE

def distance(pos1, pos2):
  return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

class ShopObject(ABC):
  @abstractmethod
  def name(self):
    pass

  @abstractmethod
  def description(self):
    pass

  @abstractmethod
  def onPurchase(self, player):
    pass

  def base_price(self):
    return 0

  def price(self, distance=0):
    return self.base_price() + distanceFee(distance)

  def distanceFee(self, distance):
    return max((distance-1) * DISTANCE_FEE, 0)

  def buy(self, player, pos):
    player.spend(self.price(distance(player.getPos(), pos)))
    self.onPurchase(player, pos)

class Building(ShopObject):
  def __init__(self, owner=None, pos=None):
    self.owner = owner
    self.pos = pos

  def setOwner(self, owner):
    self.owner = owner

  def getOwner(self):
    return self.owner
  
  def setPos(self, pos):
    self.pos = pos

  def getPos(self):
    return self.pos
  
  def vulnerable(self, player):
    return player != self.owner

  def onPurchase(self, player, pos):
    if pos is None:
      raise Exception("Building must be placed at a position")
    self.setPos(pos)
    self.setOwner(player)
    
  @abstractmethod
  def processTurn(self):
    pass

class WeaponItem(ShopObject):
  def onPurchase(self, player, pos):
    player.setWeapon(self)

  @abstractmethod
  def attackRange(self, oldPos, newPos):
    pass

class DefenseItem(ShopObject):
  def onPurchase(self, player, pos):
    player.setDefense(self)
  
  @abstractmethod
  def onDamage(self, player):
    pass

class MovementItem(ShopObject):
  def onPurchase(self, player, pos):
    player.setMovement(self)

  @abstractmethod
  def getPossibleSquares(self, pos):
    pass

class NoWeapon(WeaponItem):
  def name(self):
    return "No Weapon"

  def description(self):
    return ""

  def attackRange(self, oldPos, newPos):
    return [newPos]

class NoMovement(MovementItem):
  def name(self):
    return "No Movement Item"

  def description(self):
    return ""
  
  def getPossibleSquares(self, pos):
    return removeInvalid(cardinalDirections(pos, 1))

class NoDefense(DefenseItem):
  def name(self):
    return "No Defensive Item"
  
  def description(self):
    return ""

  def base_price(self):
    return 0
  
  def onDamage(self, player):
    player.kill()

class Player():
  def __init__(self, pos):
    self.weapon = NoWeapon()
    self.defense = NoDefense()
    self.movement = NoMovement()
    self.money = STARTING_MONEY
    self.pos = pos
    self.alive = True
  
  def setWeapon(self, weapon):
    self.weapon = weapon
  
  def setDefense(self, defense):
    self.defense = defense
  
  def setMovement(self, movement):
    self.movement = movement
  
  def setPos(self, pos):
    self.pos = pos

  def getPos(self):
    return self.pos
  
  def spend(self, amount):
    if(amount > self.money):
      raise Exception("Insufficient Funds")
    self.money -= amount
  
  def sendMoney(self, amount):
    self.money += amount

  def getBalance(self):
    return self.money

  def processMove(self, newPos):
    if(newPos not in self.getPossibleMoves()):
      raise Exception("Invalid move")
    oldPos = self.getPos()
    self.setPos(newPos)
    return self.weapon.attackRange(oldPos, newPos)
  
  def getPossibleMoves(self):
    return self.movement.getPossibleSquares(self.getPos())
  
  def processDamage(self):
    self.defense.onDamage(self)

  def kill(self):
    self.alive = False
  
  def isAlive(self):
    return self.alive
    
