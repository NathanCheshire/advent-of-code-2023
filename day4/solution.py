def read_lines_of_file(file) -> list[str]:
    """
    Reads the lines of the provided file and returns a tuple.
    """
    return open(file).read().split('\n')


def get_winning_and_our_number_lists(line: str) -> tuple[list[int], list[int]]:
    _, numbers = line.split(":")
    winning_numbers, our_numbers = numbers.split("|")

    winning_numbers_string = winning_numbers.split()
    our_numbers_string = our_numbers.split()

    winning_numbers_list = [int(num) for num in winning_numbers_string]
    our_numbers_list = [int(num) for num in our_numbers_string]

    return winning_numbers_list, our_numbers_list


def get_card_score(line: str) -> int:
    winning_numbers_list, our_numbers_list = get_winning_and_our_number_lists(
        line)

    num_matches = 0
    for our_number in our_numbers_list:
        if our_number in winning_numbers_list:
            if num_matches == 0:
                num_matches = 1
            else:
                num_matches = num_matches * 2

    return num_matches


def get_num_card_matches(line: str) -> int:
    winning_numbers_list, our_numbers_list = get_winning_and_our_number_lists(
        line)
    return sum(1 for our_number in our_numbers_list if our_number in winning_numbers_list)


def calculate_cards_from_index(index: int, lines: list[str], memo: dict[int, int]) -> int:
    if index >= len(lines):
        return 0
    if index in memo:
        return memo[index]

    num_matches = get_num_card_matches(lines[index])
    total_cards = 1

    # card indicies start at 1
    for i in range(1, num_matches + 1):
        next_index = index + i
        total_cards += calculate_cards_from_index(next_index, lines, memo)

    memo[index] = total_cards
    return total_cards


def calculate_number_of_cards(lines: list[str]) -> int:
    memo = {}
    total_cards = sum(calculate_cards_from_index(i, lines, memo)
                      for i in range(len(lines)))
    return total_cards


def part_one(lines: list[str]) -> None:
    score_sum = 0
    for line in lines:
        score = get_card_score(line)
        score_sum = score_sum + score

    print(f"Part one score: {score_sum}")


def part_two(lines: list[str]) -> None:
    print(f"Part two score: {calculate_number_of_cards(lines)}")


if __name__ == '__main__':
    lines = read_lines_of_file("./text.txt")
    part_one(lines)
    part_two(lines)
