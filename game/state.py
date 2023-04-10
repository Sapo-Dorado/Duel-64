from game.interfaces import Player
from game.constants import validPosition
import game.constants as constants
from game.shop import Mine, BasicShop

class Board:
  def __init__(self):
    self.boardObjects = [[None for _ in range(constants.BOARD_SIZE)] for _ in range(constants.BOARD_SIZE)]

  def getBoardObject(self, pos):
    x,y = pos
    return self.boardObjects[x][y]
  
  def addBoardObject(self, obj, pos, buildings):
    x,y = pos
    if self.boardObjects[x][y] is not None:
      buildings.remove(self.boardObjects[x][y])
    self.boardObjects[x][y] = obj
    buildings.append(obj)
  
  def blocksMovement(self, pos):
    obj = self.getBoardObject(pos)
    return obj is not None and obj.blocksMovement()
        
  def attackTile(self, player, pos, buildings):
    obj = self.getBoardObject(pos)
    if obj is not None and obj.vulnerable(player):
      x,y = pos
      buildings.remove(obj)
      self.boardObjects[x][y] = None

class GameState:
  def __init__(self):
    self.players = (Player(constants.P1_START_POS), Player(constants.P2_START_POS))
    self.board = Board()
    self.buildings = []
    self.shop = BasicShop()
    self.curTurn = 0
    self.winner = None

    for player in self.players:
      pos = player.getPos()
      mine = Mine(player, pos)
      self.board.addBoardObject(mine, pos, self.buildings)

  def currentPlayer(self):
    return self.players[self.curTurn]

  def otherPlayer(self):
    return self.players[abs(self.curTurn-1)]
  
  def passTurn(self):
    self.processBuildings()
    self.curTurn = abs(self.curTurn - 1)
    return self.checkWin()
  
  def processBuildings(self):
    for building in self.buildings:
      attackedTiles = building.processTurn(self)
      self.attackTiles(attackedTiles, building.getOwner())

  def getBoard(self):
    return self.board
  
  def attackTiles(self, tiles, player):
    otherPlayer = self.players[1] if player is self.players[0] else self.players[0]
    for tile in tiles:
      if tile == otherPlayer.getPos():
        otherPlayer.processDamage()
      self.board.attackTile(player, tile, self.buildings)

  def getShopItems(self):
    return self.shop.getItems()
  
  def extractItem(self, idx):
    return self.shop.extractItem(idx)

  def getPossibleMoves(self):
    if self.winner is not None:
      return []
    moves = self.currentPlayer().getPossibleMoves()
    result = []
    for move in moves:
      if self.validMovementPos(move):
        result.append(move)
    return result
  
  def processMove(self, pos):
    if self.winner is not None:
      return
    self.validateMovementPos(pos)
    curPlayer = self.currentPlayer()
    attackedTiles = curPlayer.processMove(pos)
    self.attackTiles(attackedTiles, curPlayer)
    self.passTurn()
  
  def processBuy(self, i, pos=None):
    if self.winner is not None:
      return
    currentPlayer = self.currentPlayer()
    shopObj = self.shop.extractItem(i)
    if pos is not None:
      self.validateBuyPos(pos, shopObj)
      shopObj.buy(currentPlayer, pos)
      self.board.addBoardObject(shopObj, pos, self.buildings)
    else:
      shopObj.buy(currentPlayer, currentPlayer.getPos())
    self.passTurn()
  
  def processConcede(self):
    if(len(self.getPossibleMoves()) > 0):
      raise Exception("Can't concede")
    self.winner = constants.P2_WIN_MSG if self.currentPlayer() is self.players[0] else constants.P1_WIN_MSG
    self.passTurn()
  
  def checkWin(self):
    p1HasBuilding = False
    p2HasBuilding = False
    for building in self.buildings:
      if(building.getOwner() == self.players[0]):
        p1HasBuilding = True
      if(building.getOwner() == self.players[1]):
        p2HasBuilding = True

    p1Win = False
    p2Win = False
    if (not self.players[1].isAlive() or
        not p2HasBuilding or
        self.players[0].getBalance() >= constants.WINNING_BALANCE):
      p1Win = True
    if (not self.players[0].isAlive() or
        not p1HasBuilding or
        self.players[1].getBalance() >= constants.WINNING_BALANCE):
      p2Win = True
    if p1Win and p2Win:
      self.winner = constants.TIE_MSG
      return True
    elif p1Win:
      self.winner = constants.P1_WIN_MSG
      return True
    elif p2Win:
      self.winner = constants.P2_WIN_MSG
      return True
    return False
  
  def getPrices(self, item):
    result = []
    for price in self.currentPlayer().getPrices(item):
      pos, _ = price
      if(self.validBuyPos(pos, item)):
        result.append(price)
    return result

  def getWinner(self):
    return self.winner
  
  def validMovementPos(self, pos):
    return validPosition(pos) and not self.board.blocksMovement(pos)

  def validateMovementPos(self, pos):
    if not self.validMovementPos(pos):
      raise Exception(constants.INVALID_POS_MSG)

  def validBuyPos(self, pos, item):
    return validPosition(pos) and not (item.blocksMovement() and (self.board.getBoardObject(pos) is not None or self.otherPlayer().getPos() == pos))

  def validateBuyPos(self, pos, item):
    if not self.validBuyPos(pos, item) :
      raise Exception(constants.INVALID_POS_MSG)
  

  