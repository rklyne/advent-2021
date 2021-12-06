import { countBy, range, sum } from "ramda";

type FishState = Record<string, number>;

const makeFishData = (inputData: number[]): FishState => {
  return {
    '0': 0,
    '1': 0,
    '2': 0,
    '3': 0,
    '4': 0,
    '5': 0,
    '6': 0,
    '7': 0,
    '8': 0,
    ...countBy(n => `${n}`)(inputData)
  }
}

const playCycle = (fishState: FishState): FishState => {
  return {
    '0': fishState['1'],
    '1': fishState['2'],
    '2': fishState['3'],
    '3': fishState['4'],
    '4': fishState['5'],
    '5': fishState['6'],
    '6': fishState['7'] + fishState['0'],
    '7': fishState['8'],
    '8': fishState['0'],
  }
}

const playCycles = (startState: FishState, cycles: number): FishState => {
  return range(0, cycles) .reduce((state) => playCycle(state), startState)
}

describe("day 6", () => {
  it("computes day by day", () => {
    expect(playCycle(makeFishData([
      2,3,2,0,1
    ]))).toStrictEqual(makeFishData([1,2,1,6,0,8]))
  })

  it("part 1", () => {

    expect(playCycles(makeFishData(inputData), 80)).toBe("the answer");
  })
})


const inputData = [
  1,3,4,1,1,1,1,1,1,1,1,2,2,1,4,2,4,1,1,1,1,1,5,4,1,1,2,1,1,1,1,4,1,1,1,4,4,1,1,1,1,1,1,1,2,4,1,3,1,1,2,1,2,1,1,4,1,1,1,4,3,1,3,1,5,1,1,3,4,1,1,1,3,1,1,1,1,1,1,1,1,1,1,1,1,1,5,2,5,5,3,2,1,5,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,5,1,1,1,1,5,1,1,1,1,1,4,1,1,1,1,1,3,1,1,1,1,1,1,1,1,1,1,1,3,1,2,4,1,5,5,1,1,5,3,4,4,4,1,1,1,2,1,1,1,1,1,1,2,1,1,1,1,1,1,5,3,1,4,1,1,2,2,1,2,2,5,1,1,1,2,1,1,1,1,3,4,5,1,2,1,1,1,1,1,5,2,1,1,1,1,1,1,5,1,1,1,1,1,1,1,5,1,4,1,5,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,5,4,5,1,1,1,1,1,1,1,5,1,1,3,1,1,1,3,1,4,2,1,5,1,3,5,5,2,1,3,1,1,1,1,1,3,1,3,1,1,2,4,3,1,4,2,2,1,1,1,1,1,1,1,5,2,1,1,1,2
]
