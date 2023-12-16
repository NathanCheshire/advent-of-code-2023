

def read_lines_of_file(file) -> list[str]:
    """
    Reads the lines of the provided file and returns a tuple.
    """
    return open(file).read().split('\n')


def is_start(char: str) -> bool:
    return char == 'S'


def connects_down(char: str) -> bool:
    return char in ['F', '7', '|']


def connects_up(char: str) -> bool:
    return char in ['L', 'J', '|']


def connects_vertically(char: str) -> bool:
    return connects_up(char) and connects_down(char)


def connects_left(char: str) -> bool:
    return char in ['7', 'J', '-']


def connects_right(char: str) -> bool:
    return char in ['F', 'L', '-']


def connects_horizontally(char: str) -> bool:
    return connects_left(char) and connects_right(char)


def part_one(lines: list[str]) -> int:
    pass


def part_two(lines: list[str]) -> int:
    pass


if __name__ == '__main__':
    lines = read_lines_of_file("text.txt")
    print(f"Part one: {part_one(lines)}")
    print(f"Part one: {part_two(lines)}")
