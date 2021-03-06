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
Path = List[Cell]
Moves = List[Move]

def moveCost(src: Cell, dst: Cell) -> int:
    return len(movePath(src, dst))

POD_COSTS: Dict[Pod, int] = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}

topRow: List[Cell] = ['L2', 'L1', 'T1', 'I1', 'T2', 'I2', 'T3', 'I3', 'T4', 'R1', 'R2']
topRowSet = set(topRow)

@lru_cache
def allCells(pods: int) -> List[Cell]:
    return [  # type:ignore
        'L1', 'L2', 'R1', 'R2',
        'I1', 'I2', 'I3',
    ] + [
        f'{c}{n}'
        for c in 'ABCD'
        for n in range(1, pods + 1)
    ]

@lru_cache(1000000)
def movePath(src: Cell, dst: Cell, rec=True) -> Path:
    columns = ['A', 'B', 'C', 'D']
    if src == dst:
        return []
    if src in topRowSet and dst in topRowSet:
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

@lru_cache(1000000)
def computeOccupantGuess(occupant, locations):
    outOfPlace = [l for l in locations
            if l[0] != occupant]
    return sum([moveCost(location, f'{occupant}{idx}') * POD_COSTS[occupant]

        for idx, location in enumerate(outOfPlace)])

def computeGuess(podLocations: PodLocations) -> int:
    return sum([computeOccupantGuess(occupant, tuple(locations))
        for occupant, locations in podLocations.items()
    ])

@attr.s(hash=True)
class State1(object):
    locations: StateLocations = attr.ib(eq=False)
    hash: int = attr.ib(eq=True, default=None)
    podLocations: PodLocations = attr.ib(eq=False, default=None)

    def __attrs_post_init__(self):
        # self._store = [self.locations.get(cell, NOPOD) for cell in allCells(self.pods)]
        self._computePodLocations()
        self._computeHash()
        self._computeGuessCost()

    def _computeHash(self):
        self.hash = hash(tuple(sorted(self.locations.items())))

    def _computePodLocations(self):
        self.podLocations = locationsByPod(self.locations)

    def _computeGuessCost(self):
        self.guessCost = computeGuess(self.podLocations)

    def move(self, move: Move):
        newLocations = self.locations.copy()
        src = move[0]
        dst = move[1]
        del newLocations[src]
        newLocations[dst] = self.locations[src]
        return State1(newLocations)

    def getPodAt(self, cell: Cell):
        return self.locations[cell]

    @classmethod
    def fromLocations(cls, init: InitState):
        newState = newBlankState(len(init[0]))
        locations = newState.locations.copy()
        for col, pods in zip('ABCD', init):
            for i, value in enumerate(pods, 1):
                locations[f'{col}{i}'] = value # type:ignore
        return cls(locations)

    def isEndState(self, pods: int):
        for col in 'ABCD':
            for i in range(1, pods+1):
                if self.locations.get(f'{col}{i}', NOPOD) != col:
                    return False
        return True

    def legalMoves(self, pods: int):
        moves: Moves = []
        for (src, dst), path in allLegalMoves(pods):
            srcPod = self.locations.get(src, NOPOD)
            if srcPod == NOPOD:
                continue
            if dst[0] in 'ABCD' and dst[0] != srcPod:
                continue
            if all((self.locations.get(cell, NOPOD) == NOPOD) for cell in path):
                moves.append((src, dst))
        return moves

@lru_cache(100)
def endStateStore(pods: int):
    return tuple([cell[0] if cell[0] in 'ABCD' else NOPOD for cell in allCells(pods)])

@lru_cache(200000)
def forbiddenSet(pods, store):
    return {k for (k, v) in zip(allCells(pods), store) if v != NOPOD}

@lru_cache(1000000)
def locationMap(pods: int, store):
    return {k: v for (k, v) in zip(allCells(pods), store)}

