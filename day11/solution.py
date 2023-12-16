GALAXY = "#"
SPACE = '.'


def read_lines_of_file(file) -> list[str]:
    """
    Reads the lines of the provided file and returns a tuple.
    """
    return open(file).read().split('\n')


def expand_universe(lines: list[str]) -> list[str]:
    rows_with_galaxies = set()
    cols_with_galaxies = set()

    for index, line in enumerate(lines):
        for col_index, char in enumerate(line):
            if char == GALAXY:
                rows_with_galaxies.add(index)
                cols_with_galaxies.add(col_index)

    new_lines = []

    for index, line in enumerate(lines):
        new_line = ''

        for col_index, char in enumerate(line):
            new_line += char

            if col_index not in cols_with_galaxies:
                new_line += SPACE

        new_lines.append(new_line)

        if index not in rows_with_galaxies:
            new_lines.append(new_line)

    return new_lines


def get_galaxies(grid: list[str]) -> list[tuple[int, int]]:
    galaxies = []

    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == GALAXY:
                galaxies.append((x, y))

    return galaxies


def manhattan_distance(node1: tuple[int], node2: tuple[int]) -> int:
    x1, y1 = node1
    x2, y2 = node2

    return abs(y1 - y2) + abs(x1 - x2)


def sum_manhattan(nodes) -> int:
    total_distance = 0
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            total_distance += manhattan_distance(nodes[i], nodes[j])

    return total_distance


def part_one(lines: list[str]) -> int:
    nodes = get_galaxies(lines)
    return sum_manhattan(nodes)


def sum_distances(distances: list[int]) -> int:
    """
    Calculate the sum of distances between pairs of points.
    """
    total_distance = 0
    num_distances = len(distances)

    for i in range(num_distances - 1):
        deviation = distances[i + 1] - distances[i]
        multiplier = (i + 1) * (num_distances - (i + 1))
        total_distance += multiplier * deviation

    return total_distance


def find_empty_lines(lines: list[str]) -> list[int]:
    return [index for index, line in enumerate(lines) if GALAXY not in line]


def adjust_galaxy_positions(lines: list[str], empty_lines: list[int]) -> list[int]:
    """
    Inserts empty space where necessary due to the expanding universe.
    """
    adjusted_positions = []

    for y, line in enumerate(lines):
        for char in line:
            if char == GALAXY:
                adjustment = 999999 * \
                    sum(1 for empty_line in empty_lines if empty_line < y)
                adjusted_positions.append(y + adjustment)

    return adjusted_positions


def transpose_grid(grid: list[str]) -> list[str]:
    """
    Transposes the grid meaning rows will now be columns.
    """
    return [''.join(row) for row in zip(*grid)]


def part_two(lines: list[str]) -> int:
    total_distance = 0
    for _ in range(2):  # Two iterations: one for rows, one for columns after transposing
        empty_lines = find_empty_lines(lines)
        adjusted_positions = adjust_galaxy_positions(
            lines, empty_lines)
        total_distance += sum_distances(adjusted_positions)
        lines = transpose_grid(lines)
    return total_distance


if __name__ == '__main__':
    lines = read_lines_of_file('text.txt')
    lines = expand_universe(lines)

    print(f"Part one: {part_one(lines)}")
    print(f"Part two: {part_two(lines)}")
