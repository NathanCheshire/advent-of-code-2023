import math
import re

GRAPH_LINE_PATTERN = r"(\w+)\s=\s\((\w+),\s(\w+)\)"

ABSOLUTE_START = "AAA"
ABSOLUTE_END = "ZZZ"
GHOST_START = "A"
GHOST_END = "B"

GRAPH_START_INDEX = 1
GRAPH_LEFT_INDEX = 2
GRAPH_RIGHT_INDEX = 3


def read_lines_of_file(file) -> list[str]:
    """
    Reads the lines of the provided file and returns a tuple.
    """
    return open(file).read().split('\n')


def contruct_graph(lines: list[str]) -> dict[str, tuple[str, str]]:
    """
    Constructs a graph for the paths. The dictionary key is the id of the node and the
    key contains the left as the first tuple part and the rightas the second tuple part.
    """
    graph = {}

    for line in lines:
        matched = re.match(GRAPH_LINE_PATTERN, line)

        start = matched.group(GRAPH_START_INDEX)
        left = matched.group(GRAPH_LEFT_INDEX)
        right = matched.group(GRAPH_RIGHT_INDEX)

        graph[start] = (left, right)

    return graph


def parse_instructions_and_graph(lines: list[str]) -> tuple[str, dict[str, tuple[str, str]]]:
    instructions = lines[0]
    graph = contruct_graph(lines[2:])
    return instructions, graph


def part_one(lines: list[str]) -> None:
    instructions, graph = parse_instructions_and_graph(lines)

    current_position = ABSOLUTE_START
    current_instruction = 0
    steps = 0

    while current_position != ABSOLUTE_END:
        direction_to_move = instructions[current_instruction]
        next_index = 0 if direction_to_move == "L" else 1
        current_position = graph[current_position][next_index]
        steps += 1
        current_instruction = (current_instruction + 1) % len(instructions)

    return steps


def get_ghost_start_positions(graph: dict[str, tuple[str, str]]) -> list[str]:
    return [start for start in graph if start[-1] in (GHOST_START, GHOST_END)]


def part_two(lines: list[str]) -> None:
    instructions, graph = parse_instructions_and_graph(lines)

    ghost_start_positions = get_ghost_start_positions(graph)
    distance_to_end = {}

    for ghost_start_position in ghost_start_positions:
        current_position = ghost_start_position
        current_step, steps = (0, 0)

        while current_position[-1] != GHOST_END or steps == 0:
            direction_to_move = instructions[current_step]

            next_index = 0 if direction_to_move == "L" else 1
            current_position = graph[current_position][next_index]

            steps += 1
            current_step = (current_step + 1) % len(instructions)

        distance_to_end[ghost_start_position] = steps

    # minimum steps for all ghost paths to be on nodes that end with Z
    steps = math.lcm(*distance_to_end.values())

    return steps


if __name__ == '__main__':
    lines = read_lines_of_file("./text.txt")
    print(part_one(lines))
    print(part_two(lines))
