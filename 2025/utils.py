from enum import IntEnum
from typing import Any

class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    
    def __str__(self):
        return self.name
    
    @staticmethod
    def from_initials(letter: str):
        if letter == 'U':
            return Direction.UP
        elif letter == 'D':
            return Direction.DOWN
        elif letter == 'R':
            return Direction.RIGHT
        elif letter == 'L':
            return Direction.LEFT
        else:
            raise ValueError(letter)

    def apply(self, x, y, n=1):
        if self == Direction.UP:
            return x, y - n
        elif self == Direction.DOWN:
            return x, y + n
        elif self == Direction.LEFT:
            return x - n, y
        elif self == Direction.RIGHT:
            return x + n, y
        
    def opposite(self):
        return Direction((self.value + 2) % 4)
    
    def perpendicular(self):
        if self in (Direction.UP, Direction.DOWN):
            return Direction.LEFT, Direction.RIGHT
        else:
            return Direction.UP, Direction.DOWN


def read_input(day: int, example=False, split_line=True) -> str:
    file = f"inputs/day{day}.dat"
    if example:
        file += "_example"
    with open(file, "r") as f:
        content = f.read()
        if split_line:
            return content.splitlines()
        else:
            return content
        
def split_by_empty_line(input: list[str]) -> list[list[str]]:
    """
    Split a list of strings by empty lines, return a list of lists of strings
    """
    acc = []
    res = []
    for line in input:
        if line == '':
            res.append(acc)
            acc = []
        else:
            acc.append(line)
    if acc:
        res.append(acc)
    return res


def transpose(lines: list[str]) -> list[str]:
    rows = [''] * len(lines[0])
    for line in lines:
        for i, c in enumerate(line):
            rows[i] += c
    return rows


def to_board(lines: list[str]) -> tuple[int, int, list[list[str]]]:
    """
    Convert a list of strings into a 2D array of characters
    """
    return len(lines[0]), len(lines), [list(line) for line in lines]


def to_int_board(lines: list[str]) -> tuple[int, int, list[list[int]]]:
    """
    Convert a list of strings into a 2D array of integers
    """
    return len(lines[0]), len(lines), [[int(c) for c in line] for line in lines]


def pad_board(board: list[list[Any]], pad_char: Any) -> list[list[Any]]:
    """
    Pad a 2D array with a border of pad_char
    """
    width = len(board[0])
    padded_board = [[pad_char] * (width + 2)]
    for row in board:
        padded_board.append([pad_char] + row + [pad_char])
    padded_board.append([pad_char] * (width + 2))
    return padded_board