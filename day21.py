import unittest
import itertools
from typing import *
from functools import *
from collections import defaultdict
from pprint import pprint


Dice = Callable[[], int]
MultiDice = List[Tuple[int, int]] # total, qty

Player = Tuple[int, int]  # position, score
PPOS = 0
PSCORE = 1

GameState = Tuple[Tuple[Player, ...], int, int] # players, nextPlayer, turns
PLAYERS = 0
NEXTPLAYER = 1
TURNS = 2

BranchGameState = Tuple[Dict[GameState, int]]

def diceSumChances(sides=3, rolls=3):
    diceRange = list(range(1, sides+1))
    rollSets = set(itertools.combinations(diceRange*rolls, rolls))
    totals = [sum(l) for l in rollSets]
    return {
        n: totals.count(n)
        for n in set(totals)
    }

def makeMultiDice(sides=3, rolls=3):
    return list(diceSumChances(sides, rolls).items())

def makePlayer(startPos: int) -> Player:
    return (startPos, 0)

def makeGame(positions) -> GameState:
    players = tuple([makePlayer(pos) for pos in positions])
    return (players, 0, 0)

def makeBranchingGame(positions) -> BranchGameState:
    return ({makeGame(positions): 1},)

def makeD100() -> Dice:
    it = itertools.cycle(range(1,100 + 1))
    return lambda: next(it)

def playTurn(game: GameState, dice: Dice) -> GameState:
    (players, nextPlayer, turns) = game
    lPlayers = list(players)
    roll = dice() + dice() + dice()
    player = lPlayers[nextPlayer]
    lPlayers[nextPlayer] = movePlayer(player, roll)
    return (
        tuple(lPlayers),
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

def playBranchTurn(game: BranchGameState, dice: MultiDice) -> BranchGameState:
    newBranches = defaultdict(list)
    for start, startQty in game[0].items():
        for roll, qty in dice:
            dseq = [roll, 0, 0]
            step = playTurn(start, lambda: dseq.pop())
            newBranches[step].append(qty * startQty)
    return (
        {game: sum(qtys)
            for game, qtys in newBranches.items()},
            )

def playBranchesUntil(game: BranchGameState, shouldEnd: Callable[[GameState], bool]):
    dice = makeMultiDice()
    doneGames: Dict[GameState, List[int]] = defaultdict(list)
    while len(game[0]):
        stepGames = playBranchTurn(game, dice)
        continueGames: Dict[GameState, int] = {}
        for branchGame, qty in stepGames[0].items():
            if shouldEnd(branchGame):
                doneGames[branchGame].append(qty)
            else:
                continueGames[branchGame] = qty
        print(f" >>> branches == {len(stepGames[0])}, continue {len(continueGames)}")
        game = (continueGames,)
    winsByPlayer: Dict[int, int] = defaultdict(lambda: 0)
    for game, qtys in doneGames.items():
        wonPlayer = 1 if game[PLAYERS][0][PSCORE] > game[PLAYERS][1][PSCORE] else 0
        winsByPlayer[wonPlayer] += sum(qtys)
    return winsByPlayer.items()

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

    def test_branches(self):
        startGame = makeBranchingGame([4,8])
        winScore = playBranchesUntil(
            startGame,
            lambda game: any(player[1] >= 21 for player in game[0])
        )
        self.assertEqual(444356092776315, max(dict(winScore).values()))

    def test_multi_dice(self):
        self.assertEqual(
            27,
            sum([v for k, v in makeMultiDice(3, 3)])
        )
        self.assertEqual(3, dict(makeMultiDice(3, 3))[4])

starts = [2, 7]
def part1():
    startGame = makeGame(starts)
    endGame = playUntil(
        startGame,
        lambda game: any(player[1] >= 1000 for player in game[0])
    )
    return endGame

def part2():
    print("PART 2")
    startGame = makeBranchingGame(starts)
    endGame = playBranchesUntil(
        startGame,
        lambda game: any(player[1] >= 21 for player in game[0])
    )
    pprint(list(endGame))
    print(endGame)

print(part1())
print(part2())
