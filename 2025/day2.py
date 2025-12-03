from utils import get_input
import math

example_ranges = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"

def parse_ranges(range_str) -> list[tuple[int]]:
    ranges = [list(map(int, r.split('-'))) for r in range_str.split(',')]
    return [(r[0], r[1]) for r in ranges]


def invalid_ids(max_digits:int=10, part2=False) -> list[int]:
    result = set()
    upper_limit = 10**max_digits
    target_digits = max_digits // 2
    for i in range(10**target_digits):
        str_i = str(i)
        # For part 1 we only want doubles
        # For part 2 we want doubles, triples, etc.
        max_iter = 2 if not part2 else max_digits
        for repeat in range(2, max_iter+1):
            new_id = int(str_i * repeat)
            if new_id >= upper_limit:
                break
            result.add(new_id)
    return list(result)


def count_invalid_ids(part2=False) -> int:
    range_str = get_input(2)[0]
    # range_str = example_ranges
    ranges = parse_ranges(range_str)
    doubles = invalid_ids(max_digits=10, part2=part2)
    count = 0
    for low, high in ranges:
        for d in doubles:
            if low <= d <= high:
                # print(d, low, high)
                count += d
    return count

if __name__ == "__main__":
    result_part1 = count_invalid_ids(part2=False)
    print(f"Part 1: {result_part1}")
    result_part2 = count_invalid_ids(part2=True)
    print(f"Part 2: {result_part2}")