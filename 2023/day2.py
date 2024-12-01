from dataclasses import dataclass

from utils import get_input

@dataclass
class Draw:
    red: int = 0
    green: int = 0
    blue: int = 0

    @staticmethod
    def from_string(draw: str) -> "Draw":
        items = draw.split(", ")
        r, g, b = 0, 0, 0
        for item in items:
            first, second = item.split(" ")
            if second == "red":
                r = int(first)
            elif second == "green":
                g = int(first)
            elif second == "blue":
                b = int(first)
            else:
                raise ValueError(f"Unknown color: {second}")
        return Draw(r, g, b)

@dataclass
class Game:
    id: int
    draws: list[Draw]

    @staticmethod
    def from_string(line: str) -> "Game":
        first, second = line.split(": ")
        id = int(first.split(" ")[1])
        raw_draws = second.split("; ")
        return Game(id, [Draw.from_string(draw) for draw in raw_draws])
    

def parse_input() -> list[Game]:
    content = get_input(2)
    return [Game.from_string(line) for line in content]

def max_cubes(game: Game) -> Draw:
    max_red, max_green, max_blue = 0, 0, 0
    for draw in game.draws:
        max_red = max(draw.red, max_red)
        max_green = max(draw.green, max_green)
        max_blue = max(draw.blue, max_blue)
    return Draw(max_red, max_green, max_blue)


def day2_part1() -> int:
    games = parse_input()
    possible_games = []
    for game in games:
        max_draw = max_cubes(game)
        if max_draw.red <= 12 and max_draw.green <= 13 and max_draw.blue <= 14:
            possible_games.append(game.id)
    return sum(possible_games)

def day2_part2() -> int:
    games = parse_input()
    powers = []
    for game in games:
        max_draw = max_cubes(game)
        powers.append(max_draw.red * max_draw.green * max_draw.blue)
    return sum(powers)

if __name__ == "__main__":
    print(day2_part1())
    print(day2_part2())