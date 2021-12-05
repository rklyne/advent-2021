import math

def most_common(digits):
  mean = (sum(digits) / len(digits))
  return math.floor(mean + 0.5)

def least_common(digits):
  mean = (sum(digits) / len(digits))
  if mean == 0.5:
    return 0
  return 1 - most_common(digits)

f = most_common

def search(binaries, f=most_common, digit=0):
  print(digit, len(binaries))
  target = f([int(binary[digit]) for binary in binaries])
  subset = [binary for binary in binaries if binary[digit] == str(target)]
  if len(subset) == 1:
    return int(subset[0], 2)
  return search(subset, f, digit + 1)


