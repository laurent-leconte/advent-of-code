from enum import IntEnum
from collections import Counter

from utils import get_input

class Rank(IntEnum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6

CARD_STENGTH = "23456789TJQKA"
CARD_STENGTH_PART_2 = "J23456789TQKA"


def hand_to_int(hand: str, part2=False) -> int:
    """
    Encode a hand as an integer, so that it can be compared to other hands
    """
    if part2:
        scoring = CARD_STENGTH_PART_2
    else:
        scoring = CARD_STENGTH
    res = 0
    for card in hand:
        res = scoring.find(card) + res * len(scoring)
    return res

def rank(hand: str, part2=False) -> Rank:
    counts = Counter(hand)
    num_distinct = len(counts.keys())
    if part2 and "J" in hand:
        # J is wild, turn it into the most common card
        v = counts.pop("J")
        if v == 5:
            # handle the case "JJJJJ"
            return Rank.FIVE_OF_A_KIND
        num_distinct -= 1
        # find most common card and add the wilds to it
        most_common = counts.most_common(1)[0][0]
        counts[most_common] += v

    if num_distinct == 5:
        return Rank.HIGH_CARD
    elif num_distinct == 4:
        return Rank.ONE_PAIR
    elif num_distinct == 1:
        return Rank.FIVE_OF_A_KIND
    elif num_distinct == 3:
        if 3 in counts.values():
            return Rank.THREE_OF_A_KIND
        else:
            return Rank.TWO_PAIR
    elif num_distinct == 2:
        if 4 in counts.values():
            return Rank.FOUR_OF_A_KIND
        else:
            return Rank.FULL_HOUSE
    else:
        raise ValueError("Invalid hand: {}".format(hand))
        

def score(hand: str, part2=False) -> tuple[int, int]:
    """
    Compute a unique score for the hand: first its rank, then the encoded list of cards
    """
    return (rank(hand, part2), hand_to_int(hand, part2))


def day1(part2=False, example=False):
    hands = [line.split() for line in get_input(7, example)]
    # rank the hands according to their score
    def score_func(t):
        return score(t[0], part2)
    hands.sort(key=score_func)
    res = 0
    for idx, (_, bet) in enumerate(hands):
        res += (idx+1) * int(bet)
    print(res)

if __name__ == "__main__":
    day1()
    day1(True)
