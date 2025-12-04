from utils import read_input, pad_board

def adjacent(i: int, j: int) -> list[tuple[int, int]]:
    return [(i-1, j-1), (i-1, j), (i-1, j+1), 
            (i, j-1), (i, j+1),
            (i+1, j-1), (i+1, j), (i+1, j+1)]


def list_removable(board: list[list[str]]) -> list[tuple[int, int]]:
    result = []
    width = len(board[0])
    height = len(board)
    for y in range(1, height-1):
        for x in range(1, width-1):
            if board[y][x] == '@':
                # count adjacent '@'
                count = sum(1 for (i, j) in adjacent(y, x) if board[i][j] == '@')
                if count < 4:
                    result.append((y, x))
    return result



def part1() -> int:
    lines = read_input(day=4)
    board = [list(line) for line in lines]
    padded_board = pad_board(board, pad_char='.')
    return len(list_removable(padded_board))
    
    
def part2() -> int:
    lines = read_input(day=4)
    board = [list(line) for line in lines]
    padded_board = pad_board(board, pad_char='.')
    removable = list_removable(padded_board)
    result = len(removable)
    while len(removable) > 0:
        for (i, j) in removable:
            padded_board[i][j] = '.'
        removable = list_removable(padded_board)
        result += len(removable)
    # count remaining '@'
    return result

if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())