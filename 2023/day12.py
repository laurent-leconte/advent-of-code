from utils import get_input
from itertools import product
import re
from functools import lru_cache

def parse_line(line: str) -> tuple[str, list[int]]:
    parts = line.split(' ')
    row = parts[0]
    ints = list(map(int, parts[1].split(',')))
    return row, ints

def matches(row: str, ints: list[int]):
    hashes = list(map(len, filter(None, row.split('.'))))
    return hashes == ints


def brute_force(row: str, ints: list[int]) -> int:
    nq = row.count('?')
    subparts = row.split('?')
    count = 0
    for combo in product('.#', repeat=nq):
        new_row = ''
        for i, c in enumerate(combo):
            new_row += subparts[i] + c
        new_row += subparts[-1]
        if matches(new_row, ints):
            count += 1
    return count

def is_prefix(prefix: str, row: str) -> bool:
    if len(prefix) > len(row):
        return False
    return all((p == r or r == '?') for p, r in zip(prefix, row))
    

@lru_cache
def count(row: str, ints: tuple[int]) -> int:
    res = 0
    if len(ints) == 0:
        return 1 if '#' not in row else 0
    cur, rest = ints[0], ints[1:]
    # shortest possible way to combine the remaining springs
    min_rest_len = sum(rest) + len(rest) - 1
    # prefix is .*###. (cur #)
    max_prefix_len = len(row) - min_rest_len
    max_leading_dots = max_prefix_len - cur - 1
    extended_row = row if len(ints) > 1 else row + '.'
    for i in range(max_leading_dots + 1):
        candidate = '.' * i + '#' * cur + '.'
        if is_prefix(candidate, extended_row):
            res += count(row[len(candidate):], rest)
    return res


def day12(input, part2=False):
    res =0
    for line in input:
        row, ints = parse_line(line)
        if part2:
            row ="?".join([row]*5)
            ints = ints * 5
        res += count(row, tuple(ints))
    return res
    

if __name__ == '__main__':
    input = get_input(12)
    print(day12(input))
    print(day12(input, True))