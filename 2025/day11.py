from collections import defaultdict, deque
from functools import lru_cache

from utils import read_input




def main():
    raw_lines = read_input(day=11)
    successors = defaultdict(list)
    predecessors = defaultdict(list)
    for line in raw_lines:
        src, dest_str = line.split(": ")
        dest = dest_str.split(" ")
        successors[src].extend(dest)
        for d in dest:
            predecessors[d].append(src)

    @lru_cache(maxsize=None)
    def count_paths(start: str, node: str) -> tuple[int]:
        """ count number of paths from start to node 
            with and without going through "dac" and "fft" 
            
            Returns: (without_dac_fft, with_dac, with_fft, with_both)
            """
        if node == start:
            # TODO: not correct if start is "dac" or "fft" (not the case in input)
            return (1, 0, 0, 0)
        total = [0, 0, 0, 0]
        
        for pred in predecessors[node]:
            pred_counts = count_paths(start, pred)
            if node == "dac":
                assert pred_counts[1] == 0 and pred_counts[3] == 0
                total[1] += pred_counts[0]
                total[3] += pred_counts[2]
            elif node == "fft":
                assert pred_counts[2] == 0 and pred_counts[3] == 0
                total[2] += pred_counts[0]
                total[3] += pred_counts[1]
            else:
                for i in range(4):
                    total[i] += pred_counts[i]
            
        return tuple(total)

    # Part 1
    print("Part 1", sum(count_paths("you", "out")))

    # Part 2
    print("Part 2", count_paths("svr", "out")[3])
    

if __name__ == '__main__':
    main()