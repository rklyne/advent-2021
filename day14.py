from functools import lru_cache
import pprint
import typing
from typing import *
import itertools
from textwrap import dedent
import unittest

def compute(start, changes):
    output = ''
    for i in range(len(start)):
        output += start[i]
        chunk = start[i:i+2]
        if chunk in changes:
            output += changes[chunk]
    return output

def polymerise(start, changes, steps):
    step = start
    for i in range(steps):
        step = compute(step, changes)
    return step

def compute2(start, changes):
    output = {}
    def add(pair, num):
        output.setdefault(pair, 0)
        output[pair] += num
    for k, v in start.items():
        if k in changes:
            newChar = changes[k]
            add(k[0] + newChar, v)
            add(newChar + k[1], v)

    return output

def makePairs(start):
    output = {}
    for i in range(len(start) - 1):
        output.setdefault(start[i:i+2], 0)
        output[start[i:i+2]] += 1
    return output

def polymerise2(start, changes, steps):
    step = makePairs(start)
    for i in range(steps):
        step = compute2(step, changes)
    return step

class Tests(unittest.TestCase):
    def test_pairs(self):
        self.assertEqual({"XX": 2}, makePairs("XXX"))

    def test_step(self):
        result = polymerise(
                "NNCB",
                {
                    "CH": "B",
                    "HH": "N",
                    "CB": "H",
                    "NH": "C",
                    "HB": "C",
                    "HC": "B",
                    "HN": "C",
                    "NN": "C",
                    "BH": "H",
                    "NC": "B",
                    "NB": "B",
                    "BN": "B",
                    "BB": "N",
                    "BC": "B",
                    "CC": "N",
                    "CN": "C",
                    },
                1)
        self.assertEqual("NCNBCHB", result)

    def test_4_step(self):
        result = polymerise(
                "NNCB",
                {
                    "CH": "B",
                    "HH": "N",
                    "CB": "H",
                    "NH": "C",
                    "HB": "C",
                    "HC": "B",
                    "HN": "C",
                    "NN": "C",
                    "BH": "H",
                    "NC": "B",
                    "NB": "B",
                    "BN": "B",
                    "BB": "N",
                    "BC": "B",
                    "CC": "N",
                    "CN": "C",
                    },
                4)
        self.assertEqual("NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB", result)

    def test_step2(self):
        result = polymerise2(
                "NNCB",
                {
                    "CH": "B",
                    "HH": "N",
                    "CB": "H",
                    "NH": "C",
                    "HB": "C",
                    "HC": "B",
                    "HN": "C",
                    "NN": "C",
                    "BH": "H",
                    "NC": "B",
                    "NB": "B",
                    "BN": "B",
                    "BB": "N",
                    "BC": "B",
                    "CC": "N",
                    "CN": "C",
                    },
                1)
        self.assertEqual(makePairs("NCNBCHB"), result)

    def test_2_step2(self):
        result = polymerise2(
                "NNCB",
                {
                    "CH": "B",
                    "HH": "N",
                    "CB": "H",
                    "NH": "C",
                    "HB": "C",
                    "HC": "B",
                    "HN": "C",
                    "NN": "C",
                    "BH": "H",
                    "NC": "B",
                    "NB": "B",
                    "BN": "B",
                    "BB": "N",
                    "BC": "B",
                    "CC": "N",
                    "CN": "C",
                    },
                2)
        self.assertEqual(makePairs("NBCCNBBBCBHCB"), result)

    def test_4_step2(self):
        result = polymerise2(
                "NNCB",
                {
                    "CH": "B",
                    "HH": "N",
                    "CB": "H",
                    "NH": "C",
                    "HB": "C",
                    "HC": "B",
                    "HN": "C",
                    "NN": "C",
                    "BH": "H",
                    "NC": "B",
                    "NB": "B",
                    "BN": "B",
                    "BB": "N",
                    "BC": "B",
                    "CC": "N",
                    "CN": "C",
                    },
                4)
        self.assertEqual(makePairs("NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"), result)

myStart = "CVKKFSSNNHNPSPPKBHPB"

myChanges = {
    "OF": "S",
    "VO": "F",
    "BP": "S",
    "FC": "S",
    "PN": "K",
    "HC": "P",
    "PP": "N",
    "FK": "V",
    "KN": "C",
    "BO": "O",
    "KS": "B",
    "FF": "S",
    "KC": "B",
    "FV": "C",
    "VF": "N",
    "HS": "H",
    "OS": "F",
    "VC": "S",
    "VP": "P",
    "BC": "O",
    "HF": "F",
    "HO": "F",
    "PC": "B",
    "CC": "K",
    "NB": "N",
    "KK": "N",
    "KP": "V",
    "BH": "H",
    "BF": "O",
    "OB": "F",
    "VK": "P",
    "FB": "O",
    "NP": "B",
    "CB": "C",
    "PS": "S",
    "KO": "V",
    "SP": "C",
    "BK": "O",
    "NN": "O",
    "OC": "F",
    "VB": "B",
    "ON": "K",
    "NK": "B",
    "CK": "H",
    "NH": "N",
    "CV": "C",
    "PF": "P",
    "PV": "V",
    "CP": "N",
    "FP": "N",
    "SB": "B",
    "SN": "N",
    "KF": "F",
    "HP": "S",
    "BN": "V",
    "NF": "B",
    "PO": "O",
    "CH": "O",
    "VV": "S",
    "OV": "V",
    "SF": "P",
    "BV": "S",
    "FH": "V",
    "CN": "H",
    "VH": "V",
    "HB": "B",
    "FN": "P",
    "OH": "S",
    "SK": "H",
    "OP": "H",
    "VN": "V",
    "HN": "P",
    "BS": "S",
    "CF": "B",
    "PB": "H",
    "SS": "K",
    "NV": "P",
    "FS": "N",
    "CS": "O",
    "OK": "B",
    "CO": "O",
    "VS": "F",
    "OO": "B",
    "NO": "H",
    "SO": "F",
    "HH": "K",
    "FO": "H",
    "SH": "O",
    "HV": "B",
    "SV": "N",
    "PH": "F",
    "BB": "P",
    "KV": "B",
    "KB": "H",
    "KH": "N",
    "NC": "P",
    "SC": "S",
    "PK": "B",
    "NS": "V",
    "HK": "B",
}

def part1():
    output = polymerise(myStart, myChanges, 10)
    counts = {
            char: output.count(char)
            for char in set(output)
            }
    return sorted([(v, k) for (k, v) in counts.items()])

def part2a():
    output = polymerise2(myStart, myChanges, 10)
    counts = {}
    counts[myStart[0]] = 1
    counts[myStart[-1]] = 1
    for pair, v in output.items():
        counts.setdefault(pair[0], 0)
        counts.setdefault(pair[1], 0)
        counts[pair[0]] += v
        counts[pair[1]] += v
    return sorted([(v//2, k) for (k, v) in counts.items()])

def part2():
    output = polymerise2(myStart, myChanges, 40)
    counts = {}
    counts[myStart[0]] = 1
    counts[myStart[-1]] = 1
    for pair, v in output.items():
        counts.setdefault(pair[0], 0)
        counts.setdefault(pair[1], 0)
        counts[pair[0]] += v
        counts[pair[1]] += v
    return sorted([(v/2, k) for (k, v) in counts.items()])

pprint.pprint(part1())
pprint.pprint(part2a())
pprint.pprint(part2())

