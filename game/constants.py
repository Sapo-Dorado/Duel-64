STARTING_MONEY=10
DISTANCE_FEE=1
BOARD_SIZE = 8
P1_START_POS = (0,0)
P2_START_POS = (BOARD_SIZE-1, BOARD_SIZE-1)
WINNING_BALANCE=50

def cardinalDirections(pos, distance):
  x,y = pos
  result = []
  for i in range(1,distance+1):
    result.append((x+i,y))
    result.append((x-i,y))
    result.append((x,y+i))
    result.append((x,y-i))

  return result

def validPosition(pos):
  for idx in pos:
    if(idx < 0 or idx >= BOARD_SIZE):
      return False
  return True

def removeInvalid(posList):
  return list(filter(validPosition, posList))

INVALID_POS_MSG = "Invalid position"
P1_WIN_MSG = "Player 1"
P2_WIN_MSG = "Player 2"
TIE_MSG = "Tie"
BUILDING_NEEDS_POS_MSG = "Building must be placed at a position"
NOT_ENOUGH_MONEY_MSG = "Insufficient funds"
INVALID_MOVE_MSG = "Invalid Move"

NO_WEAPON = "No Weapon"
NO_WEAPON_DESC = ""
NO_MOVEMENT = "No Movement Item"
NO_MOVEMENT_DESC = ""
NO_DEFENSE = "No Defense Item"
NO_DEFENSE_DESC = ""
SWORD = "Sword"
SWORD_DESC = "Increases attack range to include one additional block in the direction of movement."
THROWING_STAR = "Throwing Star"
THROWING_STAR_DESC = "Attacks in a Y shape pointing in the direction of movement. This adds two additional squares of range diagonally in front of you, and two in a straight line behind you."
BOOTS = "Boots"
BOOTS_DESC = "Increases potential movement range by one square in each cardinal direction."
WINGS = "Wings"
WINGS_DESC = "Increases potential movement range by one square in each cardinal direction and one square in each diagonal direction."
MINE = "Mine"
MINE_DESC = "Produces one gold per turn"
SHIELD = "Shield"
SHIELD_DESC = "Saves you from one killing blow. Sends you back to your starting location. You lose all of your items"
UPGRADED_SHIELD = "Upgraded Shield"
UPGRADED_SHIELD_DESC = "Saves you from one killing blow. Sends you back to your starting location. You keep your other items"
SPIKE_TRAP = "Spike Trap"
SPIKE_TRAP_DESC = "Attacks enemies and enemy buildings within one square in all four cardinal directions. Doesn't attack the turn it is played"
MONEY_TREE = "Money Tree"
MONEY_TREE_DESC = "After 5 turns, produce 10 gold and self destruct. Goes out with a bang!"
BARRIER = "Barrier"
