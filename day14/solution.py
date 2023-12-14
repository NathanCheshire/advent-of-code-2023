ROLLING_STONE = 'O'  # I can't get no
STABLE_STONE = '#'
EMPTY_SPACE = '.'
PART_TWO_CYCLES = 1000000000


def read_lines_of_file(file: str, splitter: str = '\n') -> list[str]:
    """
    Reads the lines of the provided file and returns a tuple.
    """
    return open(file).read().split(splitter)


def roll_rocks_north_step(lines: list[list[str]]) -> tuple[bool, list[list[str]]]:
    at_least_one_rock_rolled = False

    for line_index, line in enumerate(lines):
        last_line_index = line_index - 1

        if last_line_index >= 0:
            last_line = lines[last_line_index]

            for char_index, char in enumerate(line):
                if char == ROLLING_STONE and last_line[char_index] == EMPTY_SPACE:
                    line[char_index] = EMPTY_SPACE
                    last_line[char_index] = ROLLING_STONE

                    at_least_one_rock_rolled = True

    return at_least_one_rock_rolled, lines


def roll_rocks_north(lines: list[list[str]]) -> list[list[str]]:
    change_performed, stepped_north = roll_rocks_north_step(lines)
    while change_performed:
        change_performed, stepped_north = roll_rocks_north_step(
            stepped_north)

    return stepped_north


def compute_total_load(lines: list[list[str]]) -> int:
    load = 0

    for line_index, line in enumerate(lines):
        for place in line:
            if place == ROLLING_STONE:
                load += len(lines) - line_index

    return load


def transpose(lines: list[list[str]]) -> list[list[str]]:
    """
    Rotates the matrix to the right ninetry degrees. Code from stackoverflow.
    """
    num_rows = len(lines)
    num_cols = len(lines[0])

    transposed = [['' for _ in range(num_rows)] for _ in range(num_cols)]

    for i in range(num_rows):
        for j in range(num_cols):
            transposed[j][num_rows - 1 - i] = lines[i][j]

    return transposed


def spin_cycle(lines: list[list[str]]) -> list[list[str]]:
    """
    Computes a singular spin cycle that of tilting to the north, then west, then south, then east.
    Returns the new lines.
    """
    # roll rocks north
    rolled_north = roll_rocks_north(lines)

    # roll rocks west
    transposed = transpose(rolled_north)
    rolled_west = roll_rocks_north(transposed)

    # roll rocks south
    transposed = transpose(rolled_west)
    rolled_south = roll_rocks_north(transposed)

    # roll rocks east
    transposed = transpose(rolled_south)
    rolled_east = roll_rocks_north(transposed)

    return transpose(rolled_east)


def part_one(lines: list[list[str]]) -> int:
    return compute_total_load(roll_rocks_north(lines))


def part_two(lines: list[list[str]]) -> int:
    cycles = {0: (str(lines), compute_total_load(lines))}
    current_cycle = lines
    num_cycles = 0

    while True:
        current_cycle = spin_cycle(current_cycle)
        num_cycles += 1
        current_load = compute_total_load(current_cycle)

        if str(current_cycle) in (cycle_str for cycle_str, _ in cycles.values()):
            cycle_start = next(key for key, value in cycles.items()
                               if value[0] == str(current_cycle))

            cycle_length = num_cycles - cycle_start
            cycle_position = (PART_TWO_CYCLES - cycle_start) % cycle_length

            return cycles[(cycle_start + cycle_position) % num_cycles][1]

        cycles[num_cycles] = (str(current_cycle), current_load)


if __name__ == '__main__':
    lines = read_lines_of_file('text.txt')
    chared_lines = [list(line) for line in lines]

    print(f'Part one: {part_one(chared_lines)}')
    print(f'Part two: {part_two(chared_lines)}')
