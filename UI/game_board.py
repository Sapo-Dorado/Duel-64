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
    text = font.render(text, True,TEXT_COLOR, BACKGROUND_COLOR)
    textRect = text.get_rect()
    textRect.center = coords
    return self.screen.blit(text, textRect)

  def drawImage(self, coords, name, size):
    image = pygame.image.load(name)
    image_90 = pygame.transform.scale(image,(size,size))
    return self.screen.blit(image_90, coords)

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
        pygame.draw.rect(self.screen,TEXT_COLOR, rect, 1)
  
  def gridCenter(self, pos):
    x,y = self.grid[pos[0]][pos[1]]
    return (x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 2)
  
  def withinBlock(self, center, pos, maxDistance):
    return (pos[0] >= center[0] - maxDistance and pos[0] <= center[0] + maxDistance and
        pos[1] >= center[1] - maxDistance and pos[1] <= center[1] + maxDistance)

  def drawPlayer(self, player, playerNum):
    players = [PLAYER1_IMG, PLAYER2_IMG]
    self.drawGridImage(player.getPos(), players[playerNum])
  
  def drawBuilding(self, building):
    self.drawGridImage(building.getPos(), GAME_OBJECTS[building.name()])
  
  def drawMoveButton(self, pos):
    center = self.gridCenter(pos)

    prevRect = None
    def updateButton():
      nonlocal prevRect
      mouse = pygame.mouse.get_pos()
      rect = None
      curRect = None
      if self.withinBlock(center, mouse, BLOCK_SIZE // 2):
        rect = pygame.draw.circle(self.screen, (240,230,140), center, PLAYER_RADIUS // 2)
        curRect = 0
      else:
        rect = pygame.draw.circle(self.screen, "yellow", center, PLAYER_RADIUS // 2)
        curRect = 1
      if(prevRect != curRect):
        prevRect = curRect
        pygame.display.update(rect)

    def onEvent(event):
      if event.type == pygame.MOUSEBUTTONDOWN:
        mouse = pygame.mouse.get_pos()
        if self.withinBlock(center, mouse, BLOCK_SIZE // 2):
          self.game.processMove(pos)
          self.clearCallbacks()
          self.drawGameState()

    self.updateCallbacks.append(updateButton)
    self.eventCallbacks.append(onEvent)

  def drawShop(self):
    self.writeText((WINDOW_WIDTH // 2, SIDEBAR_SIZE // 8), "Shop", 30)

    shop = self.game.shop
    items = shop.getItems()
    imgSize = BLOCK_SIZE * 1.25
    textSize = 18
    descriptionCenter = (WINDOW_WIDTH // 2, 7 * SIDEBAR_SIZE // 8)
    prevItem = [1 for i in items]

    def writeDescription(description=None):
      cover = pygame.draw.rect(self.screen, BACKGROUND_COLOR, pygame.Rect(0,descriptionCenter[1] - textSize // 2 - 1, WINDOW_WIDTH, textSize + 2))

      text = self.writeText(descriptionCenter, description, textSize)
      pygame.display.update([cover, text])

    def leftCorner(i):
      return (10 + ((WINDOW_WIDTH - 20) * i) // len(items), SIDEBAR_SIZE // 4)
    
    def center(i):
      corner = leftCorner(i)
      return (corner[0] + imgSize // 2, corner[1] + imgSize // 2)


    def updateButtons():
      mouse = pygame.mouse.get_pos()
      hoveredItem = False
      stateChange = False
      for i,item in enumerate(items):
        if self.withinBlock(center(i), mouse, imgSize // 2):
          if(prevItem[i] != 1):
            rect = pygame.draw.circle(self.screen, "yellow", center(i), imgSize // 2)
            pygame.display.update(rect)
            writeDescription(f"{item.name()}: {item.description()}")
            prevItem[i] = 1
            stateChange = True
            hoveredItem = True
        elif prevItem[i] != 0:
          rect = self.drawImage(leftCorner(i), GAME_OBJECTS[item.name()], imgSize)
          pygame.display.update(rect)
          prevItem[i] = 0
          stateChange = True
      if stateChange and not hoveredItem:
        writeDescription()
  
    def onEventGenerator(i, item):
      def onEvent(event):
        if event.type == pygame.MOUSEBUTTONDOWN:
          mouse = pygame.mouse.get_pos()
          if self.withinBlock(center(i), mouse, imgSize // 2):
            self.clearCallbacks()
            self.drawBuyScreen(item)
      return onEvent

    self.updateCallbacks.append(updateButtons)
    for i, item in enumerate(items):
      self.eventCallbacks.append(onEventGenerator(i, item))
      
        

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

  def drawBuyScreen(self, item):
    print("buying time")

  def drawGameState(self):
    self.screen.fill( BACKGROUND_COLOR)
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

