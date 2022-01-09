from typing import *

import unittest
import attr
import heapq
from functools import lru_cache


Pod = Literal['A', 'B', 'C' , 'D', '-']
A: Pod = 'A'
B: Pod = 'B'
C: Pod = 'C'
D: Pod = 'D'
NOPOD: Pod = '-'

# L2 L1 T1 I1 T2 ... R1 R2
#       A1    B1
#       A2    B2
StoppingCell = Literal[
    'L1', 'L2', 'R1', 'R2',
    'I1', 'I2', 'I3',
    'A1', 'B1', 'C1', 'D1',
    'A2', 'B2', 'C2', 'D2',
]

# Cell = Union[StoppingCell, Literal['T1', 'T2', 'T3', 'T4']]
Cell = str

InitState = List[List[Pod]]

Move = Tuple[Cell, Cell]
Moves = List[Move]

def moveCost(src: Cell, dst: Cell) -> int:
    return len(movePath(src, dst))

def podCost(pod: Pod):
    if pod == NOPOD:
        raise RuntimeError("Cannot cost when no amphipod is present")
    return {
        'A': 1,
        'B': 10,
        'C': 100,
        'D': 1000,
    }[pod]

topRow: List[Cell] = ['L2', 'L1', 'T1', 'I1', 'T2', 'I2', 'T3', 'I3', 'T4', 'R1', 'R2']

def allCells(cols: int) -> List[Cell]:
    return [  # type:ignore
        'L1', 'L2', 'R1', 'R2',
        'I1', 'I2', 'I3',
    ] + [
        f'{c}{n}'
        for c in 'ABCD'
        for n in range(1, cols + 1)
    ]

@lru_cache(1000000)
def movePath(src: Cell, dst: Cell, rec=True) -> List[Cell]:
    columns = ['A', 'B', 'C', 'D']
    if src == dst:
        return []
    if src in topRow and dst in topRow:
        idx1 = topRow.index(src)
        idx2 = topRow.index(dst)
        if idx1 < idx2:
            return topRow[idx1+1:idx2+1]
        else:
            return list(reversed(topRow[idx2:idx1]))
    if src[0] in columns:
        top: Cell = f'T{columns.index(src[0])+1}' # type:ignore
        c = src[0]
        n = int(src[1])
        pathToTop: List[Cell] = [f'{c}{i-1}' for i in range(n, 1, -1)] + [top] # type:ignore
        return pathToTop + movePath(top, dst)

    if rec:
        reverse = movePath(dst, src, False)
        # we exclude the start
        return list(reversed(reverse))[1:] + [dst]
    else:
        raise RuntimeError(src, dst)

StateLocations = Dict[Cell, Pod]
PodLocations = Dict[Pod, List[Cell]]
# State = Tuple[StateLocations, int, PodLocations]

@attr.s(hash=True)
class State(object):
    locations: StateLocations = attr.ib(eq=False)
    hash: int = attr.ib(eq=True)
    podLocations: PodLocations = attr.ib(eq=False)

    def __attrs_post_init__(self):
        podLocations: PodLocations = self.podLocations
        guesses = [moveCost(location, f'{occupant}{idx}') * podCost(occupant)
                for occupant, locations in podLocations.items()
                for idx, location in enumerate([l for l in locations
                    if l[0] != occupant])]
                # raise RuntimeError(podLocations, guesses)
        self.guessCost = sum(guesses)

def stateFromLocations(newState: StateLocations) -> State:
    return State(newState, stateHash(newState), locationsByPod(newState))

def newBlankState(cols: int) -> State:
    return stateFromLocations({
        c: NOPOD for c in allCells(cols)
    })

def makeState(init: InitState) -> State:
    newState: State = newBlankState(len(init[0]))
    locations = newState.locations.copy()
    for col, pods in zip('ABCD', init):
        for i, value in enumerate(pods, 1):
            locations[f'{col}{i}'] = value # type:ignore
    return stateFromLocations(locations)

@lru_cache(10000)
def isEndState(state: State, cols: int):
    for col in 'ABCD':
        for i in range(1, cols+1):
            if state.locations[f'{col}{i}'] != col:
                return False
    return True

@attr.s
class Game(object):
    depth = 2

    state: State = attr.ib()

    def getLegalMoves(self) -> List[Move]:
        return []

    def isDone(self) -> bool:
        return isEndState(self.state)

extraState = [
    [D, D],
    [C, B],
    [B, A],
    [A, C],
]
def extendInput(initState: InitState) -> InitState:
    return [
            [given[0]] + extra + [given[1]]
            for (given, extra) in zip(
                initState,
                extraState
            )
    ]

myInput: InitState= [[D, C], [B, C], [B, D], [A, A]]

myInput2: InitState = extendInput(myInput)

def stateHash(state: StateLocations) -> int:
    return hash(tuple(sorted(state.items())))

def makeMove(state: State, move: Move) -> State:
    newState = state.locations.copy()
    src = move[0]
    dst = move[1]
    newState[src] = NOPOD
    newState[dst] = state.locations[src]
    return stateFromLocations(newState)

@lru_cache()
def allLegalMoves(cols: int) -> Moves:
    moves: Moves = []
    for src in allCells(cols):
        for dst in allCells(cols):
            if dst == src:
                continue
            if src in topRow and dst in topRow:
                # Amphipods will not move from hallway to hallway
                continue
            path = movePath(src, dst)
            assert dst in path, (src, dst, path)
            move: Move = (src, dst)
            moves.append(move)
    return moves

