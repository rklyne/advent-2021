from functools import lru_cache
import pprint
import typing
from typing import *
import itertools
from textwrap import dedent
import unittest



class Tests(unittest.TestCase):
    input = dedent("""\
    5283751526""").strip()

    def test_small(self):
        edges = dedent("""\
            start-A
            start-b
            A-c
            A-b
            b-d
            A-end
            b-end
        """).strip()
        expected_paths = dedent("""\
            start,A,b,A,c,A,end
            start,A,b,A,end
            start,A,b,end
            start,A,c,A,b,A,end
            start,A,c,A,b,end
            start,A,c,A,end
            start,A,end
            start,b,A,c,A,end
            start,b,A,end
            start,b,end
        """).strip()
        paths = print_paths(find_paths(make_map(edges), is_allowed_1))
        self.assertEqual(expected_paths, paths)

    def test_medium(self):
        edges = dedent("""\
            dc-end
            HN-start
            start-kj
            dc-start
            dc-HN
            LN-dc
            HN-end
            kj-sa
            kj-HN
            kj-dc
        """).strip()
        expected_paths = dedent("""\
            start,HN,dc,HN,end
            start,HN,dc,HN,kj,HN,end
            start,HN,dc,end
            start,HN,dc,kj,HN,end
            start,HN,end
            start,HN,kj,HN,dc,HN,end
            start,HN,kj,HN,dc,end
            start,HN,kj,HN,end
            start,HN,kj,dc,HN,end
            start,HN,kj,dc,end
            start,dc,HN,end
            start,dc,HN,kj,HN,end
            start,dc,end
            start,dc,kj,HN,end
            start,kj,HN,dc,HN,end
            start,kj,HN,dc,end
            start,kj,HN,end
            start,kj,dc,HN,end
            start,kj,dc,end
        """).strip()
        paths = print_paths(find_paths(make_map(edges), is_allowed_1))
        self.assertEqual(expected_paths, paths)

    def test_medium_2(self):
        edges = dedent("""\
            dc-end
            HN-start
            start-kj
            dc-start
            dc-HN
            LN-dc
            HN-end
            kj-sa
            kj-HN
            kj-dc
        """).strip()
        paths = find_paths(make_map(edges), is_allowed_2)
        self.assertEqual(103, len(paths))

def make_map(text):
    cave_map = {}
    for line in text.split("\n"):
        src, dst = line.split("-")
        cave_map.setdefault(src, set()).add(dst)
        cave_map.setdefault(dst, set()).add(src)
    return cave_map

def print_paths(paths):
    return "\n".join([','.join(path) for path in sorted(paths)])

@lru_cache
def is_small(cave: str):
    return cave.lower() == cave

def is_allowed_1(cave, past):
    return not (is_small(cave) and cave in past)

@lru_cache(10000000)
def is_allowed_2(cave, past):
    if cave == 'start': return False
    if len(past) > 16:
        return False
    if not is_small(cave):
        return True
    visited_small_caves = list(filter(is_small, past))
    if len(set(visited_small_caves)) == len(visited_small_caves):
        return True
    return cave not in past

def find_paths(cave_map, is_allowed):
    def search(src, path):
        path = path + [src]
        if src == 'end':
            return [path]
        paths = []
        for node in cave_map.get(src, []):
            if not is_allowed(node, tuple(path)):
                continue
            paths.extend(search(node, path))
        return paths
    return list(search('start', []))

myInput = """
re-js
qx-CG
start-js
start-bj
qx-ak
js-bj
ak-re
CG-ak
js-CG
bj-re
ak-lg
lg-CG
qx-re
WP-ak
WP-end
re-lg
end-ak
WP-re
bj-CG
qx-start
bj-WP
JG-lg
end-lg
lg-iw
""".strip()

def part1(input):
    caves = make_map(input)
    paths = find_paths(caves, is_allowed_1)
    count = 0
    for path in paths:
        if any(is_small(cave) for cave in path):
            count += 1
    return count

def part2(input):
    caves = make_map(input)
    paths = find_paths(caves, is_allowed_2)
    count = 0
    for path in paths:
        if any(is_small(cave) for cave in path):
            count += 1
    return count

print(part1(myInput))
print(part2(myInput))

