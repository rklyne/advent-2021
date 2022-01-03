from typing import *
from functools import lru_cache


def run(inputs: List[int]):
    assert len(inputs) == 14
    w = 0
    x = 0
    y = 0
    z = 0
    w, inputs = inputs[0], inputs[1:]
    x *= 0
    x += z
    x %= 26
    z //= 1
    x += 13
    x = 1 if ( x == w) else 0
    x = 1 if ( x == 0) else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 13
    y *= x
    z += y
    w, inputs = inputs[0], inputs[1:]
    x *= 0
    x += z
    x %= 26
    z //= 1
    x += 11
    x = 1 if ( x == w) else 0
    x = 1 if ( x == 0) else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 10
    y *= x
    z += y
    w, inputs = inputs[0], inputs[1:]
    x *= 0
    x += z
    x %= 26
    z //= 1
    x += 15
    x = 1 if ( x == w) else 0
    x = 1 if ( x == 0) else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 5
    y *= x
    z += y
    w, inputs = inputs[0], inputs[1:]
    x *= 0
    x += z
    x %= 26
    z //= 26
    x += -11
    x = 1 if ( x == w) else 0
    x = 1 if ( x == 0) else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 14
    y *= x
    z += y
    w, inputs = inputs[0], inputs[1:]
    x *= 0
    x += z
    x %= 26
    z //= 1
    x += 14
    x = 1 if ( x == w) else 0
    x = 1 if ( x == 0) else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 5
    y *= x
    z += y
    w, inputs = inputs[0], inputs[1:]
    x *= 0
    x += z
    x %= 26
    z //= 26
    x += 0
    x = 1 if ( x == w) else 0
    x = 1 if ( x == 0) else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 15
    y *= x
    z += y
    w, inputs = inputs[0], inputs[1:]
    x *= 0
    x += z
    x %= 26
    z //= 1
    x += 12
    x = 1 if ( x == w) else 0
    x = 1 if ( x == 0) else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 4
    y *= x
    z += y
    w, inputs = inputs[0], inputs[1:]
    x *= 0
    x += z
    x %= 26
    z //= 1
    x += 12
    x = 1 if ( x == w) else 0
    x = 1 if ( x == 0) else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 11
    y *= x
    z += y
    w, inputs = inputs[0], inputs[1:]
    x *= 0
    x += z
    x %= 26
    z //= 1
    x += 14
    x = 1 if ( x == w) else 0
    x = 1 if ( x == 0) else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 1
    y *= x
    z += y
    w, inputs = inputs[0], inputs[1:]
    x *= 0
    x += z
    x %= 26
    z //= 26
    x += -6
    x = 1 if ( x == w) else 0
    x = 1 if ( x == 0) else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 15
    y *= x
    z += y
    w, inputs = inputs[0], inputs[1:]
    x *= 0
    x += z
    x %= 26
    z //= 26
    x += -10
    x = 1 if ( x == w) else 0
    x = 1 if ( x == 0) else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 12
    y *= x
    z += y
    w, inputs = inputs[0], inputs[1:]
    x *= 0
    x += z
    x %= 26
    z //= 26
    x += -12
    x = 1 if ( x == w) else 0
    x = 1 if ( x == 0) else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 8
    y *= x
    z += y
    w, inputs = inputs[0], inputs[1:]
    x *= 0
    x += z
    x %= 26
    z //= 26
    x += -3
    x = 1 if ( x == w) else 0
    x = 1 if ( x == 0) else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 14
    y *= x
    z += y
    w, inputs = inputs[0], inputs[1:]
    x *= 0
    x += z
    x %= 26
    z //= 26
    x += -5
    x = 1 if ( x == w) else 0
    x = 1 if ( x == 0) else 0
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 9
    y *= x
    z += y
    return z == 0

@lru_cache(100000000)
def run_one(w, z, zd, xp, yp):
    x = z % 26  # = last steps w+yp (if x != w)
    if zd == 1:
        x += xp  # some number
        if x != w:
            z *= 26
            z += w + yp
    else:
        z //= 26
        x += xp  # some number
        if x != w:
            z *= 26
            z += w + yp

    return z

