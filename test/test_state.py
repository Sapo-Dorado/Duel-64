from game.state import GameState

def test_setup_generates_proper_board():
  game = GameState()
  assert(len(game.buildings) == 2)
