import pygame
from UI.constants import *
from game.constants import BOARD_SIZE
from game.state import GameState

def initializeGrid():
  grid = []
  for i,x in enumerate(range(0,WINDOW_WIDTH,BLOCK_SIZE)):
    grid.append([])
    for y in range(0,WINDOW_HEIGHT,BLOCK_SIZE):
      grid[i].append((x,y))
  return grid

class GameBoardUI:
  def __init__(self, screen):
    self.grid = initializeGrid()
    self.screen = screen
    self.game = GameState()
    self.updateCallbacks = []
    self.eventCallbacks = []
    self.drawGameState()

  def clearCallbacks(self):
    self.updateCallbacks = []
    self.eventCallbacks = []

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
    colors = ["grey", (100,100,100)]
    pygame.draw.circle(self.screen, colors[playerNum], self.gridCenter(player.getPos()), PLAYER_RADIUS)
  
  def drawBuilding(self, building):
    xPos,yPos = building.getPos()
    x,y = self.grid[xPos][yPos]
    rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(self.screen, "red", rect)
  
  def drawMoveButton(self, pos):
    center = self.gridCenter(pos)

    def updateButton():
      mouse = pygame.mouse.get_pos()
      if self.withinBlock(center, mouse):
        pygame.draw.circle(self.screen, (240,230,140), center, PLAYER_RADIUS // 2)
      else:
        pygame.draw.circle(self.screen, "yellow", center, PLAYER_RADIUS // 2)

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



  def drawGameState(self):
    self.screen.fill("beige")
    self.drawGrid()
    for building in self.game.buildings:
      self.drawBuilding(building)
    for i,player in enumerate(self.game.players):
      self.drawPlayer(player, i)
    for pos in self.game.getPossibleMoves():
      self.drawMoveButton(pos)
    pygame.display.flip()
    
  def update(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      for eventFn in self.eventCallbacks:
        eventFn(event)

    for updateFn in self.updateCallbacks:
      updateFn()
    pygame.display.update()

