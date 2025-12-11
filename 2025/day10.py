# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pulp",
# ]
# ///

from collections import deque

from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus, LpInteger, value

from utils import read_input


def toggle_lights(target:str, transitions=list[tuple[int]]) -> int:
    """ Starting from the off state, build a graph of all accessible light states using the transition list.
        Return the minimum number of transitions to reach the target. """

    num_lights = len(target)
    start_node = "." * num_lights

    # Keep track of nodes we've already reached. Store state as a str to allow for hashing and easy omparison
    seen: dict[str, int] = {start_node: 0}

    # Use deque for efficient breadth-first search.
    # Pop left to get the shallowest nodes, append right with the new, deeper nodes 
    to_visit = deque([(start_node, 0)])

    while target not in seen:
        current_node, current_dist = to_visit.popleft()
        for transition in transitions:
            dest_chars = [c for c in current_node]
            for light in transition:
                dest_chars[light] = '.' if current_node[light] == '#' else '#'
            dest = "".join(dest_chars)
            if dest not in seen:
                seen[dest] = current_dist + 1
                to_visit.append((dest, current_dist + 1))
    return seen[target]


def reach_joltage_bfs(target: list[int], increments=list[tuple[int]]) ->int:
    """ Similar than toggle_lights, except the number of reachable states is potentially infinite. 
        MUCH too slow for part 2. """

    num_lights = len(target)
    # Store nodes as tuples of int, representing current joltage for each button (tuple for hashability)
    start_state = tuple([0]*len(target))

    seen: dict[tuple[int], int] = {start_state: 0}
    to_visit = deque([(start_state, 0)])

    target_tuple = tuple(target)
    print(f"Target is {target_tuple}")
    def over_target(state: list[int]):
        return any((si > ti for si, ti in zip(state, target)))

    while target_tuple not in seen:
        current_state, current_dist = to_visit.popleft()
        for increment in increments:
            dest_state = list(current_state)
            for jolt in increment:
                dest_state[jolt] += 1
            dest_tuple = tuple(dest_state)
            if dest_tuple not in seen and not over_target(dest_state):
                print(f"Adding {dest_tuple} ({current_dist + 1}")
                seen[dest_tuple] = current_dist + 1
                to_visit.append((dest_tuple, current_dist + 1))
    return seen[target_tuple]


def reach_joltage_lp(target: list[int], increments=list[tuple[int]]) ->int:
    """ Use linear programming to minimize the number of increments needed to reach the target joltage. """

    prob = LpProblem("Joltage_Problem", LpMinimize)

    # Create variables for each increment, representing how many times to apply it
    increment_vars = [LpVariable(f"inc_{i}", lowBound=0, cat=LpInteger) for i in range(len(increments))]

    # Objective: minimize the total number of increments used
    prob += lpSum(increment_vars)

    # Constraints: for each button, the total increase from increments must equal the target joltage
    num_buttons = len(target)
    for button_idx in range(num_buttons):
        prob += (lpSum(increment_vars[i] * increments[i].count(button_idx) for i in range(len(increments))) == target[button_idx],
                 f"Button_{button_idx}_Target")

    # Solve the problem
    prob.solve()

    if LpStatus[prob.status] != 'Optimal':
        raise ValueError("No optimal solution found.")

    # Return the total number of increments used
    total_increments = int(value(prob.objective))
    return total_increments


def tuple_of_str(input: str) -> tuple[int]:
    nums = input[1:-1].split(',')
    return tuple([int(num) for num in nums])

def main():
    machines = read_input(day=10)
    result_part_1 = 0
    result_part_2 = 0
    for machine in machines:
        tokens = machine.split()
        target, *instructions, joltage = tokens
        parsed_instructions = [tuple_of_str(inst) for inst in instructions]
        result_part_1 += toggle_lights(target[1:-1], parsed_instructions)
        result_part_2 += reach_joltage_lp(tuple_of_str(joltage), parsed_instructions)
        print(f"Done with {machine}")
    return result_part_1, result_part_2





if __name__ == '__main__':
    part1, part2 = main()
    print("Part 1,", part1)
    print("Part 2", part2)
