LEFT_ONE = (-1, 0)
LEFT_TWO = (-2, 0)
LEFT_THREE = (-3, 0)

RIGHT_ONE = (1, 0)
RIGHT_TWO = (2, 0)
RIGHT_THREE = (3, 0)

UP_ONE = (0, 1)
UP_TWO = (0, 2)
UP_THREE = (0, 3)

DOWN_ONE = (0, -1)
DOWN_TWO = (0, -2)
DOWN_THREE = (0, -3)

VALID_MOVES = [LEFT_ONE, LEFT_TWO, LEFT_THREE,
               RIGHT_ONE, RIGHT_TWO, RIGHT_THREE,
               UP_ONE, UP_TWO, UP_THREE,
               DOWN_ONE, DOWN_TWO, DOWN_THREE]


def read_lines_of_file(file: str, splitter: str = '\n') -> list[str]:
    """
    Reads the lines of the provided file and returns a tuple.
    """
    return open(file).read().split(splitter)


def part_one(lines: list[str]) -> int:
    start = (0, 0)
    goal = (len(lines[0]) - 1, len(lines) - 1)

    print(f"Starting at {start}")
    print(f"Pathing to {goal}")

    # let's use A* with a heuristic of the heat loss factor to pathfind,
    #  making sure to never go three nodes in a straight direction


if __name__ == '__main__':
    lines = read_lines_of_file("text.txt")
    example_lines = read_lines_of_file("example_text.txt")
    print(f"Part one example: {part_one(example_lines)}")
