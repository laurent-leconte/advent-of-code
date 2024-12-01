def parse_input(input_file):
    walls = []
    with open(input_file, 'r') as f:
        for line in f:
            raw = line.strip().split(' -> ')
            walls.append([tuple(map(int, coords.split(","))) for coords in raw])
    return walls

def dimensions(walls):
    max_x = max_y = 0
    for wall in walls:
        for coords in wall:
            x, y = coords
            if int(x) > max_x:
                max_x = int(x)
            if int(y) > max_y:
                max_y = int(y)
    return max_x, max_y

def part1():
    walls = parse_input('data/day14.dat')
    print(dimensions(walls))


if __name__ == '__main__':
    part1()