import { flatten, transpose } from "ramda";

type row = [number, number, number, number, number];

export type InitialBoard = [row, row, row, row, row];

const toNumbers = (input: string[]) => {
  return input.filter(Boolean).map((txt) => {
    return parseInt(txt);
  });
};

const throwIt = (x: any) => {
  throw new Error(`${JSON.stringify(x)}`);
};

const parseBoard = (input: string): InitialBoard => {
  return input
    .split("\n")
    .map((line) => {
      return toNumbers(line.split(" "));
    })
    .filter((row) => row.length > 0) as InitialBoard;
};

export const parse = (text: string): [number[], InitialBoard[]] => {
  const blocks = text.split("\n\n");

  const numberLine = blocks[0].split(",");
  const numbers: number[] = toNumbers(numberLine);

  const boards: InitialBoard[] = blocks.slice(1).map(parseBoard);

  return [numbers, boards];
};

class Square {
  constructor(public value: number, public marked: boolean = false) {}
}

export class Board {
  private squares: Square[][];
  constructor(private init: InitialBoard) {
    this.squares = init.map((line) => line.map((n) => new Square(n)));
  }

  public mark(n: number) {
    for (const square of flatten(this.squares)) {
      if (square.value == n) {
        square.marked = true;
      }
    }
  }

  public unmarkedSquares(): number[] {
    return flatten(this.squares)
      .filter((square) => !square.marked)
      .map((square) => square.value);
  }

  public isWin(): boolean {
    for (const row of this.squares.concat(transpose(this.squares))) {
      if (row.every((square) => square.marked)) {
        return true;
      }
    }
    return false;
  }
}

export class BingoGame {
  private boards: Board[] = [];

  constructor(boards: InitialBoard[]) {
    this.boards = boards.map((initial) => new Board(initial));
  }
  public run(numbers: number[]): [Board, number] {
    for (const n of numbers) {
      this.boards.forEach((board) => board.mark(n));
      const winners = this.boards.filter(board => board.isWin());
      if (winners.length) {
        return [winners[0], n]
      }
    }
    throw new Error("no winner");
  }
  public findLoser(numbers: number[]): [Board, number] {
    for (const n of numbers) {
      const nonWinners = this.boards.filter(board => !board.isWin());
      this.boards.forEach((board) => board.mark(n));
      const nowNonWinners = this.boards.filter(board => !board.isWin());
      if (nowNonWinners.length == 0) {
        return [nonWinners[0], n]
      }
    }
    throw new Error("no winner");
  }
}
