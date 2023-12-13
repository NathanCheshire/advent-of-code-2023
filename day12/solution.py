from functools import cache


UNFOLD_FACTOR = 5
OPERATIONAL_SPRING = "."
DAMAGED_SPRING = "#"
UNKNOWN_SPRING = '?'


def read_lines_of_file(file) -> list[str]:
    """
    Reads the lines of the provided file and returns a tuple.
    """
    return open(file).read().split('\n')


def parse_lines(lines: list[str]) -> list[tuple[str, list[int]]]:
    """
    Parses the file lines and returns a list of tuples representing each line's springs and the spring states.
    """
    data = []

    for line in lines:
        springs, continuous_damaged_group_sizes_str = line.split()
        continuous_damaged_group_sizes = [
            int(num) for num in continuous_damaged_group_sizes_str.split(',')]

        data.append((springs, tuple(continuous_damaged_group_sizes)))

    return data


def compute_data_arrangements(data: list[tuple[str, list[int]]]) -> int:
    """
    Computes the arrangements of the provided spring and spring state pairs.
    """
    arrangements = 0

    for springs, damaged_groups in data:
        arrangements += calculate_number_of_arrangements(
            springs, damaged_groups)

    return arrangements


@cache
def calculate_number_of_arrangements(remaining_springs: str, damaged_groups: list[int], damaged_springs: int = 0):
    no_springs = not remaining_springs
    if no_springs:
        num_damanged_groups = len(damaged_groups)
        if ((num_damanged_groups == 1 and damaged_groups[0] == damaged_springs)
                or (num_damanged_groups == 0 and damaged_springs == 0)):
            return 1
        return 0

    first_spring = remaining_springs[0]
    remaining_springs = remaining_springs[1:]

    # separate out first size from remaining
    current_group_size = damaged_groups[0] if damaged_groups else 0
    remaining_group_sizes = damaged_groups[1:] if damaged_groups else [0]

    if first_spring == UNKNOWN_SPRING:
        with_damaged_spring = DAMAGED_SPRING + remaining_springs
        arrangements_with_damaged_spring = calculate_number_of_arrangements(
            with_damaged_spring, damaged_groups, damaged_springs)

        with_operational_spring = OPERATIONAL_SPRING + remaining_springs
        arrangements_with_operational_spring = calculate_number_of_arrangements(
            with_operational_spring, damaged_groups, damaged_springs)

        return arrangements_with_damaged_spring + arrangements_with_operational_spring

    if first_spring == DAMAGED_SPRING:
        if damaged_springs > current_group_size:
            return 0

        return calculate_number_of_arrangements(remaining_springs, damaged_groups, damaged_springs + 1)

    if first_spring == OPERATIONAL_SPRING:
        if damaged_springs == 0:
            return calculate_number_of_arrangements(remaining_springs, damaged_groups, 0)
        if damaged_springs == current_group_size:
            return calculate_number_of_arrangements(remaining_springs, remaining_group_sizes, 0)
        return 0


def unfold_record_line(springs: str, continuous_damaged_group_sizes: str):
    """
    Unfolds the record line by duplicating the spring lines joined by
      the unknown spring state character and duplicating the state sizes.
    """
    duplicated_springs = UNKNOWN_SPRING.join([springs] * UNFOLD_FACTOR)
    duplicated_continuous_damaged_group_sizes = continuous_damaged_group_sizes * UNFOLD_FACTOR

    return duplicated_springs, duplicated_continuous_damaged_group_sizes


if __name__ == '__main__':
    lines = read_lines_of_file("text.txt")
    data = parse_lines(lines)

    print(f'Part 1: {compute_data_arrangements(data)}')

    part_two_data = [unfold_record_line(springs, continuous_damaged_group_sizes)
                     for springs, continuous_damaged_group_sizes in data]
    print(f'Part 1: {compute_data_arrangements(part_two_data)}')
