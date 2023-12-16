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


def part_one(lines: list[str]) -> int:
    beam_queue = Queue()

    # start at top left traveling right
    # x, y, dx, dy
    beam_queue.put((0, 0, 1, 0))

    seen_nodes = []

    while not beam_queue.empty():
        current_beam = beam_queue.get()

        current_x = current_beam[0]
        current_y = current_beam[1]
        delta_x = current_beam[2]
        delta_y = current_beam[3]

        # skip node if already processed
        if current_beam in seen_nodes:
            continue
        seen_nodes.append(current_beam)

        current_char = get_at_grid_position(lines, current_x, current_y)

        if is_empty_space(current_char):
            print('empty space', current_x, current_y, delta_x, delta_y)
            # position plus velocity for next
            next_x = current_x + delta_x
            next_y = current_y + delta_y

            x_valid = next_x < len(lines[0]) and next_x >= 0
            y_valid = next_y < len(lines) and next_y >= 0
            if x_valid and y_valid:
                beam_queue.put((next_x, next_y, delta_x, delta_y))
        elif is_mirror(current_char):
            left = current_x - 1
            right = current_x + 1
            top = current_y - 1
            bottom = current_y + 1

            if current_char == '/':
                print('/ mirror', current_x, current_y, delta_x, delta_y)
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
                print('\\ mirror', current_x, current_y, delta_x, delta_y)
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
                if delta_x in [-1, 1]:
                    print('splitter carrying straight -',
                          current_x, current_y, delta_x, delta_y)
                    next_x = current_x + delta_x
                    next_y = current_y + delta_y

                    x_valid = next_x < len(lines[0]) and next_x >= 0
                    y_valid = next_y < len(lines) and next_y >= 0
                    if x_valid and y_valid:
                        beam_queue.put((next_x, next_y, delta_x, delta_y))
                else:
                    print('splitter -', current_x, current_y, delta_x, delta_y)
                    left_x = current_x - 1
                    right_x = current_x + 1

                    if left_x >= 0:
                        beam_queue.put((left_x, current_y, -1, 0))
                    if right_x < len(lines[0]):
                        beam_queue.put((right_x, current_y, 1, 0))
            elif current_char == '|':
                if delta_y in [-1, 1]:
                    print('splitter carrying straight |',
                          current_x, current_y, delta_x, delta_y)
                    next_x = current_x + delta_x
                    next_y = current_y + delta_y

                    x_valid = next_x < len(lines[0]) and next_x >= 0
                    y_valid = next_y < len(lines) and next_y >= 0
                    if x_valid and y_valid:
                        beam_queue.put((next_x, next_y, delta_x, delta_y))
                else:
                    print('splitter |', current_x, current_y, delta_x, delta_y)
                    above_y = current_y - 1
                    below_y = current_y + 1

                    if above_y >= 0:
                        beam_queue.put((current_x, below_y, 0, -1))
                    if below_y < len(lines):
                        beam_queue.put((current_x, below_y, 0, 1))

    unique_seen_nodes = []
    for seen_node in seen_nodes:
        if (seen_node[0], seen_node[1]) not in unique_seen_nodes:
            unique_seen_nodes.append((seen_node[0], seen_node[1]))
    return len(unique_seen_nodes)


def part_two(lines: list[str]) -> int:
    pass


if __name__ == '__main__':
    example_lines = read_lines_of_file('example_text.txt')
    lines = read_lines_of_file('text.txt')

    print(f"Part one example: {part_one(example_lines)}")
    print(f"Part one: {part_one(lines)}")

    print(f"Part two example: {part_two(example_lines)}")
    # print(f"Part two: {part_two(lines)}")
