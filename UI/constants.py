import game.constants as game_constants
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 960
SIDEBAR_SIZE = 180
BLOCK_SIZE = 75
PLAYER_RADIUS = 35
GAME_TITLE="Good Game"

BASE_PATH = "./UI/images/"
PLAYER1_IMG = BASE_PATH + "blueberry.png"
PLAYER2_IMG = BASE_PATH + "watermelon.png"

GAME_OBJECTS = {
  game_constants.SWORD: BASE_PATH + "moneymaker.png",
  game_constants.THROWING_STAR: BASE_PATH + "moneymaker.png",
  game_constants.BOOTS: BASE_PATH + "moneymaker.png",
  game_constants.WINGS: BASE_PATH + "moneymaker.png",
  game_constants.MINE: BASE_PATH + "moneymaker.png",
  game_constants.SHIELD: BASE_PATH + "moneymaker.png",
  game_constants.UPGRADED_SHIELD: BASE_PATH + "moneymaker.png",
  game_constants.SPIKE_TRAP: BASE_PATH + "moneymaker.png",
  game_constants.MONEY_TREE: BASE_PATH + "moneytree.jpeg",
  game_constants.BARRIER: BASE_PATH + "moneymaker.png"
}

def getPlayerItemInfo(player):
  return [
    ("Player", "1" if player.getStartingPosition() == game_constants.P1_START_POS else "2"),
    ("Balance:",  str(player.getBalance())),
    ("Weapon:", player.getWeapon().name()),
    ("Movement Item:", player.getMovement().name()),
    ("Defense Item:", player.getDefense().name())
  ]
