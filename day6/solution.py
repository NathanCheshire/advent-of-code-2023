def read_lines_of_file(file) -> list[str]:
    """
    Reads the lines of the provided file and returns a tuple.
    """
    return open(file).read().split('\n')


def compute_number_of_ways_to_beat_record(distance: int, record: int) -> int:
    times_that_will_beat_record = []

    for hold_time in range(1, record + 1):
        time_to_complete_distance = (distance / hold_time) + hold_time
        if time_to_complete_distance < record:
            times_that_will_beat_record.append(hold_time)

    return len(times_that_will_beat_record)


def get_ways_to_beat_times_multiplied(lines: list[str]) -> None:
    time_line = lines[0].split('Time: ')[1]
    distance_line = lines[1].split('Distance: ')[1]

    multiplied = 1
    for time, distance in zip(time_line.split(), distance_line.split()):
        ways_to_beat = compute_number_of_ways_to_beat_record(
            int(distance), int(time))
        multiplied = multiplied * ways_to_beat

    return multiplied


def get_ways_to_beat_merged_numbers_distance_and_time(lines: list[str]) -> None:
    time_line = lines[0].split('Time: ')[1]
    distance_line = lines[1].split('Distance: ')[1]

    time_line = time_line.replace(' ', '')
    distance_line = distance_line.replace(' ', '')

    time = int(time_line)
    distance = int(distance_line)
    return compute_number_of_ways_to_beat_record(distance, time)


if __name__ == '__main__':
    lines = read_lines_of_file("text.txt")

    part_one_solution = get_ways_to_beat_times_multiplied(lines)
    print(f"Part one: {part_one_solution}")

    part_one_solution = get_ways_to_beat_merged_numbers_distance_and_time(lines)
    print(f"Part two: {part_one_solution}")
