from utils import to_board, get_input
from collections import defaultdict
from functools import partial, lru_cache

def make_grid(m, n, board, start):
    queue = [start]
    grid: dict[tuple[int, int], list[tuple[int, int]]] = defaultdict(list)  # grid is a dict of (x, y) -> (x, y)
    while queue:
        x, y = queue.pop()
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if 0 <= x + dx < m and 0 <= y + dy < n and board[y + dy][x + dx] in ('.', 'S'):
                grid[(x, y)].append((x + dx, y + dy))
                if (x + dx, y + dy) not in grid:
                    queue.append((x + dx, y + dy))
    return grid    
    

def cache_walk(grid, verbose):
    @lru_cache(maxsize=None)
    def func(start, steps):
        if verbose:
            print(start, steps)
        """ from point start, how many points are reachable in *exactly* steps steps? """
        if steps == 0:
            return tuple([start])
        else:
            if verbose:
                print("Going to", ";".join([str(p) for p in grid[start]]), steps - 1)
            unique = set()
            for p in grid[start]:
                res= func(p, steps - 1)
                if verbose:
                    print("Got", res, "for", p, steps - 1)
                unique.update(res)
            return tuple(unique)
    return func

def part1(example=False, verbose=False):
    m, n, board = to_board(get_input(21, example))
    xs, ys = -1, -1
    for y in range(n):
        for x in range(m):
            if board[y][x] == 'S':
                xs, ys = x, y
                break
    
    grid = make_grid(m, n, board, (xs, ys))
    if verbose:
        print("**** grid ****")
        for k, v in grid.items():
            print(k, v)
        print("**** grid ****")
    walk = cache_walk(grid, verbose)
    reached = (walk((xs, ys), 64))
    if verbose:
        for x, y in reached:
            board[y][x] = 'O'
        for row in board:
            print("".join(row))
    print(len(reached))

if __name__ == '__main__':
    part1(False)