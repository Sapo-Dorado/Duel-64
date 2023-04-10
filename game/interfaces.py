from abc import ABC, abstractmethod
from game.constants import removeInvalid, cardinalDirections
import game.constants as constants

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

  def isBuilding(self):
    return False

  def base_price(self):
    return 0

  def price(self, distance):
    return self.base_price() + self.distanceFee(distance)

  def distanceFee(self, distance):
    return max((distance-1) * constants.DISTANCE_FEE, 0)

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
  
  def info(self):
    return None

  def blocksMovement(self):
    return False

  def isBuilding(self):
    return True

  def onPurchase(self, player, pos):
    if pos is None:
      raise Exception(constants.BUILDING_NEEDS_POS_MSG)
    self.setPos(pos)
    self.setOwner(player)
    
  #Should return the tiles being attacked, if any
  @abstractmethod
  def processTurn(self, gameState):
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
    return constants.NO_WEAPON

  def description(self):
    return constants.NO_WEAPON_DESC

  def attackRange(self, oldPos, newPos):
    return [newPos]

class NoMovement(MovementItem):
  def name(self):
    return constants.NO_MOVEMENT

  def description(self):
    return constants.NO_MOVEMENT_DESC
  
  def getPossibleSquares(self, pos):
    return removeInvalid(cardinalDirections(pos, 1))

class NoDefense(DefenseItem):
  def name(self):
    return constants.NO_DEFENSE
  
  def description(self):
    return constants.NO_DEFENSE_DESC

  def base_price(self):
    return 0
  
  def onDamage(self, player):
    player.kill()

class Player():
  def __init__(self, pos):
    self.weapon = NoWeapon()
    self.defense = NoDefense()
    self.movement = NoMovement()
    self.money = constants.STARTING_MONEY
    self.startingPosition = pos
    self.pos = pos
    self.alive = True
  
  def setWeapon(self, weapon):
    self.weapon = weapon

  def getWeapon(self):
    return self.weapon
  
  def setDefense(self, defense):
    self.defense = defense
  
  def getDefense(self):
    return self.defense

  def setMovement(self, movement):
    self.movement = movement
  
  def getMovement(self):
    return self.movement
  
  def setPos(self, pos):
    self.pos = pos

  def getPos(self):
    return self.pos
  
  def getStartingPosition(self):
    return self.startingPosition
  
  def spend(self, amount):
    if(amount > self.money):
      raise Exception(constants.NOT_ENOUGH_MONEY_MSG)
    self.money -= amount
  
  def sendMoney(self, amount):
    self.money += amount

  def getBalance(self):
    return self.money

  def processMove(self, newPos):
    if(newPos not in self.getPossibleMoves()):
      raise Exception(constants.INVALID_MOVE_MSG)
    oldPos = self.getPos()
    self.setPos(newPos)
    return self.weapon.attackRange(oldPos, newPos)
  
  def getPossibleMoves(self):
    return self.movement.getPossibleSquares(self.getPos())
  
  def getPrices(self, item):
    prices = []
    for x in range(constants.BOARD_SIZE):
      for y in range(constants.BOARD_SIZE):
        itemPos = (x,y)
        itemPrice = item.price(distance(self.getPos(), itemPos))
        if(itemPrice <= self.getBalance()):
          prices.append((itemPos, itemPrice))
    return prices

  
  def processDamage(self):
    self.defense.onDamage(self)

  def kill(self):
    self.alive = False
  
  def isAlive(self):
    return self.alive
    
