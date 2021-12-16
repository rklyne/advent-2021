import operator as op
from functools import lru_cache, reduce
import pprint
import typing
from typing import *
import itertools
from textwrap import dedent
import collections
import unittest

LITERAL = 4


Instruction = collections.namedtuple('Instruction', ['type', 'version', 'value', 'subPackets'])

class BitStream:
    def __init__(self, hex):
        self.cursor = 0
        # self.allBits = '{0:b}'.format(int(hex, 16))
        self.allBits = ''.join(['{0:b}'.format(int(byte, 16)).rjust(4, '0') for byte in hex])
        self.bits = self.allBits

    def peek(self, n):
        return self.bits[:n]

    def take(self, n):
        self.cursor += n
        result, self.bits = self.bits[:n], self.bits[n:]
        return result

    def endWord(self):
        wordSize = 8
        self.take((wordSize-self.cursor) % wordSize)

    def hasMore(self):
        return self.cursor < len(self.allBits)

    def debug(self):
        print((self.cursor, len(self.allBits), self.hasMore()))

def readPacket(stream, truncate=True, debug=lambda msg: None):
    debug(f"parse start >>> {stream.peek(12)} {stream.peek(32)[12:]}")
    readSubPacket = lambda: readPacket(stream, False, debug=debug)
    try:
        version = int(stream.take(3), 2)
        typeNum = int(stream.take(3), 2)
        if typeNum == 4:
            debug(f"parsing literal {version}")
            # literal
            cont = '1'
            valueBits = ''
            while cont == '1':
                cont = stream.take(1)
                valueBits += stream.take(4)
            value = int(valueBits, 2)
            return Instruction(typeNum, version, value, [])
        else:
            # operator
            debug(f"parsing operator {version} >>> {stream.peek(16)}")
            lengthType = stream.take(1)
            subPackets = []
            if lengthType == '0':
                subLen = int(stream.take(15), 2)
                subPacketStart = stream.cursor
                subPacketEnd = subLen + subPacketStart
                debug(f"sub packets(b) {subPacketStart} {subPacketEnd}")
                while stream.cursor < subPacketEnd:
                    debug(f" *** parsing subpacket >>> {stream.peek(16)}")
                    subPackets.append(readSubPacket())
                # raise RuntimeError(subPackets, subPacketEnd, subPacketStart)
            else:
                subPacketCount = int(stream.take(11), 2)
                debug(f"sub packets(c) {subPacketCount}")
                subPackets = [readSubPacket() for _ in range(subPacketCount) if stream.hasMore()]
                # raise RuntimeError(subPackets, subPacketCount)
            return Instruction(typeNum, version, None, list(filter(bool, subPackets)))
    finally:
        if truncate:
            stream.endWord()

def parseInstructions(hex):
    stream = BitStream(hex)
    instructions = []
    n = 0
    while stream.hasMore():
        n += 1
        print(f"parsing {n}")
        instructions.append(readPacket(stream))
    return list(filter(bool, instructions))

def versionSum(instructions):
    return sum(ins.version + versionSum(ins.subPackets or []) for ins in instructions)

def computePacket(packet: Instruction):
    t = packet.type
    if t == LITERAL:
        return packet.value
    subs = list(map(computePacket, packet.subPackets))
    if t == 0:
        return reduce(op.add, subs)
    if t == 1:
        return reduce(op.mul, subs)
    if t == 2:
        return reduce(min, subs)
    if t == 3:
        return reduce(max, subs)
    if t == 5:
        return 1 if subs[0] > subs[1] else 0
    if t == 6:
        return 1 if subs[0] < subs[1] else 0
    if t == 7:
        return 1 if subs[0] == subs[1] else 0

def compute(instructions):
    return list(map(computePacket, instructions))

class Tests(unittest.TestCase):
    def test_parse_literal(self):
        instr = parseInstructions("D2FE28")[0]
        self.assertEqual(LITERAL, instr.type)
        self.assertEqual(6, instr.version)
        self.assertEqual(2021, instr.value)

    def test_parse_length_type_1(self):
        instr = parseInstructions("38006F45291200")[0]
        self.assertEqual(1, instr.version)
        self.assertEqual(2, len(instr.subPackets))
        self.assertEqual(10, instr.subPackets[0].value)
        self.assertEqual(20, instr.subPackets[1].value)

    def test_parse_length_type_2(self):
        instr = parseInstructions("EE00D40C823060")[0]
        self.assertEqual(7, instr.version)
        self.assertEqual(3, len(instr.subPackets))

    def test_version_sum(self):
        self.assertEqual(16, versionSum(parseInstructions("8A004A801A8002F478")))
    def test_version_sum_2(self):
        self.assertEqual(12, versionSum(parseInstructions("620080001611562C8802118E34")))
    def test_version_sum_3(self):
        self.assertEqual(23, versionSum(parseInstructions("C0015000016115A2E0802F182340")))
    def test_version_sum_4(self):
        self.assertEqual(31, versionSum(parseInstructions("A0016C880162017C3686B18A3D4780")))

data = "2052ED9802D3B9F465E9AE6003E52B8DEE3AF97CA38100957401A88803D05A25C1E00043E1545883B397259385B47E40257CCEDC7401700043E3F42A8AE0008741E8831EC8020099459D40994E996C8F4801CDC3395039CB60E24B583193DD75D299E95ADB3D3004E5FB941A004AE4E69128D240130D80252E6B27991EC8AD90020F22DF2A8F32EA200AC748CAA0064F6EEEA000B948DFBED7FA4660084BCCEAC01000042E37C3E8BA0008446D8751E0C014A0036E69E226C9FFDE2020016A3B454200CBAC01399BEE299337DC52A7E2C2600BF802B274C8848FA02F331D563B3D300566107C0109B4198B5E888200E90021115E31C5120043A31C3E85E400874428D30AA0E3804D32D32EED236459DC6AC86600E4F3B4AAA4C2A10050336373ED536553855301A600B6802B2B994516469EE45467968C016D004E6E9EE7CE656B6D34491D8018E6805E3B01620C053080136CA0060801C6004A801880360300C226007B8018E0073801A801938004E2400E01801E800434FA790097F39E5FB004A5B3CF47F7ED5965B3CF47F7ED59D401694DEB57F7382D3F6A908005ED253B3449CE9E0399649EB19A005E5398E9142396BD1CA56DFB25C8C65A0930056613FC0141006626C5586E200DC26837080C0169D5DC00D5C40188730D616000215192094311007A5E87B26B12FCD5E5087A896402978002111960DC1E0004363942F8880008741A8E10EE4E778FA2F723A2F60089E4F1FE2E4C5B29B0318005982E600AD802F26672368CB1EC044C2E380552229399D93C9D6A813B98D04272D94440093E2CCCFF158B2CCFE8E24017CE002AD2940294A00CD5638726004066362F1B0C0109311F00424CFE4CF4C016C004AE70CA632A33D2513004F003339A86739F5BAD5350CE73EB75A24DD22280055F34A30EA59FE15CC62F9500"

def part1():
    print(versionSum(parseInstructions(data)))
part1()
def part2():
    print(compute(parseInstructions(data)))
part2()
