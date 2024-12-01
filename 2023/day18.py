from utils import get_input, Direction

def angle(from_dir: Direction, to_dir: Direction) -> str:
    if from_dir == Direction.UP:
        if to_dir == Direction.LEFT:
            return '7'
        elif to_dir == Direction.RIGHT:
            return 'F'
        else:
            raise ValueError(f"{from_dir} {to_dir}")
    elif from_dir == Direction.DOWN:
        if to_dir == Direction.LEFT:
            return 'J'
        elif to_dir == Direction.RIGHT:
            return 'L'
        else:
            raise ValueError(f"{from_dir} {to_dir}")
    else:
        return angle(to_dir.opposite(),from_dir.opposite())

DIR_FROM_INT = {
    "0": Direction.RIGHT,
    "1": Direction.DOWN,
    "2": Direction.LEFT,
    "3": Direction.UP
}

def parse_line(line: str, part1) -> tuple[Direction, int]:
    first, second, third = line.split(' ')
    if part1:
        return Direction.from_initials(first), int(second)
    hex = third[2:-1]  # remove parentheses and hash
    return DIR_FROM_INT[hex[-1]], int(hex[:-1], 16)


def build_perimeter(input: list[str], part1=True):
    angles = []
    current = 0, 0
    angles.append(current)
    for line in input:
        dir, length = parse_line(line, part1)
        current = dir.apply(*current, length)
        angles.append(current)
    return angles


def shoelace(angles: list[tuple[int,int]]) -> int:
    res = 0
    for idx, (x1, y1) in enumerate(angles[:-1]):
        x2, y2 = angles[idx+ 1]
        res += x1*y2 - y1*x2
        res += abs(x1 - x2) + abs(y1 - y2)
    return res // 2 + 1


def day18(part1, example=False):
    input = get_input(18, example)
    angles = build_perimeter(input, part1) 
    print(shoelace(angles))
    

if __name__ == '__main__':
    print(day18(True))
    print(day18(False))