import unittest
from textwrap import dedent
from typing import *
import time

Cell = Literal['v', '>', '.']
BLANK: Cell =  '.'
EAST: Cell =  '>'
SOUTH: Cell = 'v'
Board = List[List[Cell]]

class Game(object):
    def __init__(self, board: Board):
        self.board = board
        self.step_count = 0

    @classmethod
    def from_string(cls, data: str) -> 'Game':
        board = [list(line) for line in data.strip().replace(' ', '').split('\n')]
        return cls(board)

    def _make_step(self, f: Callable[[Board, int, int], Cell]) -> Board:
        boardIn = self.board
        newBoard = []
        for y in range(len(boardIn)):
            line: List[Cell] = []
            newBoard.append(line)
            for x in range(len(boardIn[0])):
                line.append(f(boardIn, x, y))
        return newBoard

    @staticmethod
    def _east(board: Board, x: int, y: int) -> Cell:
        current = board[y][x]
        if current == BLANK:
            if x == 0:
                westCell = board[y][len(board[y]) - 1]
            else:
                westCell = board[y][x-1]
            if westCell == EAST:
                return EAST
        if current == EAST:
            eastCell = board[y][(x+1) % len(board[y])]
            if eastCell == BLANK:
                return BLANK
        return current

    @staticmethod
    def _south(board: Board, x: int, y: int) -> Cell:
        current = board[y][x]
        if current == BLANK:
            if y == 0:
                northCell = board[len(board) - 1][x]
            else:
                northCell = board[y-1][x]
            if northCell == SOUTH:
                return SOUTH
        if current == SOUTH:
            southCell = board[(y+1) % len(board)][x]
            if southCell == BLANK:
                return BLANK
        return current

    def run_step(self):
        # 1. move east
        new1: Board = self._make_step(self._east)
        self.board = new1
        # 2. move south
        new2: Board = self._make_step(self._south)
        self.board = new2
        self.step_count += 1

    def run_while(self, f: Callable[[Board, Board], bool]):
        while True:
            oldBoard = self.board
            self.run_step()
            if not f(oldBoard, self.board):
                return

    def run_while_moving(self):
        self.run_while(lambda b1, b2: b1 != b2)

    def __str__(self) -> str:
        return '\n'.join([''.join(line) for line in self.board])

class Tests(unittest.TestCase):

    def test_step_east_no_move(self):
        start = '..\n>v'
        game = Game.from_string(start)
        game.run_step()
        self.assertEqual(str(game), '.v\n>.')

    def test_step_east_move(self):
        start = '.v\n>.'
        game = Game.from_string(start)
        game.run_step()
        self.assertEqual(str(game), '.v\n.>')

    def test_step_south_no_move(self):
        start = '.v\n>.'
        game = Game.from_string(start)
        game.run_step()
        self.assertEqual(str(game), '.v\n.>')

    def test_step_south_move(self):
        start = '.v\n..'
        game = Game.from_string(start)
        game.run_step()
        self.assertEqual(str(game), '..\n.v')

    def test_given_board_step(self):
        start = dedent('''\
                ...>...
                .......
                ......>
                v.....>
                ......>
                .......
                ..vvv..''')
        game = Game.from_string(start)
        game.run_step()
        end = dedent('''\
                ..vv>..
                .......
                >......
                v.....>
                >......
                .......
                ....v..''')
        self.assertEqual(str(game), end)

    def test_given_board_four_steps(self):
        start = dedent('''\
                ...>...
                .......
                ......>
                v.....>
                ......>
                .......
                ..vvv..''')
        game = Game.from_string(start)
        game.run_step()
        game.run_step()
        game.run_step()
        game.run_step()
        end = dedent('''\
                >......
                ..v....
                ..>.v..
                .>.v...
                ...>...
                .......
                v......''')
        self.assertEqual(str(game), end)

    def test_long_run(self):
        start = dedent('''\
                v...>>.vv>
                .vv>>.vv..
                >>.>v>...v
                >>v>>.>.v.
                v>v.vv.v..
                >.>>..v...
                .vv..>.>v.
                v.v..>>v.v
                ....v..v.>
                ''')
        game = Game.from_string(start)
        game.run_while_moving()
        end = dedent('''\
                ..>>v>vv..
                ..v.>>vv..
                ..>>v>>vv.
                ..>>>>>vv.
                v......>vv
                v>v....>>v
                vvv.....>>
                >vv......>
                .>v.vv.v..''')
        self.assertEqual(str(game), end)
        self.assertEqual(58, game.step_count)

