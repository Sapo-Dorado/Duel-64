from interfaces import Player, BoardObject
from constants import P1_START_POS, P2_START_POS, BOARD_SIZE

class Board:
  def __init__(self, players):
    self.boardObjects = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

  def getBoardObject(self, pos):
    x,y = pos
    return self.boardObjects[x][y]
  
  def addBoardObject(self, obj, pos):
    x,y = pos
    self.boardObjects[x][y] = obj
        
  def attackTile(self, player, pos):
      if not self.getBoardObject(pos).vulnerable(player):
        x,y = pos
        self.boardObjects[x][y] = None

class GameState:
  def __init__(self):
    self.players = (Player(P1_START_POS), Player(P2_START_POS))
    self.board = Board()
    self.buildings = []
    self.curTurn = 0

  def currentPlayer(self):
    return self.players[self.curTurn]
  
  def passTurn(self):
    self.curTurn = abs(self.curTurn - 1)

  def getBoard(self):
    return self.board
  
  def processMove(self, pos):
    self.validatePos(pos)
    attackedTiles = self.currentPlayer().processMove(pos)
    for tile in attackedTiles:
      self.board.attackTile(tile)
    self.passTurn()
  
  def processBuy(self, shopObj, pos):
    self.validatePos(pos)
    shopObj.buy(self.currentPlayer(), self.distance(self.currentPlayer().getPos(), pos))
    self.board.addBoardObject(shopObj, pos)
    self.passTurn()

  def distance(self, pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
  
  def validatePos(pos):
    for idx in pos:
      if(idx < 0 or idx >= BOARD_SIZE):
        raise Exception("Invalid position")

  