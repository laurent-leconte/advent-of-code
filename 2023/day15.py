from utils import get_input
from dataclasses import dataclass


@dataclass
class Box:
    index: int
    lenses: list[tuple[str, int]]

    def pop(self, label: str) -> None:
        for i, (l, _) in enumerate(self.lenses):
            if l == label:
                self.lenses.pop(i)
                return
    
    def add(self, label: str, focal: int) -> None:
        for i, (l, _) in enumerate(self.lenses):
            if l == label:
                self.lenses[i] = (l, focal)
                return
        self.lenses.append((label, focal))

    def score(self) -> int:
        score = 0
        for i, (_, f) in enumerate(self.lenses):
            score += (i+1) * f
        return score * (self.index + 1)

def hash(s: str) -> int:
    res = 0
    for c in s:
        res = ((res + ord(c)) * 17) & 255 
    return res

def part1(input: list[str]) -> int:
    res = 0
    for line in input:
        res += hash(line)
    return res


def part2(input: list[str]) -> int:
    boxes = [Box(i, []) for i in range(256)]
    for item in input:
        if '-' in item:
            label = item.split('-')[0]
            idx = hash(label)
            boxes[idx].pop(label)
        elif "=" in item:
            label, focal = item.split('=')
            idx = hash(label)
            boxes[idx].add(label, int(focal))
        else:
            print("Error on input ", item)
    return sum((b.score() for b in boxes))


if __name__ == "__main__":
    input = get_input(15, False)[0].split(',')
    #input = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
    print(part1(input))
    print(part2(input))