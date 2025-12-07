from utils import read_input
from collections import defaultdict

def walk_the_tachyon_manifold() -> tuple[int, dict[int, int]]:
    raw_lines = read_input(day=7)
    start_idx = raw_lines[0].index("S")
    current_row = defaultdict(int)
    current_row[start_idx] = 1
    num_splits = 0
    for line in raw_lines[2:]:
        new_row = defaultdict(int)
        # for each current beam, either split or continue straight
        for idx, val in current_row.items():
            if line[idx] == '^':
                num_splits += 1
                new_row[idx - 1] += val
                new_row[idx + 1] += val
            else:
                new_row[idx] += val
        current_row = new_row
    return (num_splits, current_row)

if __name__ == '__main__':
    num_splits, multiverse = walk_the_tachyon_manifold()
    print("Part 1:", num_splits)
    print("Part 2:", sum(multiverse.values()))