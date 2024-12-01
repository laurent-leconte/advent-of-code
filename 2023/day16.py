from utils import get_input
from enum import Enum
from dataclasses import dataclass

class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

    def __str__(self):
        return self.value
    


    def apply(self, x, y):
        if self == Direction.UP:
            return x, y - 1
        elif self == Direction.DOWN:
            return x, y + 1
        elif self == Direction.LEFT:
            return x - 1, y
        elif self == Direction.RIGHT:
            return x + 1, y


class Tile(Enum):
    EMPTY = '.'
    RIGHT_DOWN_MIRROR = '\\'
    RIGHT_UP_MIRROR = '/'
    VERT_SPLIT = '|'
    HORIZ_SPLIT = '-'

    def __str__(self):
        return self.value


def travel(tile: Tile, direction: Direction) -> list[Direction]:
    if tile == Tile.EMPTY:
        return [direction]
    elif tile == Tile.RIGHT_DOWN_MIRROR:
        if direction == Direction.UP:
            return [Direction.LEFT]
        elif direction == Direction.RIGHT:
            return [Direction.DOWN]
        elif direction == Direction.DOWN:
            return [Direction.RIGHT]
        elif direction == Direction.LEFT:
            return [Direction.UP]
    elif tile == Tile.RIGHT_UP_MIRROR:
        if direction == Direction.UP:
            return [Direction.RIGHT]
        elif direction == Direction.RIGHT:
            return [Direction.UP]
        elif direction == Direction.DOWN:
            return [Direction.LEFT]
        elif direction == Direction.LEFT:
            return [Direction.DOWN]
    elif tile == Tile.VERT_SPLIT:
        if direction in (Direction.DOWN, Direction.UP):
            return [direction]
        else:
            return [Direction.DOWN, Direction.UP]
    elif tile == Tile.HORIZ_SPLIT:
        if direction in (Direction.LEFT, Direction.RIGHT):
            return [direction]
        else:
            return [Direction.LEFT, Direction.RIGHT]
        

def next_step(grid, x, y, direction)-> list[tuple[int, int, Direction]]:
    tile = Tile(grid[y][x])
    # print(f"Entering {x}, {y}, moving {str(direction)}; tile is {tile}")
    directions = travel(tile, direction)
    outcome = [(*d.apply(x, y), d) for d in directions]
    # print(f"Outcome: {outcome}")
    return outcome


def walk_grid(grid, start):
    ymax = len(grid)
    xmax = len(grid[0])
    def in_grid(step):
        x, y, _ = step
        return 0 <= x < xmax and 0 <= y < ymax
    seen = set()
    stack = [start]
    while stack:
        x, y, direction = stack.pop()
        if (x, y, direction) in seen:
            continue
        seen.add((x, y, direction))
        to_add = list(filter(in_grid, next_step(grid, x, y, direction)))
        # print("Adding", to_add)
        stack.extend(to_add)
    
    coords = set()
    for x, y, _ in seen:
        coords.add((x, y))
    new_grid = [['.'] * xmax for _ in range(ymax)]
    for x, y in coords:
        new_grid[y][x] = '#'
    return len(coords)

def part1(grid):
    start = (0, 0, Direction.RIGHT)
    return walk_grid(grid, start)


def part2(grid):
    ymax = len(grid)
    xmax = len(grid[0])
    max_grid = 0
    for y in range(ymax):
        start = (0, y, Direction.RIGHT)
        max_grid = max(max_grid, walk_grid(grid, start))
        start = (xmax - 1, y, Direction.LEFT)
        max_grid = max(max_grid, walk_grid(grid, start))
    for x in range(xmax):
        start = (x, 0, Direction.DOWN)
        max_grid = max(max_grid, walk_grid(grid, start))
        start = (x, ymax - 1, Direction.UP)
        max_grid = max(max_grid, walk_grid(grid, start))
    return max_grid


if __name__ == "__main__":
    grid = get_input(16, False)
    print(part1(grid))
    print(part2(grid))