from utils import get_input
from dataclasses import dataclass
import re

@dataclass
class Card:
    id: int
    winning: list[int]
    have: list[int]

    def count_matching(self) -> int:
        return len(set(self.have).intersection(set(self.winning)))
        

def parse_line(line: str) -> Card:

    pattern = r"Card\s+(\d+): ([\d\s]+) \| ([\d\s]+)"
    match = re.match(pattern, line)

    if match:
        card_id = int(match.group(1))
        winning_numbers = list(map(int, match.group(2).split()))
        have_numbers = list(map(int, match.group(3).split()))

        # Create a Card object with the parsed values
        return Card(card_id, winning_numbers, have_numbers)
    else:
        print(f"Invalid line format: {line}")


def day4_part1() -> int:
    content = get_input(4)
    tot = 0
    for line in content:
        card = parse_line(line)
        card_matching = card.count_matching()
        if card_matching > 0:
            tot += 2 ** (card_matching - 1)
    return tot


def day4_part2() -> int:
    content = get_input(4)
    card_count = [1] * len(content)
    tot = 0
    for idx, line in enumerate(content):
        card = parse_line(line)
        card_matching = card.count_matching()
        for i in range(card_matching):
            card_count[idx + i + 1] += card_count[idx]

    return sum(card_count)

if __name__ == "__main__":
    print(day4_part1())
    print(day4_part2())