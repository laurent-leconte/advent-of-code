from utils import get_input, split_by_empty_line, transpose

def is_symmetrical(lines, i):
    first = reversed(lines[:i])
    second = lines[i:]
    return all((l1 == l2 for l1, l2 in zip(first, second)))


def count_diff(lines: list[str], i: int) -> int:
    first = reversed(lines[:i])
    second = lines[i:]
    def count_diff_line(l1, l2):
        return sum((c1 != c2 for c1, c2 in zip(l1, l2)))
    return sum((count_diff_line(l1, l2) for l1, l2 in zip(first, second)))


def test_puzzle(puzzle: list[str], part2: bool) -> tuple[int, int]:
    """
    Returns nb_of_cols, nb_of_rows : one of these will always be 0
    """
    target = 1 if part2 else 0
    for i in range(1, len(puzzle)):
        if count_diff(puzzle, i) == target:
            return 0, i
    transposed = transpose(puzzle)
    for i in range(1, len(transposed)):
        if count_diff(transposed, i) == target:
            return i, 0
    print("No symmetrical puzzle found")

def day13(example=False, part2=False):
    input = get_input(13, example)
    puzzles = split_by_empty_line(input)
    tot_cols, tot_rows = 0, 0
    for puzzle in puzzles:
        cols, rows = test_puzzle(puzzle, part2)
        tot_cols += cols
        tot_rows += rows
    print(100*tot_rows + tot_cols)


if __name__ == "__main__":
    day13(False, True)
    