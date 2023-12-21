
def read_lines_of_file(file: str, splitter: str = '\n') -> list[str]:
    """
    Reads the lines of the provided file and returns a tuple.
    """
    return open(file).read().split(splitter)


class Rating():
    def __init__(self, rating_string: str):
        parts = rating_string.strip('{}').split(",")

        x = parts[0]
        m = parts[1]
        a = parts[2]
        s = parts[3]

        x = x[2:]
        m = m[2:]
        a = a[2:]
        s = s[2:]

        self.x = int(x)
        self.m = int(m)
        self.a = int(a)
        self.s = int(s)

    def get_x(self):
        return self.x

    def get_m(self):
        return self.m

    def get_a(self):
        return self.a

    def get_s(self):
        return self.s

    def get_sum(self):
        return self.x + self.m + self.a + self.s


class Workflow():
    def __init__(self, name: str, rules: list[str]):
        self.name = name
        self.rules = rules

    def get_rules(self):
        return self.rules

    def get_name(self):
        return self.name

    def get_next_workflow_name_or_accept_or_reject(self, input: Rating) -> str:
        for rule in self.rules:
            rating_input = rule[0]

            if rating_input == 'x':
                rating_input = input.get_x()
            elif rating_input == 'm':
                rating_input = input.get_m()
            elif rating_input == 'a':
                rating_input = input.get_a()
            elif rating_input == 's':
                rating_input = input.get_s()

            if '<' in rule:
                rule_comparison_num, next_rule_if_true = rule[2:].split(":")
                rule_comparison_num = int(rule_comparison_num)
                if rating_input < rule_comparison_num:
                    return next_rule_if_true
            elif '>' in rule:
                rule_comparison_num, next_rule_if_true = rule[2:].split(":")
                rule_comparison_num = int(rule_comparison_num)
                if rating_input > rule_comparison_num:
                    return next_rule_if_true
            elif '>' not in rule and '<' not in rule:
                return rule


def construct_workflow(workflow_string: str) -> Workflow:
    name, rules = workflow_string.split('{')
    rules = rules[0:-1]

    rules = rules.split(",")
    return Workflow(name, rules)


def narrow_ranges_based_on_workflow(current_ranges: dict[str, tuple[int, int]], workflows, workflow_name: str):
    # base cases
    if workflow_name == "R":
        return 0
    if workflow_name == "A":
        product = 1
        for current_low, current_high in current_ranges.values():
            product *= current_high - current_low + 1
        return product

    current_workflow = workflows[workflow_name]

    total = 0

    for rule in current_workflow.get_rules():
        # final rule so no comparison, just invoke
        if ':' not in rule:
            total += narrow_ranges_based_on_workflow(
                current_ranges, workflows, rule)
        else:
            letter = rule[0]
            operator = rule[1]
            comparison_number = int(rule.split(':')[0][2:])
            final_workflow = rule.split(':')[1]

            current_low, current_high = current_ranges[letter]

            if operator == "<":
                new_low = current_low
                new_high = min(comparison_number - 1, current_high)
            else:
                new_low = max(comparison_number + 1, current_low)
                new_high = current_high

            if new_low < new_high:
                ranges_copy = dict(current_ranges)
                ranges_copy[letter] = (new_low, new_high)
                total += narrow_ranges_based_on_workflow(ranges_copy,
                                                         workflows, final_workflow)

            if operator == "<":
                new_low = max(comparison_number, current_low)
                new_high = current_high
            else:
                new_low = current_low
                new_high = min(comparison_number, current_high)

            if new_low < new_high:
                current_ranges[letter] = (new_low, new_high)

    return total


def part_two(workflows_and_ratings: list[str]) -> int:
    workflow_lines = workflows_and_ratings[0].splitlines()
    workflows = {}

    for workflow_line in workflow_lines:
        workflow_name = workflow_line.split("{")[0]
        workflows[workflow_name] = construct_workflow(workflow_line)

    current_ranges = {'x': (1, 4000), 'm': (
        1, 4000), 'a': (1, 4000), 's': (1, 4000)}
    return narrow_ranges_based_on_workflow(current_ranges, workflows, 'in')


def part_one(workflows_and_ratings: list[str]) -> int:
    workflows = workflows_and_ratings[0].split('\n')
    ratings = workflows_and_ratings[1].split('\n')

    actual_workflows = {}
    for workflow in workflows:
        parsed_workflow = construct_workflow(workflow)
        actual_workflows[parsed_workflow.get_name()] = parsed_workflow

    accepted_ratings = []
    for rating in ratings:
        parsed_rating = Rating(rating)

        next_workflow_name = 'in'

        while next_workflow_name not in ['R', 'A']:
            next_workflow_name = actual_workflows[next_workflow_name].get_next_workflow_name_or_accept_or_reject(
                parsed_rating)

        if next_workflow_name == 'A':
            accepted_ratings.append(parsed_rating)

    return sum(rating.get_sum() for rating in accepted_ratings)


if __name__ == '__main__':
    workflows_and_ratings = read_lines_of_file('text.txt', '\n\n')
    print(f"Part one: {part_one(workflows_and_ratings)}")
    print(f"Part two: {part_two(workflows_and_ratings)}")
