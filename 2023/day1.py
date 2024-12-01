from utils import get_input

def digits_in_string(string: str, written=False) -> int:
    res = []
    for idx, char in enumerate(string):
        if char.isdigit():
            res.append(int(char))
        elif written:
            d = is_written_digit(idx, string)
            if d is not None:
                res.append(d)
    return res

def is_written_digit(idx: int, string: str) -> bool:
    digits = {
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four" : 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8, 
        "nine": 9,
        "ten": 0,
        "eleven": 1,
        "twelve": 2,
        "thirteen": 3,
        "fourteen" : 4,
        "fifteen": 5,
        "sixteen": 6,
        "seventeen": 7,
        "eighteen": 8,
        "nineteen": 9,
    }
    for d in digits:
        n = len(d)
        if len(string) >= idx+n and string[idx:idx+n] == d:
            return digits[d]



def day1(written=False):
    content = get_input(1)
    total = 0
    for line in content:
        d = digits_in_string(line, written)
        first = d[0]
        last = d[-1]
        total += 10*first + last
    print(total)

if __name__ == "__main__":
    day1()
    day1(True)