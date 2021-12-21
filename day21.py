import unittest
import itertools
from typing import *
from functools import *


Dice = Callable[[], int]

Player = Tuple[int, int]  # position, score
GameState = Tuple[List[Player], int, int] # players, dice, nextPlayer, turns
GameState2 = Tuple[List[Player], int, int] # players, dice, nextPlayer, turns

BranchGameState = Tuple[int]

def diceSumChances(sides=3, rolls=3):
    diceRange = list(range(1, sides+1))
    rollSets = set(itertools.combinations(diceRange*rolls, rolls))
    totals = [sum(l) for l in rollSets]
    return {
        n: totals.count(n)
        for n in set(totals)
    }

def makePlayer(startPos: int) -> Player:
    return (startPos, 0)

PLAYERS = 0
NEXTPLAYER = 1
TURNS = 2
def makeGame(positions) -> GameState:
    players = [makePlayer(pos) for pos in positions]
    return (players, 0, 0)

def makeBranchingGame(positions) -> BranchGameState:
    diceChances = diceSumChances(3, 3)
    return

def addBranchStep(game: BranchGameState) -> BranchGameState:
    pass

def makeD100() -> Dice:
    it = itertools.cycle(range(1,100 + 1))
    return lambda: next(it)

def playTurn(game: GameState, dice: Dice) -> GameState:
    (players, nextPlayer, turns) = game
    players = players[:]
    roll = dice() + dice() + dice()
    player = players[nextPlayer]
    players[nextPlayer] = movePlayer(player, roll)
    return (
        players,
        (nextPlayer + 1) % len(players),
        turns + 1
    )

def movePlayer(player: Player, roll: int) -> Player:
    boardSize = 10
    position, score = player
    newPosition = (position + roll)
    while newPosition > boardSize:
        newPosition -= boardSize
    return (
        newPosition,
        score + newPosition,
    )

def playTurns(game: GameState, turns: int) -> GameState:
    dice = makeD100()
    for i in range(turns):
        game = playTurn(game, dice)
    return game

def playUntil(game: GameState, shouldEnd: Callable[[GameState], bool]) -> GameState:
    dice = makeD100()
    while not shouldEnd(game):
        game = playTurn(game, dice)
    return game

class Tests(unittest.TestCase):
    def test_one_turn(self):
        game = makeGame([4,8])
        dice = makeD100()
        game2 = playTurn(game, dice)
        self.assertEqual(game[NEXTPLAYER] + 1, game2[NEXTPLAYER])
        self.assertEqual(1, game2[TURNS])

    def test_four_turns(self):
        game = makeGame([4,8])
        game2 = playTurns(game, 4)
        self.assertEqual(0, game2[NEXTPLAYER])
        self.assertEqual(4, game2[TURNS])
        self.assertEqual([
            (4, 14),
            (6, 9)
        ], game2[PLAYERS])


def part1():
    starts = [2, 7]
    startGame = makeGame(starts)
    endGame = playUntil(
        startGame,
        lambda game: any(player[1] >= 1000 for player in game[0])
    )
    return endGame
print(part1())
