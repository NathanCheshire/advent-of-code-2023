import math

DIRECTIONS = {
    '0': (1, 0),
    'R': (1, 0),
    '1': (0, 1),
    'D': (0, 1),
    '2': (-1, 0),
    'L': (-1, 0),
    '3': (0, -1),
    'U': (0, -1)
}


def add_points(point: tuple[int, int], other_point: tuple[int, int]) -> tuple[int, int]:
    return point[0] + other_point[0], point[1] + other_point[1]


def scale_point(point: tuple[int, int], multiplier: int) -> tuple[int, int]:
    return point[0] * multiplier, point[1] * multiplier


def get_directional_tuple(direction: str) -> tuple[int, int]:
    return DIRECTIONS.get(direction, (0, 0))


def read_lines_of_file(file: str, splitter: str = '\n') -> list[str]:
    """
    Reads the lines of the provided file and returns a tuple.
    """
    return open(file).read().split(splitter)


def parse_lines(lines: list[str]) -> list[tuple[str, int, str]]:
    """
    Parses the lines of a file for this day.
    Returns a list of tuples containing direction, distance, and hex color code.
    """
    ret = []

    for line in lines:
        direction, distance, hex = line.split()
        direction = direction[0]
        distance = int(distance)
        hex = hex.strip('()')

        ret.append((direction, distance, hex))

    return ret


def corner_positions(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    current_point = (0, 0)
    corners = [current_point]

    for point in points:
        current_point = add_points(current_point, point)
        corners.append(current_point)

    return corners


def perimeter(points: list[tuple[int, int]]) -> int:
    return sum(abs(point[0]) + abs(point[1]) for point in points)


def showlace_area(corners: list[tuple[int, int]]) -> int:
    sum = 0

    for current_point, last_point in zip(corners, corners[1:] + corners[:1]):
        sum += current_point[0] * last_point[1] - \
            current_point[1] * last_point[0]

    return math.floor(abs(sum) / 2)


def polygon_capacity(points: list[tuple[int, int]]) -> int:
    showlace = showlace_area(corner_positions(points))
    return showlace + math.floor(perimeter(points) / 2) + 1


def part_one(lines: list[str]) -> int:
    inputs = parse_lines(lines)

    points = []
    for direction, scalar, _ in inputs:
        direction = get_directional_tuple(direction)
        points.append(scale_point(direction, scalar))

    return polygon_capacity(points)


def part_two(lines: list[str]) -> int:
    inputs = parse_lines(lines)

    points = []
    for _, _, color in inputs:
        direction = get_directional_tuple(color[-1])
        distance = int(color[1:-1], 16)

        points.append(scale_point(direction, distance))

    return polygon_capacity(points)


if __name__ == '__main__':
    lines = read_lines_of_file("text.txt")
    example_lines = read_lines_of_file("example.txt")

    print(f"Part one example: {part_one(example_lines)}")
    print(f"Part one: {part_one(lines)}")

    print(f"Part two example: {part_two(example_lines)}")
    print(f"Part two: {part_two(lines)}")
