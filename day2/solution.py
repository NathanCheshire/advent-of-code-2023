import re

MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14

DEBUG_MODE = True


def extract_game_and_id_from_line(string: str) -> tuple[int, str]:
    """
    Extracts a game from a line, example:

    Providing:
    Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green

    Would return:
    {1, "3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"}

    """
    match = re.match(r"Game (\d+): (.+)", string)
    if match:
        game_id = int(match.group(1))
        game_data = match.group(2)
        return game_id, game_data
    return None


def extract_subsets_from_game(string: str) -> list[str]:
    """
    Extracts the subsets from the game line, example:

    Providing: 
    3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green

    Would return:
    ["3 blue, 4 red", "1 red, 2 green", 6 blue", "2 green"]
    """
    return string.split('; ')


class GameSet:
    """
    An encapsulating class for a game set object.
    """

    def __init__(self, number, color):
        self.number = number
        self.color = color

    def __str__(self):
        return f"GameSet(number={self.number}, color={self.color})"


def extract_cube_sets_from_subset(string: str) -> list[GameSet]:
    """
    Extracts the cube sets from the subset, example:

    Providing:
    3 blue, 4 red

    Would return:

    """
    subsets = re.findall(r"(\d+) (\w+)", string)
    return [GameSet(int(number), color) for number, color in subsets]


def read_lines_of_file(file) -> list[str]:
    """
    Reads the lines of the provided file and returns a tuple.
    """
    return open(file).read().split('\n')


def debug(string: str) -> None:
    if DEBUG_MODE:
        print(string)


def part_one():
    lines = read_lines_of_file("./text.txt")
    debug(f"Lines length: {len(lines)}")

    game_ids_sum = 0
    for line in lines:
        id, game = extract_game_and_id_from_line(line)
        debug(f"Id: {id}, game: {game}")
        subsets = extract_subsets_from_game(game)

        game_possible = True
        for subset in subsets:
            cube_sets = extract_cube_sets_from_subset(subset)
            for cube_set in cube_sets:
                if cube_set.color == "blue" and cube_set.number > MAX_BLUE:
                    game_possible = False
                    debug("Game not possible, blues out of range")
                elif cube_set.color == "green" and cube_set.number > MAX_GREEN:
                    game_possible = False
                    debug("Game not possible, greens out of range")
                elif cube_set.color == 'red' and cube_set.number > MAX_RED:
                    game_possible = False
                    debug("Game not possible, reds out of range")

        if game_possible:
            game_ids_sum = game_ids_sum + id

    print(f"Game ids sum: {game_ids_sum}")


def part_two():
    lines = read_lines_of_file("./text.txt")
    debug(f"Lines length: {len(lines)}")

    power_sum = 0
    for line in lines:
        id, game = extract_game_and_id_from_line(line)
        debug(f"Id: {id}, game: {game}")
        subsets = extract_subsets_from_game(game)

        max_blues = 0
        max_greens = 0
        max_red = 0

        for subset in subsets:
            cube_sets = extract_cube_sets_from_subset(subset)
            for cube_set in cube_sets:
                if cube_set.color == "blue":
                    max_blues = max(max_blues, cube_set.number)
                    debug(f"New max blues: {max_blues}")
                elif cube_set.color == "green":
                    max_greens = max(max_greens, cube_set.number)
                    debug(f"New max greens: {max_greens}")
                elif cube_set.color == 'red':
                    max_red = max(max_red, cube_set.number)
                    debug(f"New max reds: {max_red}")

        power = max_blues * max_greens * max_red
        debug(f"Current power: {power}")
        power_sum = power_sum + power

    print(f"Power sum: {power_sum}")


if __name__ == '__main__':
    part_one()
    part_two()
