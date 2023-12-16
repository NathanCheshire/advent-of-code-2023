STEP_SEPARATOR = ','
LENS_ASSIGNMENT = '='


def read_lines_of_file(file: str, splitter: str = '\n') -> list[str]:
    """
    Reads the lines of the provided file and returns a tuple.
    """
    return open(file).read().split(splitter)


def hash(to_hash: str) -> int:
    ret = 0

    for char in to_hash:
        ascii_value = ord(char)
        ret += ascii_value
        ret = ret * 17
        ret = ret % 256

    return ret


def get_steps(lines: list[str]) -> list[str]:
    sequence_line = lines[0]
    steps = sequence_line.split(STEP_SEPARATOR)
    return steps


def part_one(lines: list[str]) -> int:
    steps = get_steps(lines)
    return sum(hash(step) for step in steps)


def part_two(lines: list[str]) -> int:
    steps = get_steps(lines)

    boxes = {}

    for step in steps:
        label = step[0: len(step) - 1]
        last_char = step[-1]
        second_last_char = step[-2]

        if second_last_char == LENS_ASSIGNMENT:
            label = step[0: len(step) - 2]

        box_to_place_label_in = hash(label)

        if last_char == '-' and box_to_place_label_in in boxes.keys():
            box_contents = boxes[box_to_place_label_in]
            new_box_contents = [(cur_label, cur_focal_length) for cur_label,
                                cur_focal_length in box_contents if cur_label != label]
            boxes[box_to_place_label_in] = new_box_contents
        elif second_last_char == LENS_ASSIGNMENT:
            focal_length = last_char

            if box_to_place_label_in in boxes.keys():
                box_contents = boxes[box_to_place_label_in]

                if any(cur_label == label for (cur_label, _) in box_contents):
                    # find the old lens and replace with, basically just updating focal length
                    new_box_contents = []
                    for cur_label, cur_focal_length in box_contents:
                        if cur_label == label:
                            new_box_contents.append((cur_label, focal_length))
                        else:
                            new_box_contents.append(
                                (cur_label, cur_focal_length))

                    boxes[box_to_place_label_in] = new_box_contents
                else:
                    box_contents.append((label, focal_length))
                    boxes[box_to_place_label_in] = box_contents

            else:
                boxes[box_to_place_label_in] = [(label, focal_length)]

    sum_focusing_powers = 0
    for box_number, box_contents in boxes.items():
        for index, (label, focal_length) in enumerate(box_contents):
            sum_focusing_powers += (1 + int(box_number)) * \
                (index + 1) * (int(focal_length))

    return sum_focusing_powers


if __name__ == '__main__':
    lines = read_lines_of_file("text.txt")

    print(f"Part one: {part_one(lines)}")
    print(f"Part two: {part_two(lines)}")
