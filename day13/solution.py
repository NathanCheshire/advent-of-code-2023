import numpy as np

VERTICAL_FACTOR = 100


def read_lines_of_file(file: str, splitter: str = '\n') -> list[str]:
    """
    Reads the lines of the provided file and returns a tuple.
    """
    return open(file).read().split(splitter)


def compute_symmetry(block: np.ndarray, allowable_error: int = 0) -> int | bool:
    """
    Returns the symmetric line of this block or False if the block is not symmetric meaning the other axis
    is what the block is symmetric on.
    """
    current_line_index = 1

    while current_line_index < len(block):
        top_half = block[:current_line_index]
        bottom_half = block[current_line_index:]

        # Extend boundaries so we have matching number of rows/cols on either side of a dividing line
        if len(top_half) > len(bottom_half):
            top_half = top_half[len(top_half) - len(bottom_half):]
        elif len(bottom_half) > len(top_half):
            bottom_half = bottom_half[: len(top_half)]

        flipped_bottom_half = np.flip(bottom_half, axis=0)

        # this is exactly equal because the problem said so, applying LTE or GTE will not work
        # the flip could happen with either side
        if np.count_nonzero(top_half != flipped_bottom_half) == allowable_error:
            return current_line_index

        current_line_index += 1

    return False


def calculate_max_symmetry(blocks: list[list[str]], allowable_error: int = 0) -> int:
    """
    Returns the symmetry value for this block, if the line is vertical, the number of cols to the
    left * 100 is returned, else the number of rows above the line.
    """
    max_symmetry = 0

    for block in blocks:
        char_lists = [list(line) for line in block]
        numpy_lined_block = np.array(char_lists)
        transposed_block = numpy_lined_block.T

        computed_symmetry = compute_symmetry(transposed_block, allowable_error)

        if computed_symmetry:
            max_symmetry += computed_symmetry
        else:
            max_symmetry += VERTICAL_FACTOR * \
                compute_symmetry(numpy_lined_block, allowable_error)

    return max_symmetry


if __name__ == '__main__':
    lines = read_lines_of_file("text.txt", splitter='\n\n')
    blocks = [line.splitlines() for line in lines]

    print(f"Part 1: {calculate_max_symmetry(blocks)}")
    print(f"Part 2: {calculate_max_symmetry(blocks, 1)}")
