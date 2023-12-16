from queue import Queue

LEFT = (-1, 0)
RIGHT = (1, 0)
DOWN = (0, -1)
UP = (0, 1)

CARDINAL_DIRECTIONS = [LEFT, RIGHT, DOWN, UP]

VALID_MOVES = {
    "|": [DOWN, UP],
    "-": [LEFT, RIGHT],
    "L": [DOWN, RIGHT],
    "J": [DOWN, LEFT],
    "7": [LEFT, UP],
    "F": [RIGHT, UP],
}


BOTTOM_LEFT = "L"
TOP_RIGHT = "7"


def read_lines_of_file(file) -> list[str]:
    """
    Reads the lines of the provided file and returns a tuple.
    """
    return open(file).read().split('\n')


def is_start(char: str) -> bool:
    return char == 'S'


def find_start_node(grid: list[str]) -> tuple[int, int]:
    for y_index, line in enumerate(grid):
        for x_index, char in enumerate(line):
            if is_start(char):
                return x_index, y_index


def get_grid_char(grid: list[str], x: int, y: int) -> str:
    return grid[y][x]


def get_distances_from_start(grid_path: Queue, grid: list[str]) -> dict[tuple[int, int], int]:
    distances_from_start = {(find_start_node(grid)): 0}

    while not grid_path.empty():
        current_distance, (x, y) = grid_path.get()
        current_grid_char = get_grid_char(lines, x, y)

        if (x, y) in distances_from_start:
            continue
        distances_from_start[(x, y)] = current_distance

        if current_grid_char == '|':
            grid_path.put((current_distance + 1, (x, y - 1)))
            grid_path.put((current_distance + 1, (x, y + 1)))
        elif current_grid_char == '-':
            grid_path.put((current_distance + 1, (x - 1, y)))
            grid_path.put((current_distance + 1, (x + 1, y)))
        elif current_grid_char == 'L':
            grid_path.put((current_distance + 1, (x, y - 1)))
            grid_path.put((current_distance + 1, (x + 1, y)))
        elif current_grid_char == 'J':
            grid_path.put((current_distance + 1, (x, y - 1)))
            grid_path.put((current_distance + 1, (x - 1, y)))
        elif current_grid_char == '7':
            grid_path.put((current_distance + 1, (x - 1, y)))
            grid_path.put((current_distance + 1, (x, y + 1)))
        elif current_grid_char == 'F':
            grid_path.put((current_distance + 1, (x + 1, y)))
            grid_path.put((current_distance + 1, (x, y + 1)))

    return distances_from_start


def get_max_distance_of_path(grid_path: Queue, grid: list[str]) -> int:
    return max(get_distances_from_start(grid_path, grid).values())


def get_grid_path(lines: list[str]):
    grid_path = Queue()

    start_x, start_y = find_start_node(lines)
    current_x, current_y = start_x, start_y

    for dx, dy in CARDINAL_DIRECTIONS:
        possible_next_x = current_x + dx
        possible_next_y = current_y + dy
        next_char = get_grid_char(lines, possible_next_x, possible_next_y)

        if next_char in VALID_MOVES.keys():
            for next_char_dx, next_char_dy in VALID_MOVES[next_char]:
                pathable_x = current_x - next_char_dx == possible_next_x
                pathable_y = current_y - next_char_dy == possible_next_y

                if pathable_x and pathable_y:
                    grid_path.put((1, (possible_next_x, possible_next_y)))

    return grid_path


def part_one(lines: list[str]) -> int:
    return get_max_distance_of_path(get_grid_path(lines), lines)


def part_two(lines: list[str]) -> int:
    grid_width = len(lines[0])
    grid_height = len(lines)

    path_nodes = get_distances_from_start(get_grid_path(lines), lines)

    nodes_inside_loop = 0
    for y_index, line in enumerate(lines):
        for x_index, char in enumerate(line):
            if (x_index, y_index) in path_nodes:
                continue

            times_crossed_path = 0
            current_sub_x, current_sub_y = x_index, y_index

            # probably not efficient but we're going to check the whole sub-square
            while current_sub_x < grid_width and current_sub_y < grid_height:
                current_sub_char = get_grid_char(
                    lines, current_sub_x, current_sub_y)

                current_node = (current_sub_x, current_sub_y)

                if current_node in path_nodes and current_sub_char != BOTTOM_LEFT and current_sub_char != TOP_RIGHT:
                    times_crossed_path += 1

                current_sub_x += 1
                current_sub_y += 1

            # this is a ray tracing technique, odd vs even dictates if a node is inside or outside a polygon
            if times_crossed_path % 2 == 1:
                nodes_inside_loop += 1

    return nodes_inside_loop


if __name__ == '__main__':
    lines = read_lines_of_file("text.txt")

    print(f"Part one: {part_one(lines)}")
    print(f"Part two: {part_two(lines)}")
