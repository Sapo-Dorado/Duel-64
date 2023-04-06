from game.shop import *

def test_sword():
  sword = Sword()
  range1 = sword.attackRange((0,0),(0,1))
  assert(len(range1) == 2)
  assert((0,1) in range1)
  assert((0,2) in range1)

  range2 = sword.attackRange((2,2),(1,2))
  assert(len(range2) == 2)
  assert((0,2) in range2)
  assert((1,2) in range2)

  range3 = sword.attackRange((0,1),(0,0))
  assert(len(range3) == 1)
  assert((0,0) in range3)

  range4 = sword.attackRange((2,2),(3,3))
  assert(len(range4) == 2)
  assert((3,3) in range4)
  assert((4,4) in range4)

def test_throwing_star():
  star = ThrowingStar()
  range1 = star.attackRange((0,0),(0,1))
  assert(len(range1) == 3)
  assert((0,0) in range1)
  assert((0,1) in range1)
  assert((1,2) in range1)

  range2 = star.attackRange((2,2),(1,2))
  assert(len(range2) == 5)
  assert((3,2) in range2)
  assert((2,2) in range2)
  assert((1,2) in range2)
  assert((0,1) in range2)
  assert((0,3) in range2)

  range3 = star.attackRange((2,2),(3,3))
  assert(len(range3) == 5)
  assert((1,1) in range3)
  assert((2,2) in range3)
  assert((3,3) in range3)
  assert((4,3) in range3)
  assert((3,4) in range3)

def test_boots():
  boots = Boots()
  range1 = boots.getPossibleSquares((4,4))
  assert(len(range1) == 8)
  assert((5,4) in range1)
  assert((6,4) in range1)
  assert((4,5) in range1)
  assert((4,6) in range1)
  assert((4,3) in range1)
  assert((4,2) in range1)
  assert((3,4) in range1)
  assert((2,4) in range1)

  range2 = boots.getPossibleSquares((0,0))
  assert(len(range2) == 4)
  assert((0,1) in range2)
  assert((0,2) in range2)
  assert((1,0) in range2)
  assert((2,0) in range2)

def test_wings():
  wings = Wings()
  range1 = wings.getPossibleSquares((4,4))
  assert(len(range1) == 12)
  assert((5,5) in range1)
  assert((3,3) in range1)
  assert((3,5) in range1)
  assert((5,3) in range1)
  assert((5,4) in range1)
  assert((6,4) in range1)
  assert((4,5) in range1)
  assert((4,6) in range1)
  assert((4,3) in range1)
  assert((4,2) in range1)
  assert((3,4) in range1)
  assert((2,4) in range1)

  range2 = wings.getPossibleSquares((0,0))
  assert(len(range2) == 5)
  assert((0,1) in range2)
  assert((1,1) in range2)
  assert((0,2) in range2)
  assert((1,0) in range2)
  assert((2,0) in range2)

def test_spike_trap():
  spike = SpikeTrap()
  spike.activated = True
  spike.setPos((4,4))
  range1 = spike.processTurn()
  assert(len(range1) == 4)
  assert((5,4) in range1)
  assert((4,5) in range1)
  assert((4,3) in range1)
  assert((3,4) in range1)

  spike.setPos((0,0))
  range2 = spike.processTurn()
  assert(len(range2) == 2)
  assert((0,1) in range2)
  assert((1,0) in range2)

