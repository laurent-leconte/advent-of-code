from utils import read_input
from operator import mul, add
from functools import reduce
import re

def compute_row_part1(line: list[str]) -> int:
    op = add if line[-1] == '+' else mul
    result = reduce(op, (int(x) for x in line[:-1]))
    return result

def part1() -> int:
    raw_lines = read_input(day=6)
    split_lines = [line.split() for line in raw_lines]
    total = sum(compute_row_part1(row) for row in zip(*split_lines))
    return total


def part2() -> int:
    raw_lines = read_input(day=6)
    current_operands = []
    current_op = None
    total = 0
    for row in zip(*raw_lines):
        row_str = ''.join(row[:-1])
        if row_str.strip() == "" and current_op:
            # a blank line indicates end of current operation
            if current_op == '+':
                total += sum(current_operands)
            else:
                total += reduce(mul, current_operands)
            # reset accs for next operation
            current_operands = []
            current_op = None
            continue
        # We're within an operation
        if not current_op:
            # grab operator if we haven't yet
            current_op = row[-1]
        current_operands.append(int(row_str.strip()))
    # compute the last operation
    if current_op == '+':
        total += sum(current_operands)
    else:
        total += reduce(mul, current_operands)
    return total

if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())