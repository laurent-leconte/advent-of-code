from utils import get_input
from dataclasses import dataclass
from itertools import combinations

@dataclass
class Map:
    galaxies: list[tuple[int, int]]
    n: int
    m: int

def galaxy_map(input: list[str]) -> Map:
    res = []
    n = len(input)
    m = len(input[0])
    for i, row in enumerate(input):
        for j, char in enumerate(row):
            if char == '#':
                res.append((i, j))
    return Map(res, n, m)


def empty(map: Map) -> tuple[list[int], list[int]]:
    empty_rows = list(range(map.n))
    empty_cols = list(range(map.m))
    row_set = set()
    col_set = set()
    for i, j in map.galaxies:
        row_set.add(i)
        col_set.add(j)
    for i in row_set:
        empty_rows.remove(i)
    for j in col_set:
        empty_cols.remove(j)

    return empty_rows, empty_cols


def dilate(empy: list[int], n: int, dilation: int):
    dilated = list(range(n))
    for i in empy:
        for j in range(i + 1, n):
            dilated[j] += dilation
    return dilated


def expand_galaxies(map: Map, dilation: int) -> list[tuple[int, int]]:
    empty_rows, empty_cols = empty(map)
    new_rows = dilate(empty_rows, map.n, dilation)
    new_cols = dilate(empty_cols, map.m, dilation)
    res = []
    for i, j in map.galaxies:
        res.append((new_rows[i], new_cols[j]))
    return res

def dist(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def measure_distances(galaxies: list[tuple[int, int]]) -> int:
    res = 0
    for gal1, gal2 in combinations(galaxies, 2):
        res += dist(gal1, gal2)
    return res


def day11():
    input = get_input(11)
    map = galaxy_map(input)
    galaxies1 = expand_galaxies(map, 1)
    print("Part 1:", measure_distances(galaxies1))
    galaxies2 = expand_galaxies(map, 10**6 - 1)
    print("Part 2:", measure_distances(galaxies2))


if __name__ == "__main__":
    day11()