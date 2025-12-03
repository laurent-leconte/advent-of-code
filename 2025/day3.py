from utils import get_input

def split_input(s: str) -> list[int]:
    return [int(c) for c in s.strip()]  # Convert each character to an integer

def find_largest_pair(digits: list[int]) -> int:
    first, second = -1, -1
    n = len(digits)
    for idx, d in enumerate(digits):
        if d > first and idx < n-1:
            # new best first digit. Store it and reset second digit
            first = d
            second = -1
            continue
        if d > second:
            second = d
    return first * 10 + second


def find_largest_ngram(digits: list[int], n: int) -> int:
    """
    Find the larget n-gram subset in a list of digits recursively.
    First, find the leftmost largest digit in [0..len(digits)-n+1].
    Call its index i0.
    Then, recursively find the largest (n-1)-gram in [i0+1..n]
    """
    if n == 1:
        return max(digits)
    max_d = -1
    for idx, d in enumerate(digits[:len(digits)-n+1]):
        if d > max_d:
            max_d = d
            i0 = idx
    return max_d * (10 ** (n-1)) + find_largest_ngram(digits[i0+1:], n-1)


def solve(input_lines: list[str], n: int) -> int:
    return sum(
        map(
            lambda line: find_largest_ngram(split_input(line), n),
            input_lines
        )
    )

examples = [
    "987654321111111",
    "811111111111119",
    "234234234234278",
    "818181911112111"
]

def test_algo(input_lines: list[str]) -> None:
    for line in input_lines:
        digits = split_input(line)
        res2 = find_largest_ngram(digits, 2)
        res_pair = find_largest_pair(digits)
        assert res2 == res_pair, f"Mismatch for line {line}: {res2} != {res_pair}"

if __name__ == "__main__":
    print("Part 1:", solve(get_input(day=3), 2))
    print("Part 2:", solve(get_input(day=3), 12))