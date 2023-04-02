from abc import ABC
from constants import STARTING_MONEY

class ShopObject(ABC):
  @abstractmethod
  def price(self):
    pass

  @abstractmethod
  def onPurchase(self, player):
    pass
  
  def buy(self, player):
    player.spend(self.price())
    self.onPurchase(player)

class BoardObject(ABC):
  def setPos(self, pos):
    self.pos = pos

  def getPos(self):
    return self.pos

class Building(BoardObject, ShopObject):
  def __init__(self):
    self.owner = None
    self.setPos(None)

  def onPurchase(self, player):
    self.owner = player
    
  @abstractmethod
  def processTurn(self):
    pass

class WeaponItem(ShopObject):
  def onPurchase(self, player):
    player.setWeapon(self)

  @abstractmethod
  def onAttack(self, pos):
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
  def getPossibleSquares(pos):
    pass

class Player(BoardObject):
  def __init__(self, pos):
    self.weapon = None
    self.defense = None
    self.movement = None
    self.money = STARTING_MONEY
    self.setPos(pos)
  
  def setWeapon(self, weapon):
    self.weapon = weapon
  
  def setDefense(self, defense):
    self.defense = defense
  
  def setMovement(self, movement):
    self.movement = movement
  
  def spend(self, amount):
    if(amount > self.money):
      raise Exception("Insufficient Funds")
    self.money -= amount

