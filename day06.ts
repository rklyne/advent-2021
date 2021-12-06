import { countBy, range, sum } from "ramda";

type FishState = Record<string, number>;

const fillState = (upTo: number, initial: number = 0): FishState => {
  const state: Record<string, number> = {};
  range(0, upTo + 1).forEach((n) => {
    state[`${n}`] = initial;
  });
  return state;
};

export const makeFishData = (inputData: number[], upTo: number = 8): FishState => {
  return {
    ...fillState(upTo),
    ...countBy((n) => `${n}`)(inputData),
  };
};

export const total = (state: FishState): number => {
  return sum(Object.values(state))
}

export const playCycle = (fishState: FishState): FishState => {
  return {
    "0": fishState["1"],
    "1": fishState["2"],
    "2": fishState["3"],
    "3": fishState["4"],
    "4": fishState["5"],
    "5": fishState["6"],
    "6": fishState["7"] + fishState["0"],
    "7": fishState["8"],
    "8": fishState["0"],
  };
};

export const playCycle2 = (fishState: FishState): FishState => {
  return {
    ...Object.fromEntries(
      Object.entries(fishState).filter(([k, v]) => k != "0").map(([k, v]) => [`${parseInt(k)-1}`, v])
    ),
    "6": fishState["7"] + fishState["0"],
    "8": fishState["0"],
  }
};

export const playCycles = (
  startState: FishState,
  cycles: number,
  playCycle: (state: FishState) => FishState
): FishState => {
  return range(0, cycles).reduce((state) => playCycle(state), startState);
};


