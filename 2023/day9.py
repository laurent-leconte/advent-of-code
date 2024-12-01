from itertools import cycle
from utils import get_input

def build_differences(nums: list[int]) -> list[list[int]]:
    if len(nums) <= 1:
        return []
    
    differences = [nums[i+1] - nums[i] for i in range(len(nums)-1)]
    
    if all(diff == 0 for diff in differences):
        return [differences]
    
    return [differences] + build_differences(differences)

def predict_next(nums: list[int]) -> int:
    diffs = build_differences(nums)
    return nums[-1] + sum([diff[-1] for diff in diffs])


def alt_sum(nums: list[int]) -> int:
    return sum([a*b for a, b in zip(nums, cycle([1, -1]))])


def predict_first(nums: list[int]) -> int:
    diffs = build_differences(nums)
    return nums[0] - alt_sum([diff[0] for diff in diffs])

def part1():
    nums = [list(map(int, line.split(' '))) for line in get_input(9)]
    res = 0
    for num in nums:
        res += predict_next(num)
    print(res)

def part2():
    nums = [list(map(int, line.split(' '))) for line in get_input(9)]
    res = 0
    for num in nums:
        res += predict_first(num)
    print(res)

if __name__ == '__main__':
    part1()
    part2()