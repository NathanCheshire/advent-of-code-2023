import re


def convert_string_numbers(string: str) -> str:
    return (string.replace("one", "one1one")
            .replace("two", "two2two")
            .replace("three", "three3three")
            .replace("four", "four4four")
            .replace("five", "five5five")
            .replace("six", "six6six")
            .replace("seven", "seven7seven")
            .replace("eight", "eight8eight")
            .replace("nine", "nine9nine"))


def read_lines_of_file(file) -> list[str]:
    return open(file).read().split('\n')


def extract_first_and_last_number(string: str) -> tuple[int, int]:
    numbers = re.findall(r'\d', string)
    first_number = numbers[0]
    last_number = numbers[-1] if len(numbers) > 1 else first_number

    return int(first_number), int(last_number)


def main():
    print('Starting solution for day 1 of advent of code...')

    lines = read_lines_of_file("./text.txt")
    print(f"Lines read: {len(lines)}")

    running_sum = 0
    for line in lines:
        print(f"On line: {line}")
        corrected_line = convert_string_numbers(line)
        print(f"Corrected line: {corrected_line}")
        first_num, last_num = extract_first_and_last_number(corrected_line)
        print(f"First and last: {first_num}, {last_num}")
        combined = first_num * 10 + last_num
        print(f"Combined: {combined}")
        running_sum = running_sum + combined

    print(f"Sum of calibration values: {running_sum}")


if __name__ == '__main__':
    main()