if __name__ == '__main__':
    myInput = dedent('''\
        ..v>.vv....vv..v..>>.vvv......v.>.>.v>vv>v>..vv.>vv..>.....v..>.>..v.v.v.....>>vv>>>.>..vv.>..vv...>.v.vv.>>.vv>v..>.vv>.v..vvv>v>>v......v
        vv.>.>..vvv>.>v.v>..>>v.>.v..>>.....v..vv>vv.v....>>.v..>..>.>>v>>....>>>>.v.v>..v.>....v.>v.v>.>>>.v>vv....>>.>.v.>>vv...v.>>.v.vv>..vv...
        v...>...v.>...>..v>..v>.>>vv..>>...>.>.>.....>>...v>..vv.v>>...>.>.>....v>..........v.>vv>..v....v>v....v.v>>>>>..>...>>.vv.v..>v.v.>v..v>.
        vv>.....>..vvv..vv.v....>..v>...vv...>v>..vvv.>....v>.>>>.>vv..vv.>..>v....v..>>>>..>>.>v>>..v>>>v.v>.>>>..vvvv..v.v.>.>v.>vv.>v.v...>.v...
        >.v....v.>.>.v>..v...>..v>..vv...>..v.>..>>.>..vv>.v.>>..v.....>v.>v.v...>.>v....>....v..vvvv....vv...>>v..v>.vvv.v..>.v..v.>v..v.v..v..>.v
        v.vv...>...>v...>...v.>..v....v..>v....>..>.>v>.v.>..>>..v.>....v..v>..>v.v>>>vvv>vv.>...>..>.>..v...>.v...v....>.v..v.v.v..>>.>v.>vv.>vvv.
        .v>.v....>..>.v>..>........v.>>.v.>..vv.>...vv>v..v.>>..v.>v..>v.>.vvv.vv.v.vv.>v...>v>v..vvv>.>>>.v.>.v>>..>.>.vv...v>...>..>v.>>.>.>..v.v
        .v>...>.......>.v..vvv..>.>.>.vv>>v.vvv>.v.>>v>>...>..>.vv..>>...vv.>....>v>>v.vv.>vv>....>>.>>>v.vvvv>....>>>..v>>.>v...>..v.>...v>>..>vv.
        .>>.v>v..v.v..>.v...v>>.>v>..v>v>>.v....vv>>v..v>.v>......vvv.v>..>>>..>.>>>>v..>.v...v>.v..>..>..v...v>v.v........>.vv>..>..>.v.....>...>.
        >v.v.>v>..vvv>.v.v..>.v.>..>..>.v..>v.>vv..>.v...v.v.>>.......v>>>>>v.>..v.>v..v.>....>.>.>>>.>..>..v.>.v>vv....v>v..>>...vv....v>..v>vvv..
        ..v........>v........v>.v.>v......v..v.>v....vv>.v.>>..v..>>vv>.vvv>...>vvv>vvv....v.....vv.v.>.>>.....v.vvv..v....>v>.....v...v...v...>..v
        ..>..>vvvvv>>>...>.>.v..>>.v>vvvvv.>..v.>.v.>>v.v.>>v...>v>.....v..>.>>>.>v>.v>...>..v....v...>..>v.>v.v>vv..vvv..vv.v.v>>v.>.>>>vvvv.>..>.
        ..>..>>vv.v>.>....vv..>v..v>>v.v..vv.>.vv..>...vv>>...>..>>v>v>>..>>..v.>.>..v..v.>>>.>v...>vvv.>.>.......vv....>vv>.....>.v>.>.>.v>>....vv
        v..>>>..v.....>v....vv>....v>>...>vv>.>.>..>.>.>vv.v..v...vv.>vv..v>.>>...v>vv....>.v.v..v...v..>..v.>...>>vv...v>.vvv.vv...v.>v>..>..>>v..
        .>..>v>.>>.v..v>.v...v.....v.>.>.....>..>.vv.>.v.v...>>v>v.....>v>v>>.>.v>>>.v.....v>>.vv.>>>.v>v....v..vv..v..>.>.v>.v....v.>.>.v>v>..>..>
        v.v...v>v..>..>>v.....>.v...>..vvv>......>v.v...>>v.>>..v.>>..v>>v>.>v.>v.>v.....>>..>vv>v.v.v.v..v.....v.>>vv.v.v>.v...>>.>...>>v.v..vv.v>
        ....v.v>v..>.>vv>v...>..v>.v>.vv..>v>vv>....v.vv>..vv.v>.vv>..v..>.>..v......v>>..>v.>v.>>..v....>v>..>.vv>.....v.>...vv.>.v....vv>v>.>>v..
        >.v..v....v.vvvv>.>.>....vv>>>>.......>.>v......vv.vv.>.>>.v...>..>..>.>....>...vv...>>...>>vv>>.v.>...v>.v>.v>>.>.v.>.>...v.v..vvvvv.>.vv.
        .........vv>..>>>v>..vv.v>.v>..v>vv.vvvv...>v.v>>vv>v...>..>.>>v.>v>.v>>>.v>...>.....vv>>.v..vv>>.v.v>.....v..>vv...v>>>v.>..>.v..v.v..>..v
        >....>v...>v.v>>.>.vv.>>vvv.....v..v..v..>...v>.v....>v.....>.v..>.....v.>>.>v>.>vv>v>..>.>>....>.vv>v....>v...v.>.v.v>...>.>>>.vv>>v.v.v>.
        .vv..>.>....v>..v>>.>v>..>...v..>..>.>v.>.>>.v>v....>.>.>...v.>>>v..vv>>..v.>..v.>.>v..>..v.>.>>v>..>v>....>.v.vv>>.v.>.vvv...vvv>..>v.>.>.
        v>.>.>>.v....>..v....vv>.v.>v...>v.v.>..>>>v....v.>>.vv..v.>.>>.>v>>.>v.v>....v.v..>......v..>>.v.v>.v..v.....>.....v>..>...>>>v>>..>>..v.>
        .v..>.>..v.>..vv.......>.>.>..>....v...v.>...v.>.v..v..vv.v.v...>>...v......vv..>v>.....>.v....>.vvv.>v...>>>v...>.v.>>...>......vv..>vv>.>
        ..>.v.>..v....>.vvvv.>.>>v..v..v.>...>v..v>..>>v>....vv>.>.vv...v.>v>>>..v.>...>vv>..v.>>.v.>v>..v>vv.........v..>.>.v.v>.v>..>v.>..v>..>.v
        >vvv...v>.>.v.....v..v>v.>>.>>v....>v>>>>.v>..v...>>...>..vv.v>.v.v.v..v.....>vv>.>.v>....>vvvv......v.>vvv.v>.v>.....v...>.v.v.....>.v>v.v
        >.>..>v.>...v.>.>v.>.>..vv>>.v...vv..v...v>..>.>vv.v>>..>>vv>vv>..>v.vv.v..vv>>v..v....v...>.>v.>v.v>v>.>>.v>>>v>.v.......>v.......>v...>..
        .......>..>>>v....>.v>>..vvvv>>>vv....v..>.vvv>>..v.>.>vv..v....v.v.>.v.>.>v..>>.v>v>>.v....v..>...v>.>...>..>v..v...>..v.>.v>>v>v...>>...v
        ...vv..vv.v.>>..v..>..>>..>vv>.>.v..vv>.>>>>vv>.v>.>>.>>vv..v....v>>v..v>.........>vv.v>>....>>...>.>.>>>v..v..>..>>.>v.>vvv>..>...v>.v>>..
        .>.v>.v>.>v.>v.v.>vvv.....v>..>v..v.>.vvv>.v.>.>v>>>...>..>v.v.v.v>vv.>.v..>.>>>vv>v....vvv>..v..vv.vvv...>..v.v>vv..>vv>v>.>>.v.>..>...v..
        v.v....v>v>v>>...v>.vv.>vv.>..>>.>.v.....v>>.......>..v..v.>.>..v...v.v..>v..>v.>>.vv.>.>v>v..>..>v..v>>>v....v.v>.>>>.>v.v.>.v...>v..v....
        v.....vv..>.>>..>>>..>.v...v>>.>.v..>.>>...v.....>>.>...v.vv..>.>.v.>.v..v>>>..>vv...v....v....v.v.v>.>..vv.>vv....>.>..v.>....>.v>v.v..>.>
        .vvvv.>>.>..>>..v>..>v.v.vv>..>>.>vv.vvvv..>>.v.>.>v.>>>>>v>.>v>.>vvv.>>......>v>....>>vvv>....v.>>.v..>...v.>v>...>..>v>v.v..>.vv>>.v.>.>v
        v>>>>v..v..v...>....>.vv..>.>.v>........>.v.>>...>...>v..v>.>..vv.>.>.>...v>vvvvv>..v.>vvvv.>.>v>.>...>v>..v>.v.>>v>>.v>>.....>.>..v.v.>..v
        >.v.........vvvv>.>.vv...>>>.>...>v.vv>.>>>v..>>v.v>>.>.>>.v...v.>.v>.>..>..v..v.>v....v...v>>v>..>.>>>...v>>>v.>.v.vv>..v>vvv..>.v..v..>v>
        ..v..v......>v>v>.>.>vv....v.>>..vvv>.vvvv..v>>v.>>.>vv.....>.v.>.v>.>.vvv..>..>..v>.vvvv>>.>....>v....v.>>..>...v>...>vv.>..vv>>.v>.>>.v..
        vv.>......>.v>>.....vvvvvv....v.>v...>.....vv>v..>...>>>>.v.>.>.>>.v....v>..v>..vv.>v..vv.>.v...>.>...>v.>v>vv...>>.>......>v>v.v>v.v.>v>v.
        ......v>.vv>...vv>>..>v.>..>...>v.v..>....v.v...>v.>v>....>>.>v.>.v>.v.>>vv>>vvv>>v.>v>..v..>v.v>vv>...v..v...>>v.>v>....>...vv...>..>v..>.
        >.>>v>>v.>.v>.>>>>>.vv...>.v>.>vv.v.>>>..v>v.v..>.vv>.....>......v>.>..>.v..v....>....v..>v..v.v.>.>vv.vv...vv..vv..>>>....vv.>.v.>>>...>..
        .v>>>>>>.vv.>v>>v...v.>.>...>>..v..v.v......v.>v....>..>.v.>v>v.>>>>vv....v.vv.>..v>.vv>>.>v..v.>.>>>v.v...vv>..>>>>.vv>.>.>.vv..v>>..>.vv.
        >.>.v.v>v>....v.v...v.v....>>...vv.....vv.vv>.>..>.>.v.v>..>.>..>.>>......vvv.vvv.>v.>v...>>..v>v.>.v>v>....>..v...>v...>v......>v...vvv>..
        .>.>vv...>.>v>>...v.>>.>>.>.vv...v.>v.>v.vv..>v...v>..>...>>>>>.vv>.v>>.v..>>.>vv>..>...>vvv.>..v>>v>v>v.>.>v......v..>..>...>..>.....>..vv
        >..v...v...v.>v>v.>>v...>>....>.>v.v>>>v.>..v>..vvv.>v..v>>>>>...>.>>v>..>v.v.v..vv...vv.>vv>.>>>.vv>..v.v..>.>...v.>..v>>v>....v...>.....>
        ....vv.>...v.>v.v...>.>.v>.>>>v....>>.>.>.>.v..>.......>.v.>>.v.v..>>v.>>vv..>>>...>.v..v..>.>.>...vv>..v..>vvv.>v.v.v>.>>v.v...v.>v.>>.v..
        ...>>v>...vv>....>>.>...>.....>....>vv>.vv>.>...>..>v.vv..v>..v.....v...>vv>v>>.....v.v.v..v.v.v>>v>>.>>..v>v>>v>.>v.>.v>.vv.vv..vvv.v.>v>.
        .>vv.>>>..>.>....v>.v>v>v...>v..v..>v>>.>>v>...>.vv.vvvv..vv....>>v.>..v....>>.v....v..vv..vv>v>vv..v..v>>.>.......>..>>..>v>...>vv..v>...v
        .v.v...>.vv>>....v.v>.vvv.v.>....v.>.>..v>>>.>...v>.v...>.vv.>.>.>...v.>v.>>..v>....v..v>>vvv..v.>v....v.v>v>v.>v...v>v>>...>>v.vv>v..v.v>.
        ..vv>.>..vv>v..vvvv..>v.v.>v.....>.v>v.>v.v..>.>.v>>....v.vv>.>v.>>......>...v.v......v>....v..>.>..v..v.....>vv>vv......v....v>>.v.v.>v>..
        v>>......v.v>v.v>>>>..>>....v>>.v....>..>>.>v.>>.>v>.v.>vv....v>>....v.>...v.....v>>>v.vvvvv.vv.vvv..>v>.vvv.>.>v.>>..>v>.v.v>...>v....v..>
        ..>>v>..v...vv>...v>>.>.v.>>v...v..v>>v>.>.v>>.>v..>v..>......v.v..v>vv>>>.......vvv...>>vv.vv...v>vv>....v>....>>>vv.vv....v>....v>.v.vv.>
        .v>......v.>v...v>.v.v...>..v..>.v..v...v..v.>..v.>...>.>.v>.v>.v>>....v.vv.>>v.>vv.v.vv.>>v>....>>..v...v.>...>>..>....>...v.>v...vvv.>vv.
        .vv....>v.v.>v...v..v>.v>v>v.v.v>.>..>>>..v.v.>.>>.>.>>>v..>>vvvv.>v.>>>.>.>........>>>....>vv.>.>>v.>>>....v>>.v>..v..>v.>v...>v.....>.vv.
        >vv.v>v.>v..>.vv>....>>...v>..vvvvv.>...vv.v.>..>v.>>......>>v.vv.>..v.>..>.v..v>..>.>v>vv.vv..>v>..v..>vvv..vv.>.>.>>v...>v..>...>.>>>>.vv
        .>.vv.v.vv>>.>>>....>>>.....>.>>..>v...v>>.>.>...vvv..>v.>>.v.vv...v..>..>..>>...vv.>v..vv.v....>.>v....>..v......>>>.v.....>v.v......v.>..
        .>..>v.>v>>.>>>.vv.>.v>...vv>.>v>v...v>..>v.....>.v..v.vvv>>>.>...v...v..v.>.vvv>..>v.>>>.>>>..>v>.>v..v...............vvv>>vvvv>>..>..v.>.
        .vv>>vv>.vv....>>.v.vvvv>.vv...v.v.v...>.>.>v.v>v.>.vv>>.v.v>.>.>>>v.v.>v.v.v>...>..vv>>>vv..v.v.>.v.v.v.>.v>v.v....v>>>..>..v.>v.v..>.>>..
        >vv>>.>.>>.v.>v.>.>.v>.v...>.>.v...>.vv..>..v..v>v..v.>.vvv..v.>v>.>>.vv.>.v..>.vv...vv..>..v..>vv>..vv.v...>....>>..>.v..vv.v..>.>>v..>.v.
        .v...>v>>>>.......vv.v.v..>..>>..>.>..v>..vv........>.v>v...>.v.>>>.>..>.......>>...>.v......vv.v>..vv.v.v..v..>..>.>v...v.v>.>>.>v....>...
        .v...vv>.>..v.>vv...v>v.v>>..>.>>>..v>>.v.v>vv..v.vv>>....v....v..vvv>..v>...v.>vv..vv.>.>.v>>..>>vvv..v.>..>>..>v..v.v..vv>.>>>vvv..v>>.>.
        ....>.>....>.....v>..>>>.vvvv.>vvvvv.....vv.vv>....>.v>.>vv...>..v.vv>.>.v>.>.>.vv.v.>v>.v.....v...v.v>.v>>vv>v.v>...>........>>>>.>v..>..>
        ..v...v.v..v..v.>vv.v>>....vv.>>v>>.>v>.v..>.v..>.....v...v.v..>>.>...>...>..v..v.v..v.v...>v.>v..>...v....>...v..v>.vv>vv.>.v>.>....>..vv.
        .....vv.vvv.>>>v.>v...>.>...v..>>......vvv.v.v...>>v>.v>.vv...v.>..>.>.vv.>>...v..v>.>.>v..v.v.>.vv.>>.v>>vv...>v>....>v.>.>.v..v>>.>>>v..v
        ..>...>.v>v.v.v.>v.v>v>.v.>.v>vv>.v.....>v>v.v.v.v...v>...>..>.>.>..v>.....v>...>....>.v>v..>v>>v..v.vvvv..>..>>.v..>..>>..>..v.>vv.v.vv...
        ...v.v>>.>v.......v>>....>>.>...>.v.vv.>>.>vv>v......>v>>>>>v>.v>v.v.v.....v>..v.>.>...v.v..>>v.v..v...v.v....v.vv.>.>>.v>..v........v..vv.
        .....>>..v>.v>v...v>..v...>>.>...vv.v.vvv>>v.v>...vv..v.......v>vv.>>v...vv>>..v.>.v>>...>>....v..>.vv>vv>..>v>.>>...>>>>......v.v.>v>.....
        >...v...>>..v>.>>...>.>.>v>>...v>v.v....vvv>....v>v>.>vv....v>v..v...>....>v..v..v.>v.v>vvvv..v>v.v..v.>v.vvvv>...v.v.v.>..>>.>.vv.v..>>>.v
        .v.v>>..vv>..vvv>..>.v>..>vv.v>>.>.v..v>.vvvv.....v.>........vv>v.v.v...vvv..>>>>vvv...v.>>>.>>..>.v.>v>>..v...>..>..>.>>.>>vv>vv.v.v.vv>>>
        >...v...v..v.v.>...v.>v.v>..v>...v.....v..>.>>.>v.v..v>>..>.....v..>.v>.>>>...>>..v.>.vvv>...v.....v.>.>.....v..v....>v>.>>.vv.v>v....>>vv.
        ...>....>>....>.>..v.>.v..vv.>.>vvv.....v>>.v....v...>....>.>.>..v.v>.>....>..vv>.v>..>v.>vv.v..>vv.v>.v....>>vvv...v.>.v.v....v..v...v....
        >...v>.v....>..>>v.>..>.>v.>vv...v.v.....v..v..v>.vvv.v>.vv>vv..>vv...vvv....v.>>>..v>.v.>v.v.v.v.>vv>..vv>>...v>v.>>....v.>.v>v.>vv.>.>vv>
        >v.>v.>..>..vv.....vv.>v>.>.vv..v.v.v>.>.>v....v.>.>...>>vv...vv.....vv.v>..>...>.>>.>>..vvvvv.>v>.>>...v..v.>.v.v>vv..>>.v.>v>>>v..v..>>v.
        ..>v.>>>>...v>vv>>...>>.>....>>....>....v>.>...v.>.>>.v.v>v>v.vvvv>v.v>....vv..v.v..v.>...v..>.vvv.>>vvvv.>.>.........>....v..>.v>.vvv.>>.>
        ..v....v.vv>>..v...>.>>vv.v>v>.>.>v..v>..>v...>..>...>.>..v>.v>>>v>>>.>.>.>.v>...v....v..v.>.v.>.>>v>>v>.>>vv.vv>>>.v.>.>>v>.vvv>>v..>.v.>>
        .....>.>.v>...>>>.>..>..>>v.>v.v..v...vvv......vvv.v...v.v..vv.>>>..>v>>...v...>>.v...v>.v.>.>.>.....>..>v.v.v...>v.v.v>>..v>..>...v>>>..v>
        >..>.........>>>>.>.v..v.vv>.v>.>.>v>>vv>v.v>v.v>>>....>v>>.v..>v.v.v.v..vvv.>.v....>.v.....>>>.>v.........>..>v.v....v..v..vv>>>vv.>...>.>
        >>v...>vv.....v>..>v...>.>v...>>.v...>>>.v.v.v.......v>v..>>.>>.>.>>..vv.>..>...>v..v>>>>>v.v>.>.>...>>...>.v>..v.vvvvvvv.v...v.vv>.v...>..
        v>>>..v.v..v.vv>>..v>>>...>.v.v>.v.>...v..>vv...vv>.>>.v>....>>..v>v>vv>..>...v..v.>...v..v..v.v.vv>.>>v..v.>>.>..>v>v>.v.>.>..v.....>v.v>v
        ..>.v..v>...>vv>v>.>....v>>.vv..>>>.v..v.>v.>vv.>>>>>.v.......>..vv>.>>>>....>.v..>..v.vvvvv>>>v..v>.v.>....v>.>...v>>.>...>v....>..>.>..>.
        v>..v...>....v...>>>....v.v>.vv>v>.>.>..>.>vv...>.v..v...v...v..vv..>.v...v.>.>.>>>............>..>...v.....v.>v.v>...v.>.......vv.>......v
        .vv>...v>>....>v.>...vvvvv.>vv>..>...v>..>.......v>v.>vv.v.>>>v.>>.......vv>>..>>.....v>.>v..v......>>>..v>v...vv.>........v.>v>.>..vvv.v..
        ..>.>>>>.vvv.>.vv.v..v>....>.vvvv>..v..vv.>v.....vv>v.....>..>.>.>..v>...vv>>.>v..>>>>v..>.v...vv.vvv.>..v>>v.vv...>>.........vv>.vv.v....v
        v....>>v...>v.v..v...v.v.>..v.....>v....>>v.v..v..v.v>.>v>>>..vv>>..>..v....>.>.v>.v>...>vv>v.....>...vvv>.>.v...v>vv.>...v..v...>vv.>v.>.>
        ....v...>>.v>>>.>v..v.>.>v..v..>.>>..v.v.vvv.>v>.>vvv...>v>>.>.v.>.vv...>...>..>>>.>.v..v..>.vv.v.>>>.>..>vv>.....>>.v>.....>..>v...>vv>>..
        >.>.>.v>.v.v..v>>v.vvv..v>..>.>v..>.>>....v..v>...>v.>v.vv.vv....v>v.>v.vv..>..>v.>vv..>v...>>>.v.v..v>>.>v.v....v.........>.>.vv.v...v>>.>
        vv..>vvv.vvv.>.>vvv>.>v>>vv.>.>.>.v>v>>>.>.v.>>..>.>.v.......>.v.v..>....>vv.vvv...v>..v..>v>vv.v>>>..>v...v..v.v.v>v.>>...v..>...vvv.>.>v>
        v..>.....>..>v..v.vv>v>v.v>v>>.v>..>>.>>.....v..v.v>..vv.v>v>v>.v>>..>.v.>>..>>v.v>.>..v..>v.vv..v.>v.>vvv>>......v...>.>.vvvvv>.>..vv>vvv.
        .....>>>>.>.vv.>>..v.>>...v..>.v..v>...v..>.>>>v>>v>v...>>...>.>..v..v>.>...vv.>....>>>v..v>.vv>...>>..v>.v.v....v>..>......v.>.>....v..vv.
        .....v.v>>..v..>..v..>v...v..>v.v..v...vv.v..v.vvv.>......v>.>>v.v.vv...v...>v>.>>.v.v.>.>.>..>.>>.v......vv>>.v...>>>>>v.>v>>>...>.v.>.v..
        v>......v.>....>>vvv.v.......vv..>>>>.v...v>v>>..vv..vv.v.v.>vv>.v.v.....>vv.v...v.v.....>>>v>....v...>...>>>...>.v..>vvv..v>v>.vv.>..v.>.v
        v.>>..vv.vv>.>v.vv>v>v..v>>.>...v..>>.>>v>..v.......vv..>v...>v.v.>>>>>vv.>>..v..>...v.>>>v.>v>v>.>>v>.>.v...>v.v>v..>>.v>v>....v.vv.>.v>vv
        >.v>.>......>>.........>>..>>>..v..>.v...v.>.....v...v.>>>>.....vv>.>.vv.>vv..>v.>..vv.>.v.>v...v.>....>>vvv>..v>v..>.v>.>...>...vv>......>
        >>>...vvvv>.>.>..>.....>v.....vvv.v>...v>vv.>v.>v>>.....>>.vv.v>>.v..>.>.v......>..>.>>..>...>...vv>>>>.v>>>...>.v>>.....vvv>>....v.>...>..
        >...>v.v>.vv.>v.>.>>.>v..>.>.>..>....>v.v...>........v>>....>>>>.>.vv...v.>>.>>>>v..>>>v.v.v>v.>vv>v..v...>..vvvv.>v...>>..>>.>..v..v>>.>v>
        ..v.v..>v....>.>...>...>>.>.v....>.v.v>v...v.vv>..>..>v.v..>.>vv..>..>v...>v>v>vvv.vvv.v..v.v.>>>..v>.>>v.>v.v.>...>v.>.>>>vv.>.v..v.....v.
        >v>>>..v.>v>>.v.......v.>.>...v>......>.v.>>v.>.>v..>.....>...vv.....v.>.v.v...>vv.>>>>....v..v.v.vv>...vv>v>.....>>>>...v>>.v>vvv>v>v...>.
        v.v>......>....>..vv>vv....>...v.>...v>....>v....>>....v..v.>vv>.>..v>.>v>vv>>vv>v.>v..v.v.v.>.>..v>..v>v...v...>.>v>..v.>....>......vv..>v
        >>v>.>v.>..>vvv..v.>.....>v>.vv>v>>>.>>..>.v.>..v.>...vv.v.vv>vv>v.v....v.v>vv..v>.>v...>>>.>>vv>v.>..v>vvv.v.>v..v.v>vv.v...v..v.v.vv>>..>
        >>.v....>.>v.....v>....>>>..>.>>..>>.....v....>>v...v>..>.>..>>v.>....v>.>v.>>.>.>>v..>.>v.>vv..v>.v.v..v.v.>>>..>.....>vv..>v>.v>.v.vv.v>.
        >v>>v.>v.>..v.......>v.vvvvv>.v......>>..>>.>.>.>v.v.>>v.v>vv.v>>>.>v....v...v..vv>.v..v>v>>..>..v...>>>>....v.>v..>.>.v.>.v>..>.v.vv..vv.v
        .>>.>>>vv.v..>>.vv>>>>..>>..>>.vv.>>v..vvv..vvv...v>v...>.....>....>>...v>..v...>>..vv>.>>v>.v..vv.vvv....>v..vv.....v.>...>>.>..v>.>..vv.v
        >>.vv.v..v....>v...>v>.v>>....v....v.v...>.v>.v>.vvvv.>...v..v>v.vv.>v.vv..>....>...v>...>.>.>.v>>>>>..v.v..v.>>>v.>>.>..>...v.>>.v..>>.v>.
        v>v>..>.>.....v.v>>..>vv.>>v..>>...>v..vv.v>>...vvvv>.v.>>....>v..v...v>....>.v>v.>>..>.>......vv>>v...>.....>vv>v.v>..>vv>>.....>v..v..v>v
        >.>vv>v>vv.>...v.>>>.....>.>.v>>..v>.....v.vv.v.v>>.>v........>...>.....>v..>>..>.>v..v..>v...v..>.>..v>v....>>....v..v>>v>>v>.v.>>.>..>>..
        v.>..>.>v.>v.>.....v.>>v>.v>>.>.>>....v.>.....v.>>.....v.v.vvvv..v...v.vvv....>v>..>v....v>.>>v>>v.>>.v>....>vvv.v>>v.v.>>.>v.>.....v.vvv..
        .vv.v.v>v>vv>.vv>v>....>.v...>.v>v>v>>vv>v>>.v>.v>v>>>vv..v.>v...v..>..>>v..vvv>>.>>>>.>...v>>.>.v.>>..>vvv>....>>>>...v.v.>.v>v>..>>>>>>.>
        .>>......>...v>>v.....>>v...>.v.v.v..>vv.>.>..>.>>.vv>>>.v.v.vv..>.....>>>>>v.>>>>v.vv.>>.>...vv..v....vv>v...vv...v>.vv...vv.v.vv..v>>>v>>
        >>vv..>>>v.>>..v.......>v.v.>....vv>.vv..>>..vvv>.>vv>.>>..v.....>>vv..>v..v>v>vv...>.>vv.v.v>>..>>.v..vv>>.>...v...>v.>v>.v..>>v>v.vvv>v.v
        ..>v>v..>.>>>...>..vv..>..v...........v..>v>...>>v>.>.>vv.>>>..>...vv>vv.v.v.>.v>.>v.>vv..v.v....v>>...v.v.>..>>.>...v..>.v...vv>.>v..>.>..
        .v..>>..>..>.v>>..>>.>vv....>vvv..>....>.>..v.>.....v....v...>>>..>>v..v..>v...vvvv..>vv..>.vvvvv.....>v....>.v..>...v....>>..>..v.>vvv>...
        ...v>>>.>>..>...>.>>..v>.....>..v>>v...v.>>.vv>v..>.>>>>>.>v>.>>....vv>.>v.>.v>>.v..v.>......v>.v>..>>..>...>v.>.>>vv...v>>.>>.v....>>v.>v.
        .v>v......v>.>..v>.>..v.>..vv.>vv>>....vv.vv.>.>>..>>.>....>...v..>.>>>......>.v...v>.>.>....>..>vv>.v.vvv>.v..vv>.>..>>..v>.>.v.v>.vvvvv>v
        ..v>..>...>>v>.vvvvv.v>vv..>v>vvv.>>....v.>>.>.>.v>.>>....>...>>>v>>>vvv..v...vv>.vv>.v.vvv.>v..v>..v.vv>.v..>v.>v...>>v..>v>.vv.vv.>v.>.v>
        >.>..>..>..>v.v.>v>...>..>..>v>v..v>.>.>v.v>.v>vv>...vv.v.>>>...>>..>>.>>.>.>>.>...v..>...v.v..v...>>..v>vv......>...>...>vv.v..v.>.vv....>
        ...>>>v>v..v>>v>>.v..v>v>.>.....v.>.>>vv>v>.v.>>.vv.v.>.vv>v.>>....>>.>>.>vv..v.....vvv>>v.>>.v...>.>>....v.v..v.v.>.v>vv.>.v.>.v.>.>>...>.
        .vv>>>.....>..>v.>v..vv.>....v>v>v>..v>..>>v>v.>...>vvv...v>>.v>vv..v..>v>...v.>>.vv..>..v>>>.>v..>vv...>v.....>...>>.vvvvv.>>.v....v.v>>v.
        ..v...>vvv.vv....>.....v.vv.....v...>.v.>>>.>v.vv>.>>.>v...>..>.>v>v.vv>..v>>v>>>.vv>v.vvv>...>v.>vvvv..>.v.>v.>v.>......>........>>.v..v>v
        .....v..>.v.v>v.>..>v...>...>.>...v.>..>..>..>.vv>..vv.>>vvv.v.>vvvv....>v...>v.v.....v>>.v.>>>>v..>v..v.v>>.>...>>.>..v..>>.v...>.v..v>v>.
        .>...vv>..v>v..v....>.>.>.....>..>..v>.....v.....>v>..v>...>>...v>.....v..vv..v......v.>.>>v.v>>>vv.>>.>v.v..v....v....v...v>..v>..>.vv>>..
        .>..>>>v..v.......v>>..v..v>>vv>>.>.>>>v...v.>v>...v..>v..v.>.>..v>>>.v.v.>>..v>.v.>.>>>v>.vv>.>>...v>v.>>..>v.vv>.v.v..vv>...v.>..>>>..>.>
        >.v>v.v.>..v.vv>..vv..>v.v>.v>v>vv.v.vvv.vv...v......v.>v..vv..>>.v>.v>..>.v.>v>v.>v.....>v>>v.>.>...v.v>>..v>v>v.vv.v..v>..>..>...>v...>..
        ..v>v.vv.v.........vv.v>.>v>vvv..v>v.v..>...v.>.>>v.>...>.vvv...>.vvv>>>.v>....v.vv..>>..v..>.>.v>>>.>v>>.>...v.v..>.......v>.>>v.v>..>>v..
        ...>.v.>v>.v>.>..>>.vv...v..v>.v....>v...v.>v..v.....>v.v.v>>.>v.>.v.>>>>...v>.vvv....v.>>.>.>.>.v..>v.>v.v.v>v>..>...>.>vv.....>>>>v.....>
        >vv.>...>>..v>v..v..v>.>.>>.v>>v>...v.....>vvv..>...v>v>.>.>.>..v..>vv.>.v.>vvv.>......>.v...vv.vv>..>v....vv>>.>v>>vvvv.>...>>..v..vvvv>v>
        vvv>v.vv.>>.....v.>...>.>..vv.v.>v.vv>.>vv........v>v>>..vvv>v>...>>.v>..v.>>....>......>>.v>>vvv......>>>v.>>>>>.>.v.......vv.v..>...vvv>v
        .>vvv>>vvv.vv.vvv..vv>.vv..v>...>.v.>...>.>......>>...v.......>vv>.>..v..v>..vv....v.v>.v.v.v...>>.>vvv.v.>.>.v.>vv..>..v>>..>..v..v..>..>v
        >...>v.v..v>.>.>..v.>..v>.v.v...v..>>.>>v..v>.>....v.....vvv..v.>.>..>v>..>>..v>vvvvv.v.>>....v...v.v>>>vv>..>>.v>.......>>...v....v.>v.v..
        .vv.vv.>>......>>......v.v>v....>v.vv>..>.>.v>..>.v>.>.v.v>>v.v.>.>.vv.v..>>v>.>..v>>...>vv..v.>>v......>...v.vvv>..>..vv.v...v....>....vv.
        >.>..v>>>>.v>....>>.>...v.>.>vv.....>>.v....v..>v>.>.>..>>>vv>>.vv..vv.>>v......v...v..v...v..>vv.v.v.>.v.>>.>.>..v>.v>...>.>.>.v.>v.>v.v>>
        .>.>....>>..v.v..v..>....>>...v..vvv>....>v.>>.>vv..v>.>.>..>>..>.v.v..>v>..>..>>>>>...>vvv..>.v....>.......>>v.......>>>.v....v>.....vvv.v
        .v>>>>...>...>.v.v.v.vvv>vvv>..>>.v...v.vv.>>v>vvv>>.v.v.v>v.>v>v.>>v..>.>>v..vv.vv.>....>..v..v..v>vv.v>vv>.v.>v.v.v>..>v.v>..>..>>v..vv..
        >.......v>v>vv..>>>.v.......v>>..v.>......v..vv>..>>v>v...>.>v.>..v>>.>.v>.>.>>...v..v..>.v.vv>v.......v>..>.>>>.v....v..v.>.>>vvv..vv>v>.>
        ..>..>>.vv....vv>....>>...>>..>>>>.>v>>...vv..>>>v>..vv.....v.v...v>vv.>v.v...>>>.>vv>..v..>.v..vv.v>.>..v.>>..>.>..v...v....v>.>v.....v..>
        >v...v.>>vvv>..>>.vv>>....v>>...v>..>v>..vv.....v..vv>.>.>...>v.v>.>>.v.vvv.v...>.>..vv.vv.>vv.v.>>.....>vv...>.>>>>>v.v.v...v.v..>...vv..>
        ..>.v.>v.v.>...v>...vvvv.v.vv..v...>.>...>.>..v>....>.vv>>v.....>.>>.v...>>v.....v..v>.v.vv>.>vv>>vv.>...>v..v.v>v>.>v...vv.>...>.v...v>>..
        v.v>.v...v.>.>.>.>.>..>.v.v>.v..vv>vv>.>v..>.v>.vv.>>v>v>.....v..v.v.>...v>...>....>..v..v>...vv..v>>..>..>.>v>...v...>..>.vv...v>vv...vv..
        >v>.v>.vv.>.vv..>.>>...v.v.>.v>..>v..>.>v.v>.vv.v.....vvv...>..v>v.>vv..>vvv.>v...v.v....>>.vvvv.v.v>>>vv>>v.>.v.vv>v.>.v>v.....>>.>.vvv.>>
        .>v..v>..v..v>v.v.>>..>.>v..v.>.>..>>.>>>>v>...v>......>>vv...vv.>v>.>.>vvv>>..v...>>..>...v.v.v>>>..>vv>.>.>v>>...>v.v>>...v>v......vv>...
        ..v..vvv.v..v.v..vv>.>...v>vv.>>>.vvvv...v.v>v.>v.>..>vv>>>.....v..v.v.v>...>>>.>....v.vv>v>v..>v>........>..>....>>..v>v...>>v.>.>v>>.>>.>
        ''')
    game = Game.from_string(myInput)
    game.run_while_moving()
    print(str(game))
    print(game.step_count)

