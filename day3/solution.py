import re

directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
              (0, 1), (1, -1), (1, 0), (1, 1)]


def read_lines_of_file(file) -> list[str]:
    """
    Reads the lines of the provided file and returns a tuple.
    """
    return open(file).read().split('\n')


def is_symbol(char):
    return not char.isdigit() and char != '.'


def get_neighbors(grid, x, y):
    neighbors = []
    rows, cols = len(grid), len(grid[0])

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            neighbors.append(grid[nx][ny])

    return neighbors


def extract_numbers_next_to_symbols_improved(lines: list[str]) -> list[int]:
    grid = [list(line) for line in lines]

    numbers_next_to_symbols = []
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y].isdigit():
                number = grid[x][y]
                print(f"On number: {number}")

                if y > 0 and grid[x][y - 1].isdigit():
                    print("Skipping because higher is digit")
                    continue

                ny = y + 1
                while ny < len(grid[x]) and grid[x][ny].isdigit():
                    number += grid[x][ny]
                    ny += 1

                for i in range(len(number)):
                    if any(is_symbol(neighbor) for neighbor in get_neighbors(grid, x, y + i)):
                        numbers_next_to_symbols.append(int(number))
                        break

    return numbers_next_to_symbols


def part_one():
    lines = read_lines_of_file("./text.txt")
    print(f"lines read: {len(lines)}")

    numbers_next_to_symbols = extract_numbers_next_to_symbols_improved(lines)

    sum = 0
    for number in numbers_next_to_symbols:
        sum = sum + number
    print(f"Sum: {sum}")


def part_two():
    pass


if __name__ == '__main__':
    part_one()
    part_two()
