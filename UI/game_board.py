import pygame
from UI.constants import *
from game.constants import BOARD_SIZE
from game.state import GameState
import sys

def initializeGrid():
  grid = []
  for i,x in enumerate(range(SIDEBAR_SIZE,WINDOW_WIDTH-SIDEBAR_SIZE,BLOCK_SIZE)):
    grid.append([])
    for y in range(SIDEBAR_SIZE,WINDOW_HEIGHT-SIDEBAR_SIZE,BLOCK_SIZE):
      grid[i].append((x,y))
  return grid

class GameBoardUI:
  def __init__(self, screen):
    self.grid = initializeGrid()
    self.screen = screen
    self.game = GameState()
    self.updateCallbacks = []
    self.eventCallbacks = []
    self.start()


  def clearCallbacks(self):
    self.updateCallbacks = []
    self.eventCallbacks = []

  def writeText(self, coords, text, size):
    font = pygame.font.SysFont('Corbel', size)
    text = font.render(text, True, "black", "beige")
    textRect = text.get_rect()
    textRect.center = coords
    self.screen.blit(text, textRect)

  def drawImage(self, coords, name):
    image = pygame.image.load(name)
    default_image_size = (BLOCK_SIZE * 1.25,BLOCK_SIZE * 1.25)
    image_90 = pygame.transform.scale(image,default_image_size)
    self.screen.blit(image_90, coords)

  def drawGridImage(self, pos ,name):
    x,y = pos
    image = pygame.image.load(name)
    default_image_size = (BLOCK_SIZE-2,BLOCK_SIZE-2)
    image_90 = pygame.transform.scale(image,default_image_size)
    gridX,gridY = self.grid[x][y]
    self.screen.blit(image_90,(gridX+1,gridY+1))

  def drawGrid(self):
    for row in self.grid:
      for x,y in row:
        rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(self.screen, "black", rect, 1)
  
  def gridCenter(self, pos):
    x,y = self.grid[pos[0]][pos[1]]
    return (x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 2)
  
  def withinBlock(self, center, pos):
    maxDistance = BLOCK_SIZE // 2
    return (pos[0] >= center[0] - maxDistance and pos[0] <= center[0] + maxDistance and
        pos[1] >= center[1] - maxDistance and pos[1] <= center[1] + maxDistance)

  def drawPlayer(self, player, playerNum):
    players = [PLAYER1_IMG, PLAYER2_IMG]
    self.drawGridImage(player.getPos(), players[playerNum])
  
  def drawBuilding(self, building):
    self.drawGridImage(building.getPos(), GAME_OBJECTS[building.name()])
  
  def drawMoveButton(self, pos):
    center = self.gridCenter(pos)

    def updateButton():
      mouse = pygame.mouse.get_pos()
      rect = None
      if self.withinBlock(center, mouse):
        rect = pygame.draw.circle(self.screen, (240,230,140), center, PLAYER_RADIUS // 2)
      else:
        rect = pygame.draw.circle(self.screen, "yellow", center, PLAYER_RADIUS // 2)
      pygame.display.update(rect)

    def onEvent(event):
      mouse = pygame.mouse.get_pos()
      if event.type == pygame.MOUSEBUTTONDOWN:
        if self.withinBlock(center, mouse):
          self.game.processMove(pos)
          self.clearCallbacks()
          self.drawGameState()
          return

    self.updateCallbacks.append(updateButton)
    self.eventCallbacks.append(onEvent)

  def drawShop(self):
    shop = self.game.shop
    items = shop.getItems()
    for i,item in enumerate(items):
      x = 10 + ((WINDOW_WIDTH - 20) * i) // len(items)
      self.drawImage((x, SIDEBAR_SIZE // 4), GAME_OBJECTS[items[i].name()])
    self.writeText((WINDOW_WIDTH // 2, SIDEBAR_SIZE // 8), "Shop", 30)

  def drawPlayerInfo(self):
    p1Info = getPlayerItemInfo(self.game.players[0])
    p2Info = getPlayerItemInfo(self.game.players[1])
    sidebarLength = WINDOW_HEIGHT - (2 * SIDEBAR_SIZE)

    for i,info in enumerate(p1Info):
      loc = (SIDEBAR_SIZE // 2, SIDEBAR_SIZE + 100 + i * (100))
      self.writeText(loc, info[0], 24)
      self.writeText((loc[0], loc[1] + 24), info[1], 24)

    for i,info in enumerate(p2Info):
      sidebarLength = WINDOW_HEIGHT - (2 * SIDEBAR_SIZE)
      loc = (WINDOW_WIDTH - (SIDEBAR_SIZE // 2), SIDEBAR_SIZE + 100 + i * (100))
      self.writeText(loc, info[0], 24)
      self.writeText((loc[0], loc[1] + 24), info[1], 24)
    
    lowerMiddle = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - (SIDEBAR_SIZE // 2))
    self.writeText(lowerMiddle, f"Current Player: Player {self.game.curTurn + 1}", 36)


  def printWinner(self):
    self.writeText((WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), self.game.getWinner(), 120)

  def drawGameState(self):
    self.screen.fill("beige")
    if(self.game.getWinner() is not None):
      self.printWinner()
    else:
      self.drawGrid()
      for building in self.game.buildings:
        self.drawBuilding(building)
      for i,player in enumerate(self.game.players):
        self.drawPlayer(player, i)
      for pos in self.game.getPossibleMoves():
        self.drawMoveButton(pos)
      self.drawShop()
      self.drawPlayerInfo()
    pygame.display.flip()
    
  def start(self):
    pygame.display.set_caption(GAME_TITLE)
    self.drawGameState()

  def update(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      for eventFn in self.eventCallbacks:
        eventFn(event)

    for updateFn in self.updateCallbacks:
      updateFn()

