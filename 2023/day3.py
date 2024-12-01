from utils import get_input
from dataclasses import dataclass
import re

example1 = [
    "467..114..",
    "...*......",
    "..35..633.",
    "......#...",
    "617*......",
    ".....+.58.",
    "..592.....",
    "......755.",
    "...$.*....",
    ".664.598.."
]

example2 = [
    "12.......*..",
    "+.........34",
    ".......-12..",
    "..78........",
    "..*....60...",
    "78.........9",
    ".5.....23..$",
    "8...90*12...",
    "............",
    "2.2......12.",
    ".*.........*",
    "1.1..503+.56",
]


@dataclass
class Number:
    val: int
    line: int
    start: int
    end: int

    def is_adjacent(self, line, col):
        adjacent_line = abs(self.line - line) <= 1
        adjacent_col = (col >= self.start - 1 and col <= self.end)
        return adjacent_line and adjacent_col
    
@dataclass
class Symbol:
    val: str
    line: int
    col: int

def parse_input(content: list[str]) -> tuple[list[Number], list[tuple[int, int]]]:
    numbers = []
    symbols = []
    for line_idx, line in enumerate(content):
        col_idx = 0
        split = re.split(r"(\.|\d+|.)", line)
        for token in split:
            if token == "":
                continue
            elif token == ".":
                col_idx += 1
            elif token.isdigit():
                numbers.append(Number(int(token), line_idx, col_idx, col_idx + len(token)))
                col_idx += len(token)
            else:
                # symbol
                symbols.append(Symbol(token, line_idx, col_idx))
                col_idx += 1
    print(len(numbers), len(symbols))
    return numbers, symbols

def day3_part1() -> int:
    content = get_input(3)
    numbers, symbols = parse_input(content)

    adj = []
    for number in numbers:
        found = False
        for symbol in symbols:
            if not found and number.is_adjacent(symbol.line, symbol.col):
                adj.append(number.val)
                found = True
    return sum(adj)

def day3_part2() -> int:
    content = get_input(3)
    numbers, symbols = parse_input(content)
    total = 0
    for symbol in symbols:
        if symbol.val == "*":
            gears = []
            for number in numbers:
                if number.is_adjacent(symbol.line, symbol.col):
                    gears.append(number.val)
            if len(gears) == 2:
                total += gears[0] * gears[1]
    return total

if __name__ == "__main__":
    print(day3_part1())
    print(day3_part2())