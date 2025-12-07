from utils import read_input

def parse_input() -> tuple[list[tuple[int, int]], list[int]]:
    raw_lines = read_input(day=5)
    ranges = []
    ids = []
    for line in raw_lines:
        if "-" in line:
            start_str, end_str = line.split("-")
            ranges.append((int(start_str), int(end_str)))
        elif line:
            ids.append(int(line))
        else:
            # empty line, skip
            continue
    return ranges, ids

def part1() -> int:
    ranges, ids = parse_input()
    valid_count = 0
    for id_ in ids:
        for (start, end) in ranges:
            if start <= id_ <= end:
                valid_count += 1
                break
    return valid_count

def part2() -> int:
    ranges, _ = parse_input()
    ranges = sorted(ranges, key=lambda x: x[0])
    merged_ranges = []
    current_start, current_end = ranges[0]
    for (start, end) in ranges[1:]:
        # end the current range if start > current_end + 1
        if start > current_end + 1:
            merged_ranges.append((current_start, current_end))
            current_start, current_end = start, end
        else:
            # merge new range with the current one
            current_end = max(current_end, end)
    merged_ranges.append((current_start, current_end))
    return sum(end - start + 1 for (start, end) in merged_ranges)

if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())