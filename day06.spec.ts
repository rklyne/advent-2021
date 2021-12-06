import { playCycle, playCycle2, playCycles, makeFishData, total } from "./day06";

describe("day 6", () => {
  it("computes day by day", () => {
    expect(playCycle(makeFishData([2, 3, 2, 0, 1]))).toStrictEqual(
      makeFishData([1, 2, 1, 6, 0, 8])
    );
  });

  it("computes day by day part 2", () => {
    expect(playCycle2(makeFishData([2, 3, 2, 0, 1]))).toStrictEqual(
      makeFishData([1, 2, 1, 6, 0, 8])
    );
  });

  it("part 1", () => {
    expect(total(playCycles(makeFishData(inputData), 80, playCycle2))).toBe(
      "the answer"
    );
  });

  it("part 2", () => {
    expect(total(playCycles(makeFishData(inputData), 256, playCycle2))).toBe(
      "the answer"
    );
  });
});

const inputData = [
  1,
  3,
  4,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  2,
  2,
  1,
  4,
  2,
  4,
  1,
  1,
  1,
  1,
  1,
  5,
  4,
  1,
  1,
  2,
  1,
  1,
  1,
  1,
  4,
  1,
  1,
  1,
  4,
  4,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  2,
  4,
  1,
  3,
  1,
  1,
  2,
  1,
  2,
  1,
  1,
  4,
  1,
  1,
  1,
  4,
  3,
  1,
  3,
  1,
  5,
  1,
  1,
  3,
  4,
  1,
  1,
  1,
  3,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  5,
  2,
  5,
  5,
  3,
  2,
  1,
  5,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  2,
  1,
  1,
  1,
  1,
  5,
  1,
  1,
  1,
  1,
  5,
  1,
  1,
  1,
  1,
  1,
  4,
  1,
  1,
  1,
  1,
  1,
  3,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  3,
  1,
  2,
  4,
  1,
  5,
  5,
  1,
  1,
  5,
  3,
  4,
  4,
  4,
  1,
  1,
  1,
  2,
  1,
  1,
  1,
  1,
  1,
  1,
  2,
  1,
  1,
  1,
  1,
  1,
  1,
  5,
  3,
  1,
  4,
  1,
  1,
  2,
  2,
  1,
  2,
  2,
  5,
  1,
  1,
  1,
  2,
  1,
  1,
  1,
  1,
  3,
  4,
  5,
  1,
  2,
  1,
  1,
  1,
  1,
  1,
  5,
  2,
  1,
  1,
  1,
  1,
  1,
  1,
  5,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  5,
  1,
  4,
  1,
  5,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  2,
  1,
  1,
  1,
  1,
  5,
  4,
  5,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  5,
  1,
  1,
  3,
  1,
  1,
  1,
  3,
  1,
  4,
  2,
  1,
  5,
  1,
  3,
  5,
  5,
  2,
  1,
  3,
  1,
  1,
  1,
  1,
  1,
  3,
  1,
  3,
  1,
  1,
  2,
  4,
  3,
  1,
  4,
  2,
  2,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  5,
  2,
  1,
  1,
  1,
  2,
];
