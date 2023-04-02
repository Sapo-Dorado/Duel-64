from abc import ABC, abstractmethod
from constants import STARTING_MONEY, DISTANCE_FEE

class ShopObject(ABC):
  @abstractmethod
  def price(self, distance):
    pass

  @abstractmethod
  def onPurchase(self, player):
    pass

  def distanceFee(self, distance):
    return distance * DISTANCE_FEE

  def buy(self, player, distance):
    player.spend(self.price(distance))
    self.onPurchase(player)

class BoardObject(ABC):
  def __init__(self):
    self.owner = None
    self.pos = None

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

class Building(BoardObject, ShopObject):
  def onPurchase(self, player):
    self.owner = player
    
  @abstractmethod
  def processTurn(self):
    pass

class WeaponItem(ShopObject):
  def onPurchase(self, player):
    player.setWeapon(self)

  @abstractmethod
  def attackRange(self, pos):
    pass

class DefenseItem(ShopObject):
  def onPurchase(self, player):
    player.setDefense(self)
  
  @abstractmethod
  def onDamage(self, pos):
    pass

class MovementItem(ShopObject):
  def onPurchase(self, player):
    player.setMovement(self)

  @abstractmethod
  def getPossibleSquares(self, pos):
    pass

class Player():
  def __init__(self, pos):
    self.weapon = None
    self.defense = None
    self.movement = None
    self.money = STARTING_MONEY
    self.pos = pos
  
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

  def processMove(self, pos):
    if(pos not in self.movement.getPossibleSquares(pos)):
      raise Exception("Invalid move")
    self.setPos(pos)
    return self.weapon.attackRange(pos)
    
