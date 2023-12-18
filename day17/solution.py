import heapq

CARDINAL_MOVES = [[-1, 0], [0, 1], [1, 0], [0, -1]]

PART_ONE_MAX_MOVES = 3
PART_TWO_MIN_MOVES = 4
PART_TWO_MAX_MOVES = 10


def read_lines_of_file(file: str, splitter: str = '\n') -> list[str]:
    """
    Reads the lines of the provided file and returns a tuple.
    """
    return open(file).read().split(splitter)


def part_one_valid_neighbor(_, __, consecutive_moves, ___):
    return consecutive_moves <= PART_ONE_MAX_MOVES


def part_two_valid_neighbor(current_direction: int, new_direction: int, new_consecutive_moves: int, consecutive_moves: int):
    return new_consecutive_moves <= PART_TWO_MAX_MOVES and (
        new_direction == current_direction or consecutive_moves >= PART_TWO_MIN_MOVES or consecutive_moves == -1)


def compute_minimal_heat_loss(valid_neighbor_function, grid: list[list[int]]):
    row_count = len(grid)
    column_count = len(grid[0])

    start_node = (0, 0, 0, -1, -1)
    queue = [start_node]

    distances = {}

    while queue:
        distance, x, y, direction, move_count = heapq.heappop(queue)

        if (x, y, direction, move_count) in distances:
            continue

        distances[(x, y, direction, move_count)] = distance

        for new_direction, (dx, dy) in enumerate(CARDINAL_MOVES):
            next_row = x + dx
            next_column = y + dy
            new_move_count = 1 if new_direction != direction else move_count + 1

            is_not_rev_direction = ((new_direction + 2) %
                                    4 != direction)

            is_valid_neighbor = valid_neighbor_function(
                direction, new_direction, new_move_count, move_count)

            if 0 <= next_row < row_count and 0 <= next_column < column_count and is_not_rev_direction and is_valid_neighbor:
                cost = grid[next_row][next_column]
                heapq.heappush(queue, (distance + cost, next_row,
                               next_column, new_direction, new_move_count))

    ans = float("inf")
    for (iteration_x, iteration_y, _, _), distance in distances.items():
        if iteration_x == row_count - 1 and iteration_y == column_count - 1:
            ans = min(ans, distance)

    return ans


if __name__ == '__main__':
    lines = read_lines_of_file("text.txt")
    grid = [[int(char) for char in row] for row in lines]

    print(
        f"Part one: {compute_minimal_heat_loss(part_one_valid_neighbor, grid)}")
    print(
        f"Part two: {compute_minimal_heat_loss(part_two_valid_neighbor, grid)}")
