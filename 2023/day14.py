from utils import get_input, transpose

def tilt_line(line: str, reverse) -> str:
    spans = line.split('#')
        # 'O' > '.'
    return '#'.join([''.join(sorted(span, reverse=reverse)) for span in spans])
    

def tilt_EW(lines: list[str], west) -> str:
    new_lines = []
    for s in lines:
        new_lines.append(tilt_line(s, west))
    return new_lines

def tilt_NS(s: str, north) -> str:
    new_lines = ['']*len(s)
    for i in range(len(s[0])):
        col = ''.join((s[j][i] for j in range(len(s))))
        new_col = tilt_line(col, north)
        for j, c in enumerate(new_col):
            new_lines[j] += c
    return new_lines

def count_leverage(lines: list[str]) -> int:
    n = len(lines)
    res = 0
    for i, line in enumerate(lines):
        res += (n - i)*line.count('O')
    return res

def cycle(lines: list[str]) -> list[str]:
    s = tilt_NS(lines, True)  # tilt north

    s = tilt_EW(s, True)  # tilt west

    s = tilt_NS(s, False)  # tilt south

    s = tilt_EW(s, False)  # tilt east

    return s


def part1(input: list[str]) -> int:
   tilted = tilt_NS(input, True)
   return count_leverage(tilted)


def part2(input: list[str]) -> int:
    tilted = input
    counts = []
    for i in range(1000):
        tilted = cycle(tilted)
        counts.append(count_leverage(tilted))
    print(counts)


if __name__ == "__main__":
    input = get_input(14, False)
    print(part1(input))

    # Lazy solution for part 2 : print the counts, find the cycle manually and compute the result
    part2(input)
    # cycle = [91333, 91332, 91320, 91306, 91286, 91270, 91278, 91295, 91317], starts at pos 113
    # result = cycle[(10**9 - 1 - pattern_start) % len(cycle)]