from dataclasses import dataclass
import re
from utils import get_input

@dataclass
class Range:
    start: int
    end: int

    @property
    def length(self) -> int:
        return self.end - self.start

    def in_range(self, value: int) -> bool:
        return self.start <= value < self.end

@dataclass
class Mapping:
    destination: int
    source: int
    length: int

    def in_range(self, value: int) -> bool:
        return self.source <= value < self.source + self.length
    
    @property
    def range_end(self) -> int:
        return self.source + self.length
    
    def in_range_back(self, value: int) -> bool:
        return self.destination <= value < self.destination + self.length
    
    def translate(self, value: int) -> int:
        return value - self.source + self.destination
    
    def translate_back(self, value: int) -> int:
        return value - self.destination + self.source
    
    def __str__(self) -> str:
        return f"{self.destination} {self.source} {self.length}"
    
@dataclass
class Map:
    source: str
    destination: str
    mappings: list[Mapping]

    def sort(self):
        self.mappings.sort(key=lambda x: x.source)

    def translate(self, value: int) -> int:
        for mapping in self.mappings:
            if mapping.in_range(value):
                result = mapping.translate(value)
                return result
        return value
    
    def translate_back(self, value: int) -> int:
        for mapping in self.mappings:
            if mapping.in_range_back(value):
                result = mapping.translate_back(value)
                return result
        return value

    def translate_range(self, range: Range) -> list[Range]:
        self.sort()
        rs = range.start
        re = range.end
        new_ranges = []
        for mapping in self.mappings:
            ms = mapping.source
            me = mapping.range_end
            if re <= ms:
                # range ends before the mapping starts, return the range as is
                return [range]
            if me <= rs:
                continue
            inter_start = max(rs, ms)
            inter_end = min(re, me)
            if  rs < ms:
                # range starts before the mapping, return the first slice as is
                new_ranges.append(Range(rs, ms))
            # at this point we know that the range and the mapping overlap
            new_ranges.append(Range(inter_start, inter_end))
            if re > me:
                leftover = Range(me, re)
                return new_ranges + self.translate_range(leftover)
            else:
                return new_ranges
        print("No mapping found for range", range)
        return [range]

def parse_seeds(line: str) -> list[int]:
    seed_list = line.split(': ')[1].split()
    return list(map(int, seed_list))

def parse_seeds_part2(line: str) -> list[Range]:
    s = parse_seeds(line)
    return [Range(s[i], s[i] + s[i+1]) for i in range(0, len(s), 2)]


def parse_mapping(line: str) -> Mapping:
    destination, source, length = map(int, line.split())
    return Mapping(destination, source, length)

def parse_map_header(line: str) -> tuple[str, str]:
    match = re.match(r'(\w+)-to-(\w+).*', line)
    if match:
        source = match.group(1)
        destination = match.group(2)
    else:
        print(f"Invalid line format: {line}")
    return source, destination

def parse_input(lines : list[str]) -> tuple[list[int], dict[str, Map]]:
    seeds = parse_seeds(lines[0])
    maps = {}
    new_map = True
    for line in lines[2:]:
        if new_map:
            source, destination = parse_map_header(line)
            current_mappings = []
            new_map = False
        elif line == "":
            maps[source] = Map(source, destination, current_mappings)
            maps[source].sort()
            new_map = True
        else:
            current_mappings.append(parse_mapping(line))
        if current_mappings:
            maps[source] = Map(source, destination, current_mappings)
            maps[source].sort()
    return seeds, maps

def parse_input_part2(lines : list[str]) -> tuple[list[Range], dict[str, Map]]:
    seeds = parse_seeds_part2(lines[0])
    maps = {}
    new_map = True
    for line in lines[2:]:
        if new_map:
            source, destination = parse_map_header(line)
            current_mappings = []
            new_map = False
        elif line == "":
            maps[destination] = Map(source, destination, current_mappings)
            maps[destination].sort()
            new_map = True
        else:
            current_mappings.append(parse_mapping(line))
        if current_mappings:
            maps[destination] = Map(source, destination, current_mappings)
            maps[destination].sort()

    return seeds, maps

def walk_map(map, source, destination, value):
    # print("Walking map", source, destination, value)
    if source == destination:
        # print("Reached destination", value)
        return value
    else:
        return walk_map(map, map[source].destination, destination, map[source].translate(value))
    
def walk_map_back(map, destination, source, value):
    # print("Walking map", source, destination, value)
    if source == destination:
        # print("Reached destination", value)
        return value
    else:
        return walk_map_back(map, map[destination].source, source, map[destination].translate_back(value))

def day5_part1(example=False) -> None:
    content = get_input(5, example=example)
    seeds, maps = parse_input(content)
    locations = []
    for seed in seeds:
        locations.append(walk_map(maps, 'seed', 'location', seed))
    print(min(locations))

def check_candidate(seed_ranges: list[Range], maps, candidate: int) -> bool:
    seed_value = walk_map_back(maps, 'location', 'seed', candidate)
    for seed_range in seed_ranges:
        if seed_range.in_range(seed_value):
            return True
    return False

def day5_part2(example=False) -> None:
    content = get_input(5, example=example)
    # seed_ranges, maps = parse_input_part2(content)
    # find_naive(maps, seed_ranges) -> 50855035
    s, maps = parse_input(content)
    seed_ranges = [Range(s[i], s[i+1]) for i in range(0, len(s), 2)]
    find_smart(maps, seed_ranges)


def walk_map_ranges(map, source, destination, ranges: list[Range]):
    # print("Walking map", source, destination, value)
    if source == destination:
        # print("Reached destination", value)
        return ranges
    else:
        new_ranges = []
        for range in ranges:
            new_ranges += map[source].translate_range(range)
        return walk_map_ranges(map, map[source].destination, destination, new_ranges)


def find_naive(maps, seed_ranges):
    candidate = 1
    while True:
        if check_candidate(seed_ranges, maps, candidate):
            print(candidate)
            break
        candidate += 1


def find_smart(maps, seed_ranges):
    ranges = walk_map_ranges(maps, 'seed', 'location', seed_ranges)
    print(min([range.start for range in ranges]))

if __name__ == "__main__":
    day5_part2(True)
    day5_part2()