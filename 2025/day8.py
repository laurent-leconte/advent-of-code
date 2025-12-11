import math
from collections import defaultdict

from utils import read_input

def read_points() -> list[tuple[int, int, int]]:
    raw_lines = read_input(day=8)
    points = []
    for line in raw_lines:
        x_str, y_str, z_str = line.split(",")
        x, y, z = int(x_str), int(y_str), int(z_str)
        points.append((x, y, z))
    return points


def join_circuits(part1=True) -> int:
    points = read_points()
    distances = []
    num_points = len(points)
    for i in range(num_points):
        x1, y1, z1 = points[i]
        for j in range(i + 1, num_points):
            x2, y2, z2 = points[j]
            dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
            distances.append((dist, i , j))
    # which circuit each point belong to
    # we start with each point in its own circuit
    circuits = list(range(num_points))
    num_circuits = num_points
    # connect circuits according to shortest distances
    distances.sort()
    to_connect = 1000 if part1 else len(distances)
    for _, i, j in distances[:to_connect]:
        # union the circuits
        circuit_i = circuits[i]
        circuit_j = circuits[j]
        if circuit_i == circuit_j:
            continue
        num_circuits -= 1
        if num_circuits == 1 and not part1:
            # Part 2  : all points connected, get the last two points that were connected
            point_i = points[i]
            point_j = points[j]
            return point_i[0] * point_j[0]
        for k in range(num_points):
            if circuits[k] == circuit_j:
                circuits[k] = circuit_i
    # Part 1 : find three largest circuits and multiply their sizes
    circuit_sizes = defaultdict(int)
    for circuit in circuits:
        circuit_sizes[circuit] += 1
    three_largest = sorted(circuit_sizes.values(), reverse=True)[:3]
    return math.prod(three_largest)


if __name__ == '__main__':
    print("Part 1:", join_circuits(True))
    print("Part 2:", join_circuits(False))