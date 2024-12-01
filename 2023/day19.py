from utils import get_input, split_by_empty_line
from dataclasses import dataclass, replace
from typing import Callable, Optional
import re
from functools import reduce
from operator import mul
from collections import defaultdict

@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    @property
    def total(self) -> int:
        return self.x + self.m + self.a + self.s


@dataclass
class Range:
    # inclusive - exclusive
    x: tuple[int,int] = (1, 4001)
    m: tuple[int,int] = (1, 4001)
    a: tuple[int,int] = (1, 4001)
    s: tuple[int,int] = (1, 4001)

    @property
    def size(self):
        return reduce(
            mul,
            [r[1] - r[0] for r in (self.x, self.m, self.a, self.s)]
        )

    def __str__(self) -> str:
        return ";".join((str(r) for r in (self.x, self.m, self.a, self.s)))

@dataclass
class Rule:
    rule: Callable[[Part], bool]
    target: str
    var: str
    op: str
    val: int

    def matches(self, part: Part) -> bool:
        return self.rule(part)
    
    def __str__(self) -> str:
        return f"{self.var}{self.op}{self.val}:{self.target}"
    
    def split_range(self, r: Range) -> tuple[Optional[Range], Optional[Range]]:
        """ Take a range and split it in two, the range which matches the condition and the rest.
        If the entire range matches (or doesn't match), None is used to denote the empty range for the rest."""
        rmin, rmax = getattr(r, self.var)
        if self.op == '<':
            # return [rmin, val[ and [val, rmax[ if rmin < val < rmax
            # else return None, [rmin, rmax[
            if rmin < self.val < rmax:
                rtrue = replace(r)
                setattr(rtrue, self.var, (rmin, self.val))
                rfalse = replace(r)
                setattr(rfalse, self.var, (self.val, rmax))
                return rtrue, rfalse
            elif self.val <= rmin:
                return None, r
            elif self.val >= rmax:
                return r, None
            else:
                print("You made a boo-boo in your logic")
        elif self.op == '>':
            # return [val+1, rmax[ and [rmin, val+1[ if rmin < val+1 < rmax
            if rmin < self.val + 1 < rmax:
                rfalse = replace(r)
                setattr(rfalse, self.var, (rmin, self.val + 1))
                rtrue = replace(r)
                setattr(rtrue, self.var, (self.val + 1, rmax))
                return rtrue, rfalse
            elif  rmin > self.val:
                return r, None
            elif rmax < self.val :
                return None, r
            else:
                print("You made a boo-boo in your logic")

@dataclass
class Workflow:
    name: str
    rules: list[Rule]
    default: str

    def apply(self, part: Part) -> str:
        for rule in self.rules:
            if rule.matches(part):
                return rule.target
        return self.default
    
    def __str__(self) -> str:
        return self.name + ":" + ";".join((str(r) for r in self.rules)) + ";" + self.default
    
    def apply_range(self, range: Range) -> dict[str, list[Range]]:
        # print(f"Applying WF {self.__str__()} to {range}")
        res = defaultdict(list)
        for rule in self.rules:
            rtrue, rfalse = rule.split_range(range)
            if rtrue:
                res[rule.target].append(rtrue)
            range = rfalse
            if not range:
                break
        if range:
            res[self.default].append(range)
        # print("Result:", res)
        return res
    

def parse_rule(rule: str) -> Rule:
    pattern = r'(\w)(.)(\d+):(\w+)'
    match = re.match(pattern, rule)

    if match:
        var = match.group(1)
        op = match.group(2)
        val = int(match.group(3))
        target = match.group(4)
        if op == '>':
            rule = lambda part: getattr(part, var) > val
        elif op == '<':
            rule = lambda part: getattr(part, var) < val
        else:
            print("Invalid operator", op)
        return Rule(rule, target, var, op, val)
    else:
        print("Invalid rule", rule)


def parse_workflow(workflow: str) -> Workflow:
    pattern = r'(\w+){(.+),(\w+)}'
    match = re.match(pattern, workflow)
    if match:
        name = match.group(1)
        rules = [parse_rule(rule) for rule in match.group(2).split(',')]
        default = match.group(3)
        return Workflow(name, rules, default)
    else:
        print("Invalid workflow", workflow)


def parse_part(part: str) -> Part:
    pattern = r'{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}'
    match = re.match(pattern, part)
    if match:
        return Part(int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4)))
    else:
        print("Invalid part", part)


def apply_workflows(workflows: dict[str, Workflow], part: Part) -> str:
    wf = workflows["in"]
    out = wf.apply(part)
    while out not in ('A', 'R'):
        wf = workflows[out]
        out = wf.apply(part)
    return out

def apply_workflow_range(workflows: dict[str, Workflow], wf: str, range: Range) -> list[Range]:
    """ For a given range and workflow, return all sub-ranges which lead to acceptance """
    workflow_res = workflows[wf].apply_range(range)
    res = []
    
    for next_wf, next_ranges in workflow_res.items():
        for next_range in next_ranges:
            print(f"From {wf} to {next_wf}: {next_range.size}")
            if next_wf == 'A':
                res.append(next_range)
            elif next_wf == 'R':
                continue
            else:
                res.extend(apply_workflow_range(workflows, next_wf, next_range))
    return res


def part1(example: bool = False):
    wf_lines, parts = split_by_empty_line(get_input(19, example))
    workflows = {}
    for wf in wf_lines:
        workflow = parse_workflow(wf)
        workflows[workflow.name] = workflow
    parts = [parse_part(part) for part in parts]
    res = 0
    for part in parts:
        out = apply_workflows(workflows, part)
        if out == 'A':
            res += part.total
    return res

def part2(example: bool = False):
    wf_lines, _ = split_by_empty_line(get_input(19, example))
    workflows = {}
    for wf in wf_lines:
        workflow = parse_workflow(wf)
        workflows[workflow.name] = workflow
    all_ranges = apply_workflow_range(workflows, "in", Range())
    return sum([r.size for r in all_ranges])

if __name__ == "__main__":
    print("Solution to part 1:", part1(False))
    print("Solution to part 2:", part2(False))