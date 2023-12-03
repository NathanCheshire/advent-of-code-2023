NEIGHBOR_OFFSETS = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                    (0, 1), (1, -1), (1, 0), (1, 1)]


def read_lines_of_file(file) -> list[str]:
    """
    Reads the lines of the provided file and returns a tuple.
    """
    return open(file).read().split('\n')


def is_symbol(char):
    """
    Returns whether the provided character is a symbol meaning not a digit and not a period.
    """
    return not char.isdigit() and char != '.'


def get_neighbors(grid: list[list[str]], x: int, y: int) -> list[str]:
    """
    Returns the neighbors of the provided grid x,y position.
    """
    neighbors = []
    rows, cols = len(grid), len(grid[0])

    for offset_x, offset_y in NEIGHBOR_OFFSETS:
        nx = x + offset_x
        ny = y + offset_y
        nx_in_bounds = 0 <= nx < rows
        ny_in_bounds = 0 <= ny < cols
        if nx_in_bounds and ny_in_bounds:
            neighbors.append(grid[nx][ny])

    return neighbors


def compute_part_number_sum(grid: list[list[str]]) -> int:
    """
    The part one solution, computes the sum of all part numbers of the grid.
    """
    numbers_next_to_symbols = []
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y].isdigit():
                number = grid[x][y]

                if y > 0 and grid[x][y - 1].isdigit():
                    continue

                ny = y + 1
                while ny < len(grid[x]) and grid[x][ny].isdigit():
                    number += grid[x][ny]
                    ny += 1

                for i in range(len(number)):
                    if any(is_symbol(neighbor) for neighbor in get_neighbors(grid, x, y + i)):
                        numbers_next_to_symbols.append(int(number))
                        break

    sum = 0
    for number in numbers_next_to_symbols:
        sum = sum + number

    return sum


def find_numbers_around_gear(grid, x, y) -> list[int]:
    """
    Finds the number around the provided gear position.
    """
    # there will probably not be duplicate numbers so this helps eliminate a duplicate number bug I was seeing
    numbers = set()

    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue

            nx = x + dx
            ny = y + dy

            in_x_bounds = 0 <= nx < len(grid)
            in_y_bounds = 0 <= ny < len(grid[0])
            is_digit = grid[nx][ny].isdigit()

            # construct the full number of all the digits
            if in_x_bounds and in_y_bounds and is_digit:
                # extend left attempt
                number = ''
                lx = nx
                ly = ny
                while ly >= 0 and grid[lx][ly].isdigit():
                    number = grid[lx][ly] + number
                    ly -= 1

                # extend right attempt
                rx = nx
                ry = ny + 1

                while ry < len(grid[0]) and grid[rx][ry].isdigit():
                    number += grid[rx][ry]
                    ry += 1

                numbers.add(number)

    return numbers


def calculate_gear_ratio_sum(grid: list[list[str]]) -> int:
    """
    The part two solution, computes the sum of all gear ratios of the grid.
    """
    x_len = len(grid)
    y_len = len(grid[0])

    total_sum = 0
    for x in range(x_len):
        for y in range(y_len):
            if grid[x][y] != '*':
                continue

            numbers = find_numbers_around_gear(grid, x, y)

            if len(numbers) == 2:
                num1, num2 = map(int, numbers)
                total_sum += num1 * num2

    return total_sum


if __name__ == '__main__':
    lines = read_lines_of_file("./text.txt")
    grid = [list(line) for line in lines]

    # part 1
    sum = compute_part_number_sum(grid)
    print(f"Sum: {sum}")

    # part 2
    gear_ratio = calculate_gear_ratio_sum(grid)
    print(f"Gear ratio: {gear_ratio}")
