import { identity, range, sortBy } from "ramda";

type Coord = [number, number];
type Coords = [Coord, Coord];
export type InputData = Coords[];

export type AreaMap = number[][];

const throwIt = (x: any) => {
  throw new Error(`${JSON.stringify(x)}`);
};

export const printMap = (map: AreaMap): string => {
  return map.map((line) => line.map((x) => `${x}`).join("")).join("\n");
};

export const diagonalRange = (input: Coords): Coord[] => {
  const [[x0, y0], [x1, y1]] = input;
  const xDir = x1 > x0 ? 1 : -1;
  const yDir = y1 > y0 ? 1 : -1;
  return range(0, Math.abs(x0 - x1) + 1).map((incr) => [
    x0 + xDir * incr,
    y0 + yDir * incr,
  ]);
};

export const buildMap = (
  inputData: InputData,
  size: [number, number],
  diagonals: boolean = false
): AreaMap => {
  const map = new Array(size[1]).fill(false).map((x) => {
    return new Array(size[0]).fill(0);
  });

  for (const input of inputData) {
    const [[ix0, iy0], [ix1, iy1]] = input;
    const [x0, x1] = sortBy(identity, [ix0, ix1]);
    const [y0, y1] = sortBy(identity, [iy0, iy1]);
    const invertX = ix0 < ix1;
    const invertY = iy0 < iy1;
    if (ix0 != ix1 && iy0 != iy1) {
      if (diagonals) {
        for (const position of diagonalRange(input)) {
          const [x, y] = position;
          map[y][x] += 1;
        }
      }
      continue;
    }
    for (const x of range(x0, x1 + 1)) {
      for (const y of range(y0, y1 + 1)) {
        map[y][x] += 1;
      }
    }
  }

  return map;
};
