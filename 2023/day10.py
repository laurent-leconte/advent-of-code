from enum import Enum
from utils import get_input

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def opposite(self):
        return Direction((self.value + 2) % 4)
    
    def translate(self, location: tuple[int, int]) -> tuple[int, int]:
        i, j = location
        if self == Direction.NORTH:
            return (i-1, j)
        elif self == Direction.EAST:
            return (i, j+1)
        elif self == Direction.SOUTH:
            return (i+1, j)
        elif self == Direction.WEST:
            return (i, j-1)
        else:
            raise ValueError(f"Invalid direction {self}")

class Pipe(Enum):
    NORTH_SOUTH = "|" 
    EAST_WEST = "-"
    NORTH_EAST = "L"
    NORTH_WEST = "J"
    SOUTH_WEST = "7"
    SOUTH_EAST = "F"

    def exit(self, entry: Direction) -> Direction:
        one, two = [Direction[name] for name in self.name.split('_')]
        if entry == one:
            return two
        elif entry == two:
            return one
        else:
            raise ValueError(f"Invalid entry direction {entry} for pipe {self}")
        
    def has_direction(self, direction: Direction) -> bool:
        return direction in [Direction[name] for name in self.name.split('_')]


def find_start(map: list[list[str]]):
    for i, row in enumerate(map):
        for j, char in enumerate(row):
            if char == 'S':
                return i, j


def next_tile(map: list[list[str]], current: tuple[int, int], entry: Direction) -> tuple[tuple[int, int], Direction]:
    """ Given the current tile and entry direction, return the next tile and exit direction """
    i, j = current
    pipe = Pipe(map[i][j])
    exit = pipe.exit(entry)
    return exit.translate(current), exit    


def walk_map(map: list[list[str]]) -> list[tuple[int, int]]:
    start = find_start(map)
    for dir in Direction:
        candidate = dir.translate(start)
        if Pipe(map[candidate[0]][candidate[1]]).has_direction(dir.opposite()):
            break
    else:
        raise ValueError(f"Found no suitable neighbor starting from {start}")
    path = [start, candidate]
    current, next_dir = next_tile(map, candidate, dir.opposite())
    while map[current[0]][current[1]] != 'S':
        path.append(current)
        current, next_dir = next_tile(map, current, next_dir.opposite())
    return path


def replace_start(map: list[list[str]], start_coords: tuple[int, int]) -> Pipe:
    connexions =[]
    for dir in [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]:
        candidate = dir.translate(start_coords)
        if Pipe(map[candidate[0]][candidate[1]]).has_direction(dir.opposite()):
            connexions.append(dir)
    assert len(connexions) == 2
    return Pipe[f"{connexions[0].name}_{connexions[1].name}"]


def count_inside(row: str) -> int:
    num_walls = 0
    inside = 0
    start_bend = None
    for char in row:
        if char == ' ':
            if num_walls % 2 == 1:
                # we're inside if we've traversed an odd number of walls
                inside += 1
        elif char == '|':
            num_walls += 1
        elif char == '-':
            continue
        elif char in ['L', 'J', '7', 'F']:
            if start_bend is None:
                assert char in ['L', 'F']
                start_bend = char
            else:
                assert char in ['J', '7']
                if start_bend + char in ('L7', 'FJ'):
                    # one bend goes up, the other goes down: counts as a wall
                    num_walls += 1
                start_bend = None
        else:
            raise ValueError(f"Invalid char {char}")
    return inside


def day10():
    map = get_input(10)
    start = find_start(map)
    # walk path
    path = walk_map(map)
    print("Part 1:", len(path) // 2)
    # replace "S" with the correct pipe
    start_row = map[start[0]]
    j = start[1]
    map[start[0]] = start_row[:j] + replace_start(map, start).value + start_row[j+1:]
    # clean up map: replace unused pipes with spaces
    for i, row in enumerate(map):
        new_row = []
        for j, char in enumerate(row):
            if (i, j) in path:
                new_row.append(char)
            else:
                new_row.append(' ')
        map[i] = ''.join(new_row)
    print("Part 2:", sum([count_inside(row) for row in map]))

if __name__ == "__main__":
    day10()