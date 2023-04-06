import pytest
from game.state import *
from game.constants import *
from game.shop import *

def test_setup_generates_proper_board():
  game = GameState()

  assert(game.getWinner() is None)
  assert(len(game.buildings) == 2)
  assert(game.board.getBoardObject(P1_START_POS).name() == MINE)
  assert(game.board.getBoardObject(P2_START_POS).name() == MINE)
  assert(game.currentPlayer() == game.players[0])
  assert(game.currentPlayer().getBalance() == constants.STARTING_MONEY)
  assert(game.currentPlayer().getWeapon().name() == constants.NO_WEAPON)
  assert(game.currentPlayer().getMovement().name() == constants.NO_MOVEMENT)
  assert(game.currentPlayer().getDefense().name() == constants.NO_DEFENSE)

  assert(game.otherPlayer() == game.players[1])
  assert(game.otherPlayer().getBalance() == constants.STARTING_MONEY)
  assert(game.otherPlayer().getWeapon().name() == constants.NO_WEAPON)
  assert(game.otherPlayer().getMovement().name() == constants.NO_MOVEMENT)
  assert(game.otherPlayer().getDefense().name() == constants.NO_DEFENSE)

  game.passTurn()

  assert(game.currentPlayer() == game.players[1])
  assert(game.currentPlayer().getBalance() == constants.STARTING_MONEY + 1)
  assert(game.otherPlayer() == game.players[0])
  assert(game.otherPlayer().getBalance() == constants.STARTING_MONEY + 1)
  assert(game.getWinner() is None)

def test_validatePos():
  game = GameState()
  game.validatePos(P1_START_POS)
  game.validatePos(P2_START_POS)
  with pytest.raises(Exception, match=constants.INVALID_POS_MSG):
    game.validatePos((-1,0))
  with pytest.raises(Exception, match=constants.INVALID_POS_MSG):
    game.validatePos((0, -1))
  with pytest.raises(Exception, match=constants.INVALID_POS_MSG):
    game.validatePos((0, BOARD_SIZE))
  with pytest.raises(Exception, match=constants.INVALID_POS_MSG):
    game.validatePos((BOARD_SIZE, 0))
  with pytest.raises(Exception, match=constants.INVALID_POS_MSG):
    game.validatePos((BOARD_SIZE+10, -10))

def test_getPossibleMoves():
  game = GameState()
  moves = game.getPossibleMoves()
  assert(len(moves) == 2)
  assert((0,1) in moves)
  assert((1,0) in moves)

  game.players[0].setPos((5,5))
  moves = game.getPossibleMoves()
  assert(len(moves) == 4)
  assert((4,5) in moves)
  assert((5,4) in moves)
  assert((5,6) in moves)
  assert((6,5) in moves)

def test_attack_wins_game():
  game = GameState()
  game.otherPlayer().setPos((0,1))
  game.processMove((0,1))
  assert(not game.players[1].isAlive())
  assert(game.getWinner() == constants.P1_WIN_MSG)
  assert(game.currentPlayer() == game.players[1])

def test_attack_destroys_building():
  game = GameState()
  game.otherPlayer().setPos((0,1))
  game.processMove((1,0))
  game.processMove((0,0))
  assert(len(game.buildings) == 1)
  assert(game.buildings[0] == game.board.getBoardObject(P2_START_POS))
  assert(game.getWinner() == constants.P2_WIN_MSG)

def test_weapon_increases_range():
  game = GameState()
  sword = Sword()
  sword.buy(game.currentPlayer(), game.currentPlayer().getPos())
  assert(game.currentPlayer().getBalance() == STARTING_MONEY - sword.base_price())
  assert(game.currentPlayer().getWeapon() == sword)
  game.players[1].setPos((0,2))
  game.processMove((0,1))
  assert(not game.currentPlayer().isAlive())
  assert(game.getWinner() == P1_WIN_MSG)

def test_movement_increases_possible_moves():
  game = GameState()
  game.currentPlayer().setPos((4,4))
  boots = Boots()
  boots.buy(game.currentPlayer(), game.currentPlayer().getPos())
  moves = game.getPossibleMoves()
  assert(len(moves) == 8)

def test_shield():
  game = GameState()
  game.otherPlayer().setPos((0,1))
  shield = Shield()
  shield.buy(game.otherPlayer(), game.otherPlayer().getPos())
  boots = Boots()
  boots.buy(game.otherPlayer(), game.otherPlayer().getPos())
  game.processMove((0,1))
  assert(game.currentPlayer().isAlive())
  assert(game.currentPlayer().getPos() == (P2_START_POS))
  assert(game.currentPlayer().getMovement().name() == NO_MOVEMENT)

def test_upgraded_shield():
  game = GameState()
  game.otherPlayer().money = 100
  game.otherPlayer().setPos((0,1))
  shield = UpgradedShield()
  shield.buy(game.otherPlayer(), game.otherPlayer().getPos())
  boots = Boots()
  boots.buy(game.otherPlayer(), game.otherPlayer().getPos())
  game.processMove((0,1))
  assert(game.currentPlayer().isAlive())
  assert(game.currentPlayer().getPos() == (P2_START_POS))
  assert(game.currentPlayer().getMovement().name() == BOOTS)

def test_invalid_inputs_revert():
  game = GameState()
  game.currentPlayer().money = 0
  boots = Boots()
  with pytest.raises(Exception, match=constants.NOT_ENOUGH_MONEY_MSG):
    boots.buy(game.currentPlayer(), game.currentPlayer().getPos())
  with pytest.raises(Exception, match=INVALID_MOVE_MSG):
    game.processMove((5,5))

def test_shop():
  game = GameState()
  assert(len(game.getShopItems()) == 8)
  item1 = game.extractItem(3)
  item2 = game.extractItem(3)
  assert(item1.name() == item2.name())
  assert(item1 is not item2)

def test_spike_attack():
  game = GameState()
  game.currentPlayer().sendMoney(50)
  trap = SpikeTrap()
  game.processBuy(trap, (P2_START_POS[0],P2_START_POS[0]-1))
  assert(game.currentPlayer().isAlive())
  assert(game.getWinner() == None)
  game.passTurn()
  assert(not game.otherPlayer().isAlive())
  assert(game.getWinner() == P1_WIN_MSG)
