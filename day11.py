import itertools
from textwrap import dedent
import unittest

def init_state(text):
    return [[[int(char) for char in row] for row in text.split("\n")], 0]

def print_state(state):
    grid, flashes = state
    return "\n".join(map(lambda row: ''.join([str(n) for n in row]), grid))

def gridMap(f, grid):
    return list(map(lambda row: list(map(f, row)), grid))

def findCells(f, grid):
    return [
            (x,y)
            for y in range(len(grid))
            for x in range(len(grid[0]))
            if f(grid[y][x])
            ]

def applyFlash(grid, cell):
    cellX, cellY = cell
    newGrid = gridMap(lambda x: x, grid)
    for offsetX in [-1, 0, 1]:
        for offsetY in [-1, 0, 1]:
            y = cellY+offsetY
            x = cellX+offsetX
            if y < 0 or y >= len(grid):
                continue
            if x < 0 or x >= len(grid[0]):
                continue
            newGrid[y][x] += 1
    return newGrid

def process_step(state):
    grid, flashes = state
    # first add 1 to all
    grid = gridMap(lambda x: x + 1, grid)
    # then compute flashes, trigger more flashes
    computedFlashes = set()
    allFlashes = set(findCells(lambda x: x>=10, grid))
    while allFlashes != computedFlashes:
        for flashCell in allFlashes - computedFlashes:
            grid = applyFlash(grid, flashCell)
        computedFlashes = allFlashes
        allFlashes = set(findCells(lambda x: x>=10, grid))
    flashes += len(allFlashes)
    grid = gridMap(lambda x: 0 if x >= 10 else x, grid)
    return [grid, flashes]

def play(input, steps=1):
    state = init_state(input)
    for i in range(steps):
        state = process_step(state)
    return print_state(state), state[1]

def play2(input, steps=1000):
    state = init_state(input)
    for i in range(steps):
        state = process_step(state)
        if sum([n for row in state[0] for n in row]) == 0:
            return i + 1


class Tests(unittest.TestCase):
    input = dedent("""\
    5483143223
    2745854711
    5264556173
    6141336146
    6357385478
    4167524645
    2176841721
    6882881134
    4846848554
    5283751526""").strip()

    def test_one_step(self):
        after_one_step = dedent("""\
        6594254334
        3856965822
        6375667284
        7252447257
        7468496589
        5278635756
        3287952832
        7993992245
        5957959665
        6394862637
        """).strip()
        self.assertEqual(after_one_step, play(self.input, 1)[0])

    def test_two_steps(self):
        after_two_steps = dedent("""\
        8807476555
        5089087054
        8597889608
        8485769600
        8700908800
        6600088989
        6800005943
        0000007456
        9000000876
        8700006848""").strip()
        self.assertEqual(after_two_steps, play(self.input, 2)[0])

    def test_ten_steps(self):
        after_ten_steps = dedent("""\
        0481112976
        0031112009
        0041112504
        0081111406
        0099111306
        0093511233
        0442361130
        5532252350
        0532250600
        0032240000""").strip()
        self.assertEqual(after_ten_steps, play(self.input, 10)[0])


myInput = """
7612648217
7617237672
2853871836
7214367135
1533365614
6258172862
5377675583
5613268278
8381134465
3445428733
""".strip()

print(play(myInput, 100)[1])
print(play2(myInput, 1000))

