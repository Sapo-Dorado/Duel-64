from game.interfaces import WeaponItem, DefenseItem, MovementItem, Building, NoDefense, NoMovement, NoWeapon
from game.constants import removeInvalid, cardinalDirections, getDir
import game.constants as constants

class BasicShop:
  def __init__(self):
    self.items = [Sword(), ThrowingStar(), Boots(), Wings(), Shield(), UpgradedShield(), Mine(), MoneyTree(), SpikeTrap(), Barrier()]
    self.constructors = [Sword, ThrowingStar, Boots, Wings, Shield, UpgradedShield, Mine, MoneyTree, SpikeTrap, Barrier]
  
  def extractItem(self, idx):
    item = self.items[idx]
    self.items[idx] = self.constructors[idx]()
    return item
  
  def getItems(self):
    return self.items

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

class Mine(Building):
  def name(self):
    return constants.MINE
  
  def description(self):
    return constants.MINE_DESC
  
  def base_price(self):
    return 10
  
  def processTurn(self, gameState):
    if(self.getOwner() == gameState.currentPlayer()):
      self.getOwner().sendMoney(1)
    return []

class SpikeTrap(Building):
  def name(self):
    return constants.SPIKE_TRAP
  
  def description(self):
    return constants.SPIKE_TRAP_DESC
  
  def base_price(self):
    return 5
  
  def onPurchase(self, player, pos):
    super().onPurchase(player, pos)
    self.activated = False

  def processTurn(self, gameState):
    if(self.activated):
      return removeInvalid(cardinalDirections(self.getPos(), 1))
    else:
      self.activated = True
      return []

class MoneyTree(Building):
  def name(self):
    return constants.MONEY_TREE
  
  def description(self):
    return constants.MONEY_TREE_DESC
  
  def base_price(self):
    return 5

  def info(self):
    return str(self.turnCount)

  def onPurchase(self, player, pos):
    super().onPurchase(player, pos)
    self.turnCount = 5
  
  def vulnerable(self, player):
    if(self.turnCount > 0):
      return super().vulnerable(player)
    return True
  
  def processTurn(self, gameState):
    if(self.getOwner() == gameState.currentPlayer()):
      self.turnCount -= 1
      if(self.turnCount <= 0):
        self.getOwner().sendMoney(10)
        targets = cardinalDirections(self.getPos(), 1)
        x,y = self.getPos()
        targets.append((x,y))
        targets.append((x+1,y+1))
        targets.append((x+1,y-1))
        targets.append((x-1,y+1))
        targets.append((x-1,y-1))
        return removeInvalid(targets)
    return []

class Barrier(Building):
  def name(self):
    return constants.BARRIER
  
  def description(self):
    return constants.BARRIER_DESC
  
  def base_price(self):
    return 3
  
  def distanceFee(self, distance):
    return 0

  def vulnerable(self, player):
    return False
  
  def blocksMovement(self):
    return True
  
  def countsForWin(self):
    return False
  
  def processTurn(self, gameState):
    return []
  
