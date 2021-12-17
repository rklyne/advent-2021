import functools
import itertools
import attr
import math
import unittest
import typing
from typing import *

import operator as op

SnailPair = Tuple['Snail', 'Snail']  # type: ignore
Snail = Union[int, SnailPair]  # type: ignore

def split(n: int) -> Snail:
    return (n//2, (n - n//2))

def iterTuples(snail: Snail):
    if isinstance(snail, tuple):
        yield snail[0], 0
        yield snail[1], 1

In = Literal["in"]
IN: In = "in"
Out = Literal["out"]
OUT: Out = "out"

SnailSteps = Union[In, Out, int]

def walk(snail: Snail) -> Iterator[SnailSteps]:
    if isinstance(snail, tuple):
        yield IN
        yield from walk(snail[0])
        yield from walk(snail[1])
        yield OUT
    else:
        yield snail

def buildSnail(steps) -> Snail:
    mySnail: List[Snail] = []
    it = iter(steps)
    for step in it:
        if isinstance(step, int):
            mySnail.append(step)
        elif step == IN:
            mySnail.append(buildSnail(it))
        elif step == OUT:
            break
    if len(mySnail) == 1:
        return mySnail[0]
    return mySnail[0], mySnail[1]

def levelCheck(steps):
    level = 0
    maxLevel = 0
    for idx, step in enumerate(steps):
        if step == IN:
            level += 1
        if step == OUT:
            level -= 1
        maxLevel = max(maxLevel, level)
    if maxLevel > 5:
        raise RuntimeError(steps)


def explode(snail: Snail, debug = lambda msg: None) -> Snail:
    # If any pair is nested inside four pairs, the leftmost such pair explodes
    level = 0
    foundPlace = False
    lastNumIdx = None
    increment2 = None
    steps = list(walk(snail))
    # levelCheck(steps)
    debug("BEGIN")
    debug(steps)
    for idx, step in enumerate(steps):
        debug(f" >>> lvl={level} last={lastNumIdx} *{foundPlace}: {increment2}*  >>> {step}")
        if step == IN:
            level += 1
        if step == OUT:
            level -= 1
        if isinstance(step, int):
            if foundPlace:
                debug(f" !! second increment {step} {steps[idx-2:idx+2]}")
                steps[idx] += increment2
                break
            lastNumIdx = idx
        elif not foundPlace:
            hasNumbers = idx + 2 < len(steps) and isinstance(steps[idx+1], int) and isinstance(steps[idx+2], int)
            if level > 4 and hasNumbers:
                if foundPlace:
                    raise RuntimeError(increment2)
                # do the exploding
                assert steps[idx] == IN, step
                foundPlace = True
                debug(f"from here {steps[idx: idx+5]}")
                increment1 = steps[idx+1]
                increment2 = steps[idx+2]
                debug(f" >> increments {increment1}, {increment2}")
                steps[idx:idx+4] = [0]
                if lastNumIdx:
                    debug(f" >> lastNum {increment1}, {steps[lastNumIdx]}")
                    # You won't believe this line! Type systems hate him!
                    steps[lastNumIdx] += increment1  # type: ignore
    debug(steps)
    return buildSnail(steps)

@attr.s
class SnailFish(object):
    snail: Snail = attr.ib()

    def add(self, other: 'SnailFish', debug = lambda msg: None) -> 'SnailFish':
        return SnailFish((self.snail, other.snail)).reduce(debug)

    def magnitude(self):
        def mag(snail):
            if isinstance(snail, int):
                return snail
            return 3*mag(snail[0]) + 2*mag(snail[1])
        return mag(self.snail)

    def mapValues(self, f: Callable[[int], Snail]):
        changes = []
        def mapSnail(s: Snail):
            if changes:
                return s
            elif isinstance(s, int):
                n = f(s)
                if n != s:
                    changes.append(n)
                return n
            else:
                return (mapSnail(s[0]), mapSnail(s[1]))
        return SnailFish(mapSnail(self.snail))


    def reduce(self, debug = lambda msg: None) -> 'SnailFish':
        nextSnail = self.snail
        n = 0
        while True:
            n += 1
            debug(f"reduce step >>>> {nextSnail}")
            step1 = explode(nextSnail, debug=debug)
            if step1 != nextSnail:
                debug(" !!!!!!! keeping exploded ")
                nextSnail = step1
                continue

            # If any regular number is 10 or greater, the leftmost such regular number splits
            step2 = SnailFish(nextSnail).mapValues(
                    lambda snail: split(snail) if snail >= 10 else snail
                    ).snail
            if step2 != nextSnail:
                debug(" !!!!!!! keeping split ")
                nextSnail = step2
                continue
            break
        return SnailFish(nextSnail)

SF = SnailFish

class Tests(unittest.TestCase):
    def test_add_1(self):
        self.assertEqual(SF((1, 2)).add(SF(((3, 4), 5))), SF(((1, 2), ((3, 4), 5))))

    def test_add_2(self):
        l = ((((7,7),(7,7)),((8,7),(8,7))),(((7,0),(7,7)),9))
        r = ((((4,2),2),6),(8,7))
        a = ((((8,7),(7,7)),((8,6),(7,7))),(((0,7),(6,6)),(8,7)))
        self.assertEqual(a, SnailFish(l).add(SnailFish(r)).snail)

    def test_add_3(self):
        l = ((((1,1),(2,2)),(3,3)),(4,4))
        r = (5, 5)
        a = ((((3,0),(5,3)),(4,4)),(5,5))
        self.assertEqual(a, SnailFish(l).add(SnailFish(r)).snail)

    def test_add_4(self):
        l = ((((3,0),(5,3)),(4,4)),(5,5))
        r = (6, 6)
        a = ((((5,0),(7,4)),(5,5)),(6,6))
        self.assertEqual(a, SnailFish(l).add(SnailFish(r)).snail)

    def test_explode_0(self):
        l = (1, 2)
        self.assertEqual(explode(l), l)

    def test_explode_1(self):
        l = (((((9,8),1),2),3),4)
        r = ((((0,9),2),3),4)
        self.assertEqual(explode(l), r)

    def test_explode_2(self):
        l = ((((0,7),4),(7,((8,4),9))),(1,1))
        r = ((((0,7),4),(15,(0,13))),(1,1))
        self.assertEqual(explode(l), r)

    def test_split(self):
        self.assertEqual((5,6), split(11))
        self.assertEqual((6,6), split(12))
        self.assertEqual((5,5), split(10))
        self.assertEqual((0,0), split(0))

    def test_explode_5(self):
        r = (((((0, 7), ((7, 7), 0)), ((7, 7), (7, 7))), (((36, 0), 15), (6, (7, 0)))), ((8, (2, 2)), (5, (9, (4, 9)))))
        expected = ((((0, ((14, 7), 0)), ((7, 7), (7, 7))), (((36, 0), 15), (6, (7, 0)))), ((8, (2, 2)), (5, (9, (4, 9)))))
        actual = explode(r)
        self.assertEqual(expected, actual)

    def test_magnitude(self):
        l = ((((6,6),(7,6)),((7,7),(7,0))),(((7,7),(7,7)),((7,8),(9,9))))
        self.assertEqual(4140, SnailFish(l).magnitude())

    def test_add_all(self):
        data = [
                ((0,(5,8)),((1,7),(9,6)),((4,(1,2)),((1,4),2))),
        (((5,(2,8)),4),(5,((9,9),0))),
        (6,(((6,2),(5,6)),((7,6),(4,7)))),
        (((6,(0,7)),(0,9)),(4,(9,(9,0)))),
        (((7,(6,4)),(3,(1,3))),(((5,5),1),9)),
        ((6,((7,3),(3,2))),(((3,8),(5,7)),4)),
        ((((5,4),(7,7)),8),((8,3),8)),
        ((9,3),((9,9),(6,(4,9)))),
        ((2,((7,7),7)),((5,8),((9,3),(0,2)))),
        ((((5,2),5),(8,(3,7))),((5,(7,5)),(4,4))),
                ]
        self.assertEqual((
            (((6,6),(7,6)),((7,7),(7,0))),(((7,7),(7,7)),((7,8),(9,9)))
            ), addAll(data).snail)


    def test_walk_build(self):
        sf = (((((9,8),1),2),3),4)
        self.assertEqual(sf, buildSnail(walk(sf)))

myInput = [        (2,(0,(9,(5,9)))),
        ((2,(1,8)),3),
        ((((7,2),6),((7,8),3)),(9,((6,9),2))),
        ((((7,2),(9,8)),7),(4,((2,2),(5,0)))),
        ((8,(2,2)),(5,(9,(4,9)))),
        ((((6,2),(4,8)),5),0),
        ((3,(3,(6,6))),(6,9)),
        (((9,5),((8,2),(4,0))),((5,5),((5,0),(1,9)))),
        ((((7,4),(8,1)),(2,(7,1))),2),
        ((((9,6),3),8),(((9,8),7),(5,(0,8)))),
        (((4,(4,0)),((7,3),3)),(8,(3,(8,2)))),
        ((((8,4),1),6),((1,(8,7)),1)),
        (((8,2),((1,4),3)),((4,5),((9,1),(7,2)))),
        ((((5,0),(8,8)),((4,2),4)),(2,((4,3),(3,7)))),
        (((8,7),(2,1)),(9,3)),
        ((3,(7,4)),(0,3)),
        (4,(((5,0),(5,2)),3)),
        ((((0,1),0),8),(6,3)),
        ((7,((9,8),(2,7))),(((8,8),(9,4)),((0,5),(4,1)))),
        ((((3,7),(5,4)),(8,(1,8))),((1,8),((6,9),9))),
        ((((7,4),(7,7)),7),(1,((8,2),(1,8)))),
        ((((6,2),8),((1,2),3)),(((3,6),(4,9)),((3,1),(9,8)))),
        (((3,(1,1)),((6,5),(2,2))),9),
        ((((9,1),4),1),(((1,3),3),(0,(1,4)))),
        (((5,0),(4,(6,8))),((2,4),((0,3),(2,6)))),
        (9,((9,(1,5)),1)),
        ((1,((6,0),(9,2))),(((4,2),7),((2,9),6))),
        ((((8,2),8),9),(((4,9),(3,8)),2)),
        (((9,1),(6,5)),(((9,5),5),1)),
        ((((1,3),5),2),(1,1)),
        ((((0,0),(8,1)),8),8),
        ((((3,3),5),((9,6),9)),((3,(0,9)),7)),
        (((6,5),1),1),
        (((4,(1,3)),((2,2),2)),((8,0),((8,1),(2,6)))),
        (9,((4,6),2)),
        (((5,(8,8)),((1,8),(4,9))),(9,(3,6))),
        ((((9,3),3),0),8),
        (((5,0),((2,8),(1,1))),(((5,6),9),8)),
        ((((5,0),(5,2)),((7,0),(9,8))),(3,((5,7),(5,9)))),
        ((3,(5,7)),1),
        ((((2,5),(0,7)),9),(((3,2),1),(7,1))),
        (6,(7,(6,0))),
        (((8,5),((1,7),(7,6))),((1,3),(5,(1,9)))),
        ((((9,4),(8,3)),1),((1,6),((2,5),1))),
        ((((6,5),(6,6)),(5,5)),(1,8)),
        ((((7,7),(2,2)),3),(1,((8,6),(5,1)))),
        ((6,(2,4)),((8,8),((3,5),6))),
        ((1,((6,1),(9,3))),((2,0),5)),
        (((5,9),(6,(1,9))),(3,(4,(7,7)))),
        ((((3,6),(8,5)),((9,4),(4,1))),(3,3)),
        (((3,9),(1,6)),2),
((((0,9),7),6),(7,(9,(9,9)))),
(((5,(6,0)),(8,(7,5))),(((8,8),0),(8,1))),
((((6,9),(9,0)),2),(((0,3),(1,6)),(2,4))),
((((8,2),(3,0)),((3,8),8)),(6,((9,3),4))),
(((6,6),2),(5,(1,4))),
((1,(1,4)),(((4,3),0),1)),
((((9,9),3),0),(((3,3),(2,8)),(1,0))),
((((1,1),(3,5)),(9,7)),4),
(((9,(3,6)),5),((4,9),(9,3))),
((8,7),(5,(7,(7,7)))),
((((0,5),(7,3)),((8,6),8)),(((4,4),(5,0)),((2,2),2))),
(((5,0),((1,9),(5,8))),((1,5),((9,3),(0,7)))),
(((1,(1,5)),(8,(2,2))),0),
(((6,(7,8)),((0,2),5)),(3,(5,(8,0)))),
((((1,7),2),3),(((8,7),(7,8)),(7,(5,5)))),
((1,(7,(3,3))),(8,(9,(3,0)))),
((5,6),((5,(2,8)),((5,5),(8,8)))),
((8,((7,7),(4,0))),((5,(0,4)),(6,(6,2)))),
((4,((0,0),(0,1))),((3,1),((6,7),4))),
((((3,2),(4,2)),((4,4),(6,3))),(9,(0,(1,9)))),
((((4,6),2),((9,6),4)),((9,(9,1)),(0,(1,8)))),
(((5,8),((6,5),(0,4))),((0,(6,3)),(2,0))),
((6,8),((5,5),(5,8))),
(((7,3),(8,(6,7))),(((1,5),2),7)),
((6,(8,(8,9))),(((1,1),(3,0)),((7,2),(3,7)))),
((((8,1),6),(9,(5,1))),(((5,9),(1,9)),5)),
((((3,6),(5,7)),((0,3),8)),(3,((2,1),0))),
((7,(5,1)),(((3,6),9),((4,0),6))),
((((3,8),8),0),((1,(1,4)),((4,5),(8,5)))),
(((8,(0,6)),(4,3)),(8,((1,5),8))),
(2,((1,(9,7)),((2,0),6))),
((((7,4),4),((4,9),3)),(((6,5),(0,5)),((9,8),(2,6)))),
(((3,(7,2)),((7,7),4)),(((3,4),(6,0)),(6,3))),
(((1,9),((9,8),9)),5),
(((4,2),2),(((4,4),7),5)),
(((9,1),(2,(1,5))),((4,3),(4,(9,5)))),
(2,(((8,4),1),((2,4),2))),
(((0,6),5),(1,((2,0),6))),
((((2,4),(1,7)),(1,0)),(9,5)),
((7,(3,(2,0))),((7,8),8)),
((9,(1,0)),((0,4),((0,1),0))),
(0,9),
((((2,9),(2,4)),((5,6),8)),((5,(1,4)),(3,(0,6)))),
((5,((5,8),0)),(((0,6),(4,5)),((8,9),(8,3)))),
((((5,2),(7,7)),(0,(4,1))),((8,7),((5,3),7))),
(((5,3),5),(0,0)),
(3,5),
((2,6),5),
((5,((6,0),3)),((3,(8,7)),(2,0))),
]


def addAll(snails: List[Snail]):
    total = SnailFish(snails[0])
    for snail in snails[1:]:
        total = total.add(SnailFish(snail))
    return total

def largestMag(snails: List[Snail]):
    largest = 0
    sfs = list(map(SnailFish, snails))
    for snail1 in sfs:
        for snail2 in sfs:
            if snail1 == snail2:
                continue
            mag = snail1.add(snail2).magnitude()
            largest = max(largest, mag)
    return largest

def part1():
    return addAll(myInput).magnitude()
def part2():
    return largestMag(myInput)

print(part1())
print(part2())