@attr.s(hash=True)
class State2(object):
    pods: int = attr.ib(eq=True)
    _store = attr.ib(eq=True)
    locations: StateLocations = attr.ib(eq=False, default=None)
    hash: int = attr.ib(eq=True, default=None)

    def __attrs_post_init__(self):
        # self.locations = {k: v for (k, v) in zip(allCells(self.pods), self._store)}

        self._computeHash()
        self.guessCost = State2._computeGuessCost(self.pods, self._store)

    def _computeHash(self):
        self.hash = hash(self._store)

    @staticmethod
    @lru_cache(100000)
    def _computeGuessCost(pods, store):
        podCount = {}
        guess = 0
        for cell, pod in zip(allCells(pods), store):
            if pod == NOPOD:
                continue
            if cell[0] != pod:
                podCount.setdefault(pod, 0)
                podCount[pod] += 1
                guess += POD_COSTS[pod] * moveCost(cell, pod + '1')

        for v in podCount.values():
            # compensate for using '1' above
            guess += ((v-1) * v ) // 2
        return guess

    def move(self, move: Move) -> 'State2':
        newLocations = list(self._store)
        allMoves = allCells(self.pods)
        src = allMoves.index(move[0])
        dst = allMoves.index(move[1])
        newLocations[dst] = self._store[src]
        newLocations[src] = NOPOD
        return State2(self.pods, tuple(newLocations))

    def getPodAt(self, cell: Cell) -> Pod:
        if cell[0] == 'T': return NOPOD
        return self._store[allCells(self.pods).index(cell)]

    @classmethod
    def fromLocations(cls, init: InitState):
        pods = len(init[0])
        locations = {}
        for pod, initPods in zip('ABCD', init):
            for i, value in enumerate(initPods, 1):
                locations[f'{pod}{i}'] = value # type:ignore
        store = tuple(locations.get(cell, NOPOD) for cell in allCells(pods))
        return cls(pods, store)

    def isEndState(self, pods: int):
        return self._store == endStateStore(self.pods)

    def legalMoves(self, pods: int):
        forbidden = forbiddenSet(self.pods, self._store)
        locations = locationMap(self.pods, self._store)
        moves: Moves = []
        for (src, dst), path in allLegalMoves(self.pods):
            srcPod = locations[src]
            if srcPod == NOPOD:
                continue
            if dst[0] != srcPod:
                if src in topRowSet:
                    continue
                if dst[0] in 'ABCD':
                    continue
            if all(cell not in forbidden for cell in path):
                moves.append((src, dst))
        return moves


State = State2

def newBlankState(pods: int) -> State:
    return makeState([[NOPOD]*pods]*4)

def makeState(init: InitState) -> State:
    return State.fromLocations(init)

@lru_cache(10000)
def isEndState(state: State, pods: int):
    return state.isEndState(pods)

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

def makeMove(state: State, move: Move) -> State:
    return state.move(move)

@lru_cache()
def allLegalMoves(pods: int) -> List[Tuple[Move, Path]]:
    moves: Moves = []
    for src in allCells(pods):
        for dst in allCells(pods):
            if dst[0] == src[0]:
                continue
            if src in topRowSet and dst in topRowSet:
                # Amphipods will not move from hallway to hallway
                continue
            path: Path = movePath(src, dst)
            assert dst in path, (src, dst, path)
            move: Move = (src, dst)
            moves.append((move, path))
    print(f"legal moves@{pods} == {len(moves)}")
    return moves

def legalMoves(state: State, pods: int) -> Moves:
    return state.legalMoves(pods)

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
    pods: int = len(init[0])
    visited: Dict[State, int] = {state: 0}
    seqs: Heap = []
    heapq.heappush(seqs, (state.guessCost, 0, [], state)) # type: ignore
    print(f"PODS: {pods}")

    steps = 0
    while seqs and not isEndState(seqs[0][3], pods):
        if steps % 200000 == 0:
            seqs = pruneHeap(seqs)
        guessCost, cost, moves, state = heapq.heappop(seqs)
        if len(moves) == (state.pods * 4 * 2):
            continue
        if visited.get(state, 0) < cost:
            continue
        if steps % debugStep == 0:
            print(f" >> {steps} ({len(seqs)}) >> cost {cost}/{guessCost}")
        steps += 1
        for move in legalMoves(state, pods):
            podType = state.getPodAt(move[0])
            newState: State = makeMove(state, move)
            newMoves = moves + [move]
            newCost = cost + (POD_COSTS[podType] * moveCost(*move))
            newGuess = newState.guessCost
            if newGuess > 47000:
                continue
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
    allLegalMoves(4)
    print(findFastestWin(myInput))
    print(myInput2)
    # print(findFastestWin(myInput2))
