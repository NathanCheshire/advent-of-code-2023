def read_lines_of_file(file) -> list[str]:
    """
    Reads the lines of the provided file and returns a tuple.
    """
    return open(file).read().split('\n')


def parse_line_for_numbers(line: str) -> tuple[int]:
    return [int(num) for num in line.split(' ')]


def compute_row_differences(numbers: list[int]) -> list[int]:
    """
    Returns a list of the differences between consecutive numbers in the list.
    """
    return [numbers[number + 1] - numbers[number] for number in range(len(numbers) - 1)]


def extrapolate_next_value(numbers: list[int]) -> int:
    rows = [numbers]

    while rows[-1]:
        next_row = compute_row_differences(rows[-1])
        all_zeros = all(number == 0 for number in next_row)
        if not next_row or all_zeros:
            break

        rows.append(next_row)

    for row_index in range(len(rows) - 2, -1, -1):
        current_row_value = rows[row_index][-1]
        down_row_over_value = rows[row_index + 1][-1]

        rows[row_index].append(current_row_value + down_row_over_value)

    top_row = rows[0]
    next_value = top_row[-1]
    return next_value


def part_one(lines: list[str]) -> int:
    sum = 0
    for line in lines:
        numbers = parse_line_for_numbers(line)
        next_number = extrapolate_next_value(numbers)
        sum += next_number

    return sum


if __name__ == '__main__':
    lines = read_lines_of_file("text.txt")
    print(f"Part one: {part_one(lines)}")
