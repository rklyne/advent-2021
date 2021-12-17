import math
import unittest
import typing
from typing import *

import operator as op

Coords = Tuple[int, int]
Box = Tuple[Coords, Coords]
Vector = Tuple[int, int]
Path = List[Coords]

def computeStep(start: Coords, speed: Vector) -> Tuple[Coords, Vector]:
    if speed[0] < 0:
        newX = min(0, speed[0]+1)
    else:
        newX = max(0, speed[0]-1)
    newPos: Coords = (start[0] + speed[0], start[1] + speed[1])
    newVector: Vector = (newX, speed[1] - 1)
    return (newPos, newVector)

def computePathWhile(start: Coords, speed0: Vector, cond: Callable[[Path], bool]) -> Path:
    pos, speed = start, speed0
    path: Path = []
    while cond(path + [pos]):
        path.append(pos)
        pos, speed = computeStep(pos, speed)
    return path

def computePath(start: Coords, speed0: Vector, steps: int) -> Path:
    return computePathWhile(start, speed0, lambda path: len(path) <= steps)


class Tests(unittest.TestCase):
    def test_step(self):
        newPos, newSpeed = computeStep((5,5), (4,4))
        self.assertEqual((9,9), newPos)
        self.assertEqual((3,3), newSpeed)

    def test_path(self):
        path = list(computePath((0,0), (7, 2), 8))
        self.assertEqual(8, len(path))
        self.assertEqual((28, -7), path[-1])

    def test_path_2(self):
        path = list(computePath((0,0), (6, 3), 10))
        self.assertEqual((21, -9), path[-1])

    def test_find_trajectory(self):
        paths = list(findTrajectory([[20, -5], [30, -10]]))
        expectedPaths = set([
(23,-10),  (25,-9),   (27,-5),   (29,-6),   (22,-6),   (21,-7),   (9,0),     (27,-7),   (24,-5),
(25,-7),   (26,-6),   (25,-5),   (6,8),     (11,-2),   (20,-5),   (29,-10),  (6,3),     (28,-7),
(8,0),     (30,-6),   (29,-8),   (20,-10),  (6,7),     (6,4),     (6,1),     (14,-4),   (21,-6),
(26,-10),  (7,-1),    (7,7),     (8,-1),    (21,-9),   (6,2),     (20,-7),   (30,-10),  (14,-3),
(20,-8),   (13,-2),   (7,3),     (28,-8),   (29,-9),   (15,-3),   (22,-5),   (26,-8),   (25,-8),
(25,-6),   (15,-4),   (9,-2),    (15,-2),   (12,-2),   (28,-9),   (12,-3),   (24,-6),   (23,-7),
(25,-10),  (7,8),     (11,-3),   (26,-7),   (7,1),     (23,-9),   (6,0),     (22,-10),  (27,-6),
(8,1),     (22,-8),   (13,-4),   (7,6),     (28,-6),   (11,-4),   (12,-4),   (26,-9),   (7,4),
(24,-10),  (23,-8),   (30,-8),   (7,0),     (9,-1),    (10,-1),   (26,-5),   (22,-9),   (6,5),
(7,5),     (23,-6),   (28,-10),  (10,-2),   (11,-1),   (20,-9),   (14,-2),   (29,-7),   (13,-3),
(23,-5),   (24,-8),   (27,-9),   (30,-7),   (28,-5),   (21,-10),  (7,9),     (6,6),     (21,-5),
(27,-10),  (7,2),     (30,-9),   (21,-8),   (22,-7),   (24,-9),   (20,-6),   (6,9),     (29,-5),
(8,-2),    (27,-8),   (30,-5),   (24,-7),
            ])
        self.assertEqual(len(expectedPaths), len(paths), paths)
        self.assertEqual(expectedPaths, set([speed for (speed, _, last) in paths]))

    def test_inBox(self):
        self.assertTrue(inBox([[20, -5], [30, -10]], [21, -9]))

def inBox(target: Box, spot: Coords) -> bool:
    assert (target[1][0] >= target[0][0])
    assert (target[1][1] <= target[0][1])

    return (
            (spot[0] <= target[1][0] and spot[0] >= target[0][0])
            and
            (spot[1] >= target[1][1] and spot[1] <= target[0][1])
            )

def qf(c):
    # (vx**2 + vx) / 2 = c
    # quadratic formula
    return (-1 + math.sqrt(1 + (8*c))) / 2

def findTrajectory(target: Box, debug=lambda msg: None):
    good = []
    xSpeedMin = min(qf(target[0][0]), target[0][0])
    xSpeedMax = max(qf(target[1][0]), target[1][0] + 1)
    yMin = (target[1][1] - 1)
    yMax = 180
    print(f" ** range X = ({xSpeedMin} ... {xSpeedMax})")
    print(f" ** range Y = ({yMin} ... {yMax})")
    for xSpeed in range(math.floor(xSpeedMin) - 1, math.floor(xSpeedMax) + 2):
        debug(f"found X = {xSpeed} ({xSpeedMin}, {xSpeedMax})")
        for ySpeed in range(yMin, yMax):
            path = computePathWhile((0, 0), (xSpeed, ySpeed), lambda path: path == [] or (path[-1][0] <= target[1][0] and path[-1][1] >= target[1][1]))
            if any(inBox(target, step) for step in path):
                good.append([(xSpeed, ySpeed), max(y for (x, y) in path), path[-1]])
                debug(f">>>> GOOD ({xSpeed}, {ySpeed}) {path}")
                continue
    return good


# target area x=70..96, y=-179..-124
targetTL: Coords = (70, -124)
targetBR: Coords = (96, -179)
target: Box = (targetTL, targetBR)

def part1():
    results = findTrajectory(target)
    return max([y for (speed, y, last) in results]), len(results)

print(f" >>> part 1 + 2 => {part1()}")

