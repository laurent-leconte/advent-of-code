from utils import read_input

def parse_input() -> list[tuple[str, int]]:
    lines = read_input(1)
    combinations = []
    for line in lines:
        combinations.append((line[0], int(line[1:])))
    return combinations

def count_zeroes(combinations: list[tuple[str, int]], any_click=False) -> int:
    position = 50
    count_zeros = 0
    for letter, number in combinations:
        if letter == 'L':
            new_position = position - number
        elif letter == 'R':
            new_position = position + number
        if new_position % 100 == 0:
            # we land on zero
            count_zeros += 1
        if any_click:
            # count all the times we passed 0 (i.e. every 100 steps)
            passed_zeroes = abs(new_position // 100)
            if new_position % 100 == 0 and new_position > 0:
                # if we land on zero going right, we overcounted one (landing already counted above)
                # not an issue going left due to how integer division works
                passed_zeroes -= 1
            if position == 0 and new_position < 0:
                # if we start on zero going left, we overcounted one
                passed_zeroes -= 1
            count_zeros += passed_zeroes
        position = new_position % 100
    return count_zeros

if __name__ == "__main__":
    input_data = parse_input()
    result_part1 = count_zeroes(input_data)
    result_part2 = count_zeroes(input_data, any_click=True)
    print(f"Part 1: {result_part1}")
    print(f"Part 2: {result_part2}")