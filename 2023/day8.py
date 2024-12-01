from utils import get_input
from itertools import cycle
from math import lcm

def parse_maze(lines: list[str]) -> dict[str, list[str]]:
    maze_dict = {}
    for line in lines:
        key, values = line.split(' = ')
        values = values.strip('()').split(', ')
        maze_dict[key] = values
    return maze_dict

def walk_maze(maze: dict[str, list[str]], directions: str) -> int:
    current = 'AAA'
    target = 'ZZZ'
    count = 0
    for direction in cycle(directions):
        if current == target:
            return count
        if direction == 'L':
            current = maze[current][0]
        elif direction == 'R':
            current = maze[current][1]
        count += 1

def find_cycle(maze: dict[str, list[str]], directions: str, start: str) -> int:
    current = start
    count = 0
    targets = []
    for direction in cycle(directions):
        if current.endswith('Z'):
            targets.append(count)
            if len(targets) == 2:
                break
        if direction == 'L':
            current = maze[current][0]
        elif direction == 'R':
            current = maze[current][1]
        count += 1
    first, second = targets
    if first == second - first:
        return first
    else:
        print(f"No cycle for {start} ({first}, {second})")
        return None



def parse_input():
    lines = get_input(8)
    directions = lines[0]
    maze = parse_maze(lines[2:])
    return maze, directions

def part1():
    print(walk_maze(* parse_input()))


def part2():
    maze, directions = parse_input()
    starts = [key for key in maze.keys() if key.endswith('A')]
    cycles = [find_cycle(maze, directions, start) for start in starts]
    print(lcm(*cycles))



if __name__ == "__main__":
    part2()