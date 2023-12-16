from queue import Queue


def read_lines_of_file(file: str, splitter: str = '\n') -> list[str]:
    """
    Reads the lines of the provided file and returns a tuple.
    """
    return open(file).read().split(splitter)


def is_mirror(char: str) -> bool:
    return char in ['/', '\\']


def is_empty_space(char: str) -> bool:
    return char == '.'


def is_splitter(char: str) -> bool:
    return char in ['|', '-']


def get_at_grid_position(grid: list[str], x: int, y: int) -> str:
    return grid[y][x]


def x_y_in_bounds(grid: list[str], x: int, y: int) -> bool:
    x_valid = x < len(grid[0]) and x >= 0
    y_valid = y < len(grid) and y >= 0
    return x_valid and y_valid


def count_energized_tiles(lines: list[str], starting_tile: tuple[int, int, int, int]) -> int:
    beam_queue = Queue()

    # x, y, dx, dy
    beam_queue.put(starting_tile)

    seen_nodes = []

    while not beam_queue.empty():
        current_beam = beam_queue.get()

        current_x, current_y, delta_x, delta_y = current_beam

        if current_beam in seen_nodes:
            continue
        seen_nodes.append(current_beam)

        current_char = get_at_grid_position(lines, current_x, current_y)

        if is_empty_space(current_char) or (current_char == '-' and delta_x in [-1, 1]) or (current_char == '|' and delta_y in [-1, 1]):
            next_x = current_x + delta_x
            next_y = current_y + delta_y

            if x_y_in_bounds(lines, next_x, next_y):
                beam_queue.put((next_x, next_y, delta_x, delta_y))
        elif is_mirror(current_char):
            left = current_x - 1
            right = current_x + 1
            top = current_y - 1
            bottom = current_y + 1

            if current_char == '/':
                # if coming from top, add left char, going left
                if delta_y == 1 and left >= 0:
                    beam_queue.put((left, current_y, -1, 0))
                # if coming from left, add top char, going up
                if delta_x == 1 and top >= 0:
                    beam_queue.put((current_x, top, 0, -1))
                # if coming from right, add bottom char, going down
                if delta_x == -1 and bottom < len(lines):
                    beam_queue.put((current_x, bottom, 0, 1))
                # if coming from bottom, add right char, going right
                if delta_y == -1 and right < len(lines[0]):
                    beam_queue.put((right, current_y, 1, 0))

            elif current_char == '\\':
                # if coming from top, add right char, going right
                if delta_y == 1 and right < len(lines[0]):
                    beam_queue.put((right, current_y, 1, 0))
                # if coming from right, add top char, going up
                if delta_x == -1 and top >= 0:
                    beam_queue.put((current_x, top, 0, -1))
                # if coming from left, add bottom char, going down
                if delta_x == 1 and bottom < len(lines):
                    beam_queue.put((current_x, bottom, 0, 1))
                # if coming from bottom, add left char, going left
                if delta_y == -1 and left >= 0:
                    beam_queue.put((left, current_y, -1, 0))

        elif is_splitter(current_char):
            if current_char == '-':
                left_x = current_x - 1
                right_x = current_x + 1

                if left_x >= 0:
                    beam_queue.put((left_x, current_y, -1, 0))
                if right_x < len(lines[0]):
                    beam_queue.put((right_x, current_y, 1, 0))
            elif current_char == '|':
                above_y = current_y - 1
                below_y = current_y + 1

                if above_y >= 0:
                    beam_queue.put((current_x, above_y, 0, -1))
                if below_y < len(lines):
                    beam_queue.put((current_x, below_y, 0, 1))

    unique_seen_nodes = []
    for seen_node in seen_nodes:
        if (seen_node[0], seen_node[1]) not in unique_seen_nodes:
            unique_seen_nodes.append((seen_node[0], seen_node[1]))
    return len(unique_seen_nodes)


def part_one(lines: list[str], example_lines: list[str]) -> None:
    top_left_moving_right = (0, 0, 1, 0)

    print(
        f"Part one example: {count_energized_tiles(example_lines, top_left_moving_right)}")
    print(f"Part one: {count_energized_tiles(lines, top_left_moving_right)}")


def compute_maximum_energeized_tiles(lines: list[str]) -> int:
    x_len = len(lines[0])
    y_len = len(lines)

    starting_tiles = []

    # top going downward
    for x in range(0, x_len):
        starting_tiles.append((x, 0, 0, 1))

    # bottom going upward
    for x in range(0, x_len):
        starting_tiles.append((x, y_len - 1, 0, -1))

    # Nathan comment: I actually got the right answer to my problem only generating
    # the top and bottom starting points, left and right were not computed but I still got 7831, the solution to my part 2

    # left going right
    for y in range(0, y_len):
        starting_tiles.append((0, y, 1, 0))

    # right going left
    for y in range(0, y_len):
        starting_tiles.append((x_len - 1, y, -1, 0))

    max_energized_tiles = 0
    for starting_tile in starting_tiles:
        max_energized_tiles = max(
            max_energized_tiles, count_energized_tiles(lines, starting_tile))
        pass

    return max_energized_tiles


def part_two(lines: list[str], example_lines: list[str]) -> None:
    print(
        f"Part two example: {compute_maximum_energeized_tiles(example_lines)}")
    print(f"Part two: {compute_maximum_energeized_tiles(lines)}")


if __name__ == '__main__':
    lines = read_lines_of_file('text.txt')
    example_lines = read_lines_of_file('example_text.txt')

    part_one(lines, example_lines)
    part_two(lines, example_lines)
