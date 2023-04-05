from game.interfaces import Player
from game.constants import P1_START_POS, P2_START_POS, BOARD_SIZE, WINNING_BALANCE, valid_position
from game.shop import Mine

class Board:
  def __init__(self):
    self.boardObjects = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

  def getBoardObject(self, pos):
    x,y = pos
    return self.boardObjects[x][y]
  
  def addBoardObject(self, obj, pos, buildings):
    x,y = pos
    if self.boardObjects[x][y] is not None:
      buildings.remove(self.boardObjects[x][y])
    self.boardObjects[x][y] = obj
    buildings.append(obj)
        
  def attackTile(self, player, pos, buildings):
      if not self.getBoardObject(pos).vulnerable(player):
        x,y = pos
        if self.boardObjects[x][y] is not None:
          buildings.remove(self.boardObjects[x][y])
        self.boardObjects[x][y] = None

class GameState:
  def __init__(self):
    self.players = (Player(P1_START_POS), Player(P2_START_POS))
    self.board = Board()
    self.buildings = []
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
      attackedTiles = building.processTurn()
      self.attackTiles(attackedTiles)

  def getBoard(self):
    return self.board
  
  def attackTiles(self, tiles):
    for tile in tiles:
      otherPlayer = self.otherPlayer()
      if tile == otherPlayer.getPos():
        otherPlayer.processDamage()
      self.board.attackTile(curPlayer, tile, self.buildings)


  def getPossibleMoves(self):
    return self.currentPlayer().getPossibleMoves()
  
  def processMove(self, pos):
    self.validatePos(pos)
    curPlayer = self.currentPlayer()
    attackedTiles = curPlayer.processMove(pos)
    self.attackTiles(attackedTiles)
    self.passTurn()
  
  def processBuy(self, shopObj, pos=None):
    if pos is not None:
      self.validatePos(pos)

    shopObj.buy(self.currentPlayer(), pos)
    self.board.addBoardObject(shopObj, pos, self.buildings)
    self.passTurn()
  
  def checkWin():
    p1HasBuilding = False
    p2HasBuilding = False
    for building in self.buildings:
      if(building.getOwner() == self.players[0]):
        p1HasBuilding = True
      if(building.getOwner() == self.players[1]):
        p2HasBuilding = True

    p1Win = False
    p2Win = False
    if not self.players[1].isAlive() or not p2HasBuilding or self.players[0].getBalance >= WINNING_BALANCE:
      p1Win = True
    if not self.players[0].isAlive() or not p1HasBuilding or self.players[1].getBalance >= WINNING_BALANCE:
      p2Win = True
    if p1Win and p2Win:
      self.winner = "Tie"
      return True
    elif p1Win:
      self.winner = "Player 1"
      return True
    elif p2Win:
      self.winner = "Player 2"
      return True
    return False
  
  def getWinner():
    return self.winner
  
  def validatePos(pos):
    if not valid_position(pos):
      raise Exception("Invalid position")

  