Program = List[Tuple[int, int, int]]

program: Program = [
    (1, 13, 13),
    (1, 11, 10),
    (1, 15, 5),
    (26, -11, 14),
    (1, 14, 5),
    (26, 0, 15),
    (1, 12, 4),
    (1, 12, 11),
    (1, 14, 1),
    (26, -6, 15),
    (26, -10, 12),
    (26, -12, 8),
    (26, -3, 14),
    (26, -5, 9),
]

def run2(inputs: List[int]):
    assert len(inputs) == 14
    z = run_program(program, inputs)
    return z == 0


def run_program(programIn, inputs: List[int], z0: int = 0):
    if len(inputs) != len(programIn):
        raise RuntimeError(inputs, programIn)
    data = iter(inputs)
    zs = []
    z = z0
    for zd, xp, yp in programIn:
        z = run_one(next(data), z, zd, xp, yp)
        zs.append(z)
    return z

Runner = Callable[[List[int]], bool]
Model = str

def validate(n: int, runner: Runner = run2, dataLen: int = 14):
    return runner([int(c) for c in str(n).rjust(dataLen, '0')])

def max_program(program: Program) -> Model:
    # (1, la, lb)
    # (26, ra, rb)
    # 1 -> push, 26 -> pop
    # on pop, find matching push. left digit max is min(9-(ra+lb), 9)) r digit max is then min()
    digits: List[int] = [0] * len(program)
    stack = []
    for idx, (zd, xp, yp) in enumerate(program):
        if zd == 1:
            stack.append((idx, yp))
        else:
            prevIdx, prevYp = stack.pop()
            digits[idx] = min(9+(prevYp + xp), 9)
            digits[prevIdx] = min(9- (prevYp + xp), 9)
    return ''.join(map(str, digits))

def min_program(program: Program) -> Model:
    # (1, la, lb)
    # (26, ra, rb)
    # 1 -> push, 26 -> pop
    # on pop, find matching push. left digit max is min(9-(ra+lb), 9)) r digit max is then min()
    digits: List[int] = [0] * len(program)
    stack = []
    for idx, (zd, xp, yp) in enumerate(program):
        if zd == 1:
            stack.append((idx, yp))
        else:
            prevIdx, prevYp = stack.pop()
            digits[idx] = max(1+(prevYp + xp), 1)
            digits[prevIdx] = max(1- (prevYp + xp), 1)
    return ''.join(map(str, digits))


def bruteForce(programIn: Program) -> List[Model]:
    valid: List[Model] = []
    for i in reversed(range(10**len(programIn))):
        if validate(i, lambda inputs: 0 == run_program(programIn, inputs), len(programIn)):
            valid.append(str(i).rjust(len(programIn), '0'))
    return valid

def part1b():
    valid = 0
    for n in range(1, 10):
        if n % 1000000 == 0:
            print(f". {valid}")
        if run2([n]*14):
            valid += 1

    print(valid)

def part1a():
    program1 = [
        (1, 5, 4),
        (26, 8, 16),
        (1, 9, 14),
        (1, 5, 14),
        (26, 8, 16),
        (26, 8, 16),
    ]
    program2 = [
            # (1, la, lb)
            # (26, ra, rb)
            # 1 -> push, 26 -> pop
            # on pop, find matching push. left digit max is min(9-(la+rb), 9)), r digit max is then min(ra, 9) ???
        (1, 4, 6),
        (26, 2, 1),
    ]
    valid = 0
    step = 0
    predict = max_program(program)
    predict2 = min_program(program)
    # model = bruteForce(program)
    model = "???"
    print(f"{model}({predict} / {predict2})  <<<<  {program}")

if __name__ == '__main__':
    print(validate(99999999999999, run))
    part1b()
    part1a()
    print("----")

"""
inp w
mul x 0
add x z
mod x 26
div z 1
add x 13
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 13
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 11
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 10
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 15
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 5
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -11
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 14
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 14
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 5
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x 0
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 15
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 12
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 4
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 12
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 11
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 14
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 1
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -6
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 15
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 12
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -12
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 8
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -3
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 14
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -5
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 9
mul y x
add z y
"""
