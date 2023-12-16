def read_lines_of_file(file: str, splitter: str = '\n') -> list[str]:
    """
    Reads the lines of the provided file and returns a tuple.
    """
    return open(file).read().split(splitter)


def part_one(lines: list[str]) -> int:
    pass


def part_two(lines: list[str]) -> int:
    pass


if __name__ == '__main__':
    lines = read_lines_of_file("text.txt")

    print(f"Part one: {part_one(lines)}")
    print(f"Part one: {part_two(lines)}")
