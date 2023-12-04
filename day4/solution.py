def read_lines_of_file(file) -> list[str]:
    """
    Reads the lines of the provided file and returns a tuple.
    """
    return open(file).read().split('\n')


def get_card_score(line: str) -> int:
    _, numbers = line.split(":")
    winning_numbers, our_numbers = numbers.split("|")

    winning_numbers_string = winning_numbers.split()
    our_numbers_string = our_numbers.split()

    winning_numbers_list = [int(num) for num in winning_numbers_string]
    our_numbers_list = [int(num) for num in our_numbers_string]

    num_matches = 0
    for our_number in our_numbers_list:
        if our_number in winning_numbers_list:
            if num_matches == 0:
                num_matches = 1
            else:
                num_matches = num_matches * 2

    print("Num matches: ", num_matches)
    return num_matches


def part_one():
    lines = read_lines_of_file("./text.txt")

    score_sum = 0
    for line in lines:
        score = get_card_score(line)
        score_sum = score_sum + score

    print(f"Score: {score_sum}")


if __name__ == '__main__':
    part_one()
