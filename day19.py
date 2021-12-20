import unittest

import attr
import itertools
from collections import *
from typing import *
import math
from pprint import pprint

from data19 import data as myInput

def mean(ns):
    # iterator safe
    total = 0
    count = 0
    for n in ns:
        count += 1
        total += n
    return total / count

def rms(coords: List[int]) -> float:
    return math.sqrt(mean([n**2 for n in coords]))

Coord = Tuple[int, int, int]

def coordMinus(l: Coord, r: Coord) -> Coord:
    return (
        l[0] - r[0],
        l[1] - r[1],
        l[2] - r[2],
    )

def coordPlus(l: Coord, r: Coord) -> Coord:
    return (
        l[0] + r[0],
        l[1] + r[1],
        l[2] + r[2],
    )

def toCoordList(x: Any) -> List[Coord]:
    return list(map(tuple, x))  # type: ignore

@attr.s
class Rotation(object):
    transform: Coord = attr.ib()
    shuffle: Coord = attr.ib()

    def mapPoint(self, point: Coord) -> Coord:
        return (
            point[self.shuffle[0]] * self.transform[0],
            point[self.shuffle[1]] * self.transform[1],
            point[self.shuffle[2]] * self.transform[2],
        )

    def map(self, points: List[Coord]) -> List[Coord]:
        return [self.mapPoint(point) for point in points]

"""
[x,y,z]
[1,1,1]
rot z
[1,-1,1]
[-1,-1,1]
[-1,1,1]
[1,1,1]
rot y

"""

long_rotations = list([
    Rotation(rotate, shuffle)
    for rotate in toCoordList(set(itertools.permutations([-1, 1]*3, 3)))

    for shuffle in toCoordList(itertools.permutations([0,1,2]))
])
_ones = [1, -1]
rotations = list([
    Rotation(rotate, shuffle)
    # third param is covered by the combination with shuffles below
    for rotate in toCoordList([(a, b, c) for a in _ones for b in _ones for c in _ones])

    for shuffle in toCoordList(itertools.permutations([0,1,2]))
])
print(f" >>> Rotations: {len(rotations)}")
rotation0 = Rotation((1, 1, 1), (0, 1, 2))

PointMap = Dict[int, int]

@attr.s
class Scanner(object):
    points: List[Coord] = attr.ib(converter=toCoordList)
    rms_pairs: Dict[float, Set[Tuple[int, int]]] = attr.ib(
        default=attr.Factory(lambda: defaultdict(set))
    )

    def __attrs_post_init__(self):
        self._calculate()

    def _calculate(self):
        for (lIdx, l), (rIdx, r) in itertools.combinations(list(enumerate(self.points)), 2):
            rmsd = rms([x-y for x, y in zip(l, r)])
            self.rms_pairs[rmsd].add((lIdx, rIdx))

    def translate(self, t: Coord) -> List[Coord]:
        return [
            coordPlus(p, t)
            for p in self.points
        ]

    def add(self, other: 'Scanner') -> Tuple[Optional['Scanner'], Optional[Coord]]:
        overlap, translation, rotation = self.overlapping_points(other)
        if len(overlap) > 10:
            newPoints = [
                coordPlus(translation, c)
                for idx, c in enumerate(rotation.map(other.points))
                if idx not in overlap
            ]
            return Scanner(self.points + newPoints), translation
            # raise RuntimeError(overlap, newPoints)
        return None, None

    def overlapping_points(self, other: 'Scanner') -> Tuple[PointMap, Coord, Rotation]:
        # find mapping set
        lDistances = set(self.rms_pairs.keys())
        rDistances = set(other.rms_pairs.keys())
        matching_distances = set(lDistances).intersection(rDistances)
        # find mapping
        mappedPoints: PointMap = {}
        mappedTranslation = (0, 0, 0)
        mappedRotation = rotation0
        for rotation in rotations:
            rPoints = rotation.map(other.points)
            for lIdx, lDist in set([(idx, dist) for dist in matching_distances for idxPair in self.rms_pairs[dist] for idx in idxPair]):
                lPoint: Coord = self.points[lIdx]
                for rIdxs in other.rms_pairs[lDist]:
                    for rIdx in rIdxs:
                        rPoint: Coord = rPoints[rIdx]
                        translation: Coord = coordMinus(lPoint, rPoint)

                        mapping: PointMap = {
                            rI: lI
                            for lI, l in enumerate(self.points)
                            for rI, r in enumerate(rPoints)
                            if l == coordPlus(r, translation)
                        }
                        if len(mapping) > len(mappedPoints):
                            print(f"new map {len(mapping)}")
                            mappedPoints = mapping
                            mappedTranslation = translation
                            mappedRotation = rotation
                            if len(mapping) >= 12:
                                return (mappedPoints, mappedTranslation, mappedRotation)
        return (mappedPoints, mappedTranslation, mappedRotation)

class Tests(unittest.TestCase):
    def test_rms(self):
        self.assertEqual(1, rms([1, 1]))

    def test_scanner_rms(self):
        scanner = Scanner([[1,1,1], [2,2,2]])
        self.assertSetEqual(
            set([1.0]),
            set(scanner.rms_pairs.keys()),
            scanner.rms_pairs
        )
        self.assertSetEqual({(0, 1)}, scanner.rms_pairs[1.0])

    def test_scanner_overlap(self):
        scanner1 = Scanner([(1,1,1), (2,2,2), (3,3,3), (6,1,1)])
        scanner2 = Scanner([(1,1,1), (0,0,0), (5,0,0)])
        overlaps, translation, rotation = scanner1.overlapping_points(scanner2)
        self.assertEqual(
            3,
            len(overlaps),
            overlaps)

    def test_scanner_overlap_2(self):
        scanner1 = Scanner([(-1,-1,-1), (-2,-2,-2), (-3,-3,-3), (-6,-1,-1)])
        scanner2 = Scanner([(1,1,1), (0,0,0), (5,0,0)])
        overlaps, translation, rotation = scanner1.overlapping_points(scanner2)
        self.assertEqual(
            3,
            len(overlaps),
            overlaps)

    def test_rotation_1(self):
        rot = Rotation((-1, -1, 1), (2, 1, 0))
        self.assertEqual((-4, -3, 2), rot.mapPoint((2, 3, 4)))
        self.assertEqual(
                [
                    (-4, -3, 2),
                    (-5, -4, 3),
                ],
                rot.map([
                    (2, 3, 4),
                    (3, 4, 5),
                ]))


def manhattanDistance(a, b):
    return sum(map(abs, coordMinus(b, a)))

def part1():
    scanners = [Scanner(set(points)) for points in myInput]
    main = scanners.pop()
    start = len(scanners)
    last = 0
    translations = []
    distances = [(0, 0, 0)]
    while scanners and len(scanners) != last:
        last = len(scanners)
        for n in iter(scanners):
            added, newDistance = main.add(n)
            if added:
                print(f"woo {len(main.points)}")
                main = added
                distances.append(newDistance)
                scanners.remove(n)
                maxDistance = max([manhattanDistance(p1, p2) for (p1, p2) in itertools.combinations(distances, 2)])
                print(f"distance {maxDistance}")

    if scanners:
        print(f"fail {start} -> {len(scanners)}")
    else:
        print(len(main.points))
        maxDistance = max(manhattanDistance(p1, p2) for (p1, p2) in itertools.combinations(distances))
        print(f"distance {maxDistance}")

if __name__ == '__main__':
    part1()
    print(sum(map(len, myInput)))