@lru_cache(20000)
def legalMoves(state: State, cols: int) -> Moves:
    moves: Moves = []
    for src, dst in allLegalMoves(cols):
        srcPod = state.locations[src]
        if srcPod == NOPOD:
            continue
        if dst[0] in 'ABCD' and dst[0] != srcPod:
            continue
        path = movePath(src, dst)
        if all(('T' in cell or state.locations[cell] == NOPOD) for cell in path):
            moves.append((src, dst))
    return moves

Heap = List[Tuple[int, int, Moves, State]]
def pruneHeap(heap: Heap) -> Heap:
    newHeap: Heap = []
    seenStates = set()
    for item in heap:
        h = item[3].hash
        if h not in seenStates:
            newHeap.append(item)
            seenStates.add(h)
    return newHeap

def locationsByPod(state: StateLocations) -> PodLocations:
    podLocations: PodLocations = {}
    for cell, occupant in state.items():
        if occupant != NOPOD:
            podLocations.setdefault(occupant, []).append(cell)
    return podLocations

def guessStateCost(state: State) -> int:
    return state.guessCost

def findFastestWin(init: InitState, debugStep=10000) -> Tuple[int, Moves]:
    state = makeState(init)
    cols: int = len(init[0])
    visited: Dict[State, int] = {state: 0}
    seqs: Heap = []
    heapq.heappush(seqs, (guessStateCost(state), 0, [], state)) # type: ignore
    print(f"COLS: {cols}")

    steps = 0
    while seqs and not isEndState(seqs[0][3], cols):
        guessCost, cost, moves, state = heapq.heappop(seqs)
        if visited.get(state, 0) < cost:
            continue
        if steps % debugStep == 0:
            print(f" >> {steps} ({len(seqs)}) >> cost {cost}/{guessCost}")
        steps += 1
        for move in legalMoves(state, cols):
            podType = state.locations[move[0]]
            newState: State = makeMove(state, move)
            newMoves = moves + [move]
            newCost = cost + (podCost(podType) * moveCost(*move))
            newGuess = guessStateCost(newState)
            prevCost = visited.get(newState, None)
            if prevCost and prevCost <= newCost:
                continue
            heapq.heappush(seqs, (newCost + newGuess, newCost, newMoves, newState))
            visited[newState] = newCost

    top = seqs[0]
    return (top[1], top[2])

class Tests(unittest.TestCase):
    def test_game_done(self):
        state = makeState([[A,A],[B,B],[C,C],[D,D]])
        self.assertTrue(isEndState(state, 2))

    def test_game_not_done(self):
        state = makeState([[A,B],[A,B],[C,C],[D,D]])
        self.assertFalse(isEndState(state, 2))

    def test_legal_moves(self):
        game = Game(makeState([[A,B],[A,B],[C,C],[D,D]]))
        self.assertEqual([], game.getLegalMoves())

class TestMoveCost(unittest.TestCase):
    def test_fromL1_1(self):
        self.assertEqual(2, moveCost('L1', 'I1'))
    def test_fromL1_2(self):
        self.assertEqual(4, moveCost('L1', 'I2'))
    def test_fromL1_3(self):
        self.assertEqual(4, moveCost('L1', 'B1'))
    def test_fromL1_4(self):
        self.assertEqual(5, moveCost('L1', 'B2'))
    def test_fromL1_5(self):
        self.assertEqual(8, moveCost('L1', 'R1'))

    def test_fromL2_1(self):
        self.assertEqual(3, moveCost('L2', 'I1'))
    def test_fromL2_2(self):
        self.assertEqual(5, moveCost('L2', 'I2'))
    def test_fromL2_3(self):
        self.assertEqual(5, moveCost('L2', 'B1'))
    def test_fromL2_4(self):
        self.assertEqual(6, moveCost('L2', 'B2'))
    def test_fromL2_5(self):
        self.assertEqual(9, moveCost('L2', 'R1'))

    def test_path_A2_I1(self):
        self.assertEqual(['A1', 'T1', 'I1'], movePath('A2', 'I1'))
    def test_path_A2_B1(self):
        self.assertEqual(['A1', 'T1', 'I1', 'T2', 'B1'], movePath('A2', 'B1'))
    def test_path_A2_B2(self):
        self.assertEqual(['A1', 'T1', 'I1', 'T2', 'B1', 'B2'], movePath('A2', 'B2'))
    def test_path_A4_B4(self):
        self.assertEqual(['A3', 'A2', 'A1', 'T1', 'I1', 'T2', 'B1', 'B2', 'B3', 'B4'], movePath('A4', 'B4'))
    def test_path_A1_L1(self):
        self.assertEqual(['T1', 'L1'], movePath('A1', 'L1'))
    def test_path_A2_L1(self):
        self.assertEqual(['A1', 'T1', 'L1'], movePath('A2', 'L1'))
    def test_path_L1_A1(self):
        self.assertEqual(['T1', 'A1'], movePath('L1', 'A1'))
    def test_path_T1_L1(self):
        self.assertEqual(['L1'], movePath('T1', 'L1'))

if __name__ == '__main__':
    print(findFastestWin(myInput))
    print(myInput2)
    # print(findFastestWin(myInput2))
