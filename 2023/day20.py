from dataclasses import dataclass
from enum import Enum
from typing import Union
from collections import deque
from functools import reduce
from operator import mul

from utils import get_input

# Low pulse = 0, high pulse = 1

class ModuleType(Enum):
    FLIP_FLOP = 1
    CONJ = 2
    BROADCAST = 3
    UNTYPED = 4

class Module:
    type: ModuleType
    name: str
    destinations: list[str]

    def __init__(self, type, name, destinations):
        self.type = type
        self.name = name
        self.destinations = destinations
        if type == ModuleType.FLIP_FLOP:
            self.status = 0  # Flip Flop default to off
        elif type == ModuleType.CONJ:
            self.status  = {}  # We will add the incoming connections as they are defined

    def register_input(self, incoming: str) -> None:
        if self.type != ModuleType.CONJ:
            return  # only do something for conjunction modules
        self.status[incoming] = 0  # init defaults to low pulse

    def receive(self, sender, pulse) -> list[tuple[str, int]]:
        if self.type == ModuleType.BROADCAST:
            return [(self.name, dest, pulse) for dest in self.destinations]
        elif self.type == ModuleType.FLIP_FLOP:
            if pulse == 1:
                return []  # high pulse: do nothing
            else:
                # swith internal status
                self.status = 1 - self.status
                # is status is on (1), send a high pulse. Else send a low pulse
                return [(self.name, dest, self.status) for dest in self.destinations]
        elif self.type == ModuleType.CONJ:
            self.status[sender] = pulse
            if any((status == 0 for status in self.status.values())):
                return [(self.name, dest, 1) for dest in self.destinations]
            else:
                return [(self.name, dest, 0) for dest in self.destinations]
        elif self.type == ModuleType.UNTYPED:
            return []
        else:
            raise ValueError("Bad module type", self.type)
        
    def __str__(self):
        prefix = ""
        if self.type == ModuleType.FLIP_FLOP:
            prefix = "%"
        elif self.type == ModuleType.CONJ:
            prefix = "&"
        return f"{prefix}{self.name} -> {','.join(self.destinations)}"

def parse_module(line: str) -> Module:
    module, dest = line.split(' -> ')
    destinations = dest.split(', ')
    if module == 'broadcaster':
        return Module(ModuleType.BROADCAST, "broadcaster", destinations)
    elif module.startswith('&'):
        return Module(ModuleType.CONJ, module[1:], destinations)
    elif module.startswith('%'):
        return Module(ModuleType.FLIP_FLOP, module[1:], destinations)
    else:
        raise ValueError(line)


def build_modules(input: list[str]) -> dict[str, Module]:
    modules: dict[str, Module] = {}
    for line in input:
        module = parse_module(line)
        modules[module.name] = module
    # register inputs once all modules have been created
    # Use a copy of the dict to iterate as we may add modules in flight
    for name, module in modules.copy().items():
        for dest in module.destinations:
            if dest not in modules:
                # add untyped modules
                modules[dest] = Module(ModuleType.UNTYPED, dest, [])
            modules[dest].register_input(name)
    return modules

def push_button(modules: dict[str, Module], watched = {}, idx=0, part1=True) -> list[int,int]:
    """ Push the button and return a count low/high pulses """
    count = [0, 0]
    # initiate the deque with the button pulse
    pulses = deque()
    pulses.append(("button", "broadcaster", 0))
    res_part2 = None
    while len(pulses) > 0:
        signal = pulses.popleft()
        # print("Handling", signal)
        sender, dest, pulse = signal
        if sender in watched.copy() and watched[sender] != pulse:
            print(idx, sender)
            res_part2 = idx
            watched.pop(sender)
        # count the pulse
        count[pulse] += 1
        # send the pulse to the module and append the new pulses to the end of the deque
        pulses.extend(modules[dest].receive(sender, pulse))
    return count if part1 else res_part2


def part1(example=False):
    modules = build_modules(get_input(20, example))
    low, high = 0, 0
    for _ in range(1000):
        new_low, new_high = push_button(modules)
        low += new_low
        high += new_high
    print(low, high, high*low)

def part2(example=False):
    modules = build_modules(get_input(20, example))
    to_watch = modules['lx'].status.keys()
    print(to_watch)
    watched = {m: 0 for m in to_watch}
    frequencies = []
    for i in range(10**5):
        res = push_button(modules, watched, i + 1, part1=False)
        if res: 
            frequencies.append(res)
        if len(watched) == 0:
            break
    print(frequencies)
    print(reduce(mul, frequencies))


if __name__ == '__main__':
    part1(False)
    part2(False)
