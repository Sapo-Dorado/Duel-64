STARTING_MONEY=10
DISTANCE_FEE=1
BOARD_SIZE = 8
P1_START_POS = (0,0)
P2_START_POS = (BOARD_SIZE-1, BOARD_SIZE-1)
WINNING_BALANCE=50

def valid_position(pos):
  for idx in pos:
    if(idx < 0 or idx >= BOARD_SIZE):
      return False
  return True


SHIELD = "Shield"
UPGRADED_SHIELD = "Upgraded Shield"
MINE = "Mine"
MONEY_TREE = "Money Tree"
BARRIER = "Barrier"
SPIKE_TRAP = "Spike Trap"
