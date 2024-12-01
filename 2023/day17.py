from utils import Direction, to_int_board, get_input
import heapq


def day17(min_dist, max_dist, example=False):
    xmax, ymax, grid = to_int_board(get_input(17, example))
    def is_in_board(x, y):
        return 0 <= x < xmax and 0 <= y < ymax
    heap = [(0, 0, 0, Direction.DOWN), (0, 0, 0, Direction.RIGHT)]
    heapq.heapify(heap)
    seen = {}
    while heap:
        dist, x, y, dir = heapq.heappop(heap)
        # print(f"Dist: {dist}, x: {x}, y: {y}, dir: {dir}")
        if (x, y, dir) in seen:
            assert seen[(x, y, dir)] <= dist
            continue
        seen[(x, y, dir)] = dist
        for d in dir.perpendicular():
            new_x, new_y, new_dist = x, y, dist
            for i in range(max_dist):
                new_x, new_y = d.apply(new_x, new_y)
                if not is_in_board(new_x, new_y):
                    break
                new_dist += grid[new_y][new_x]
                if i >= min_dist - 1:
                    heapq.heappush(heap, (new_dist, new_x, new_y, d))
    # print(seen)
    return min(seen[(xmax-1, ymax-1, d)] for d in (Direction.DOWN, Direction.RIGHT))

if __name__ == "__main__":
    print(day17(1, 3, False))
    print(day17(4, 10, False))
                