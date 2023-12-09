CARD_ORDER = 'AKQJT98765432'
PART_TWO_CARD_ORDER = 'AKQT98765432J'


def read_lines_of_file(file) -> list[str]:
    """
    Reads the lines of the provided file and returns a tuple.
    """
    return open(file).read().split('\n')


def part_one_card_value(hand: str) -> int:
    return CARD_ORDER.index(hand)


def part_two_card_value(hand: str) -> int:
    return PART_TWO_CARD_ORDER.index(hand)


def get_hand_and_bid(line: str) -> tuple[str, int]:
    hand, bid = line.split(" ")
    return hand, int(bid)


def replace_jokers(hand):
    if 'J' not in hand:
        return hand

    counts = {card: hand.count(card) for card in set(hand) if card != 'J'}
    max_card = max(counts, key=counts.get, default=None)

    if max_card:
        return [max_card if card == 'J' else card for card in hand]
    else:
        # In case there are only J's, replace them with the lowest card
        return ['2' if card == 'J' else card for card in hand]


def is_five_of_a_kind(hand):
    return len(set(hand)) == 1


def is_four_of_a_kind(hand):
    counts = {card: hand.count(card) for card in set(hand)}
    return 4 in counts.values()


def is_full_house(hand):
    counts = {card: hand.count(card) for card in set(hand)}
    return set(counts.values()) == {2, 3}


def is_three_of_a_kind(hand):
    counts = {card: hand.count(card) for card in set(hand)}
    return 3 in counts.values() and len(counts) == 3


def is_two_pair(hand):
    counts = {card: hand.count(card) for card in set(hand)}
    return list(counts.values()).count(2) == 2


def is_one_pair(hand):
    counts = {card: hand.count(card) for card in set(hand)}
    return list(counts.values()).count(2) == 1


def sort_hands(hands):
    return sorted(hands, key=lambda hand: [-part_two_card_value(card) for card in hand])


def part_one(lines: list[str]) -> int:
    hand_and_bids = [get_hand_and_bid(line) for line in lines]
    hands = [hand for hand, bid in hand_and_bids]

    five_of_a_kind = []
    four_of_a_kind = []
    full_house = []
    three_of_a_kind = []
    two_pair = []
    one_pair = []
    high_card = []

    for hand in hands:
        scoring_hand = replace_jokers(hand)

        if is_five_of_a_kind(scoring_hand):
            five_of_a_kind.append(hand)
        elif is_four_of_a_kind(scoring_hand):
            four_of_a_kind.append(hand)
        elif is_full_house(scoring_hand):
            full_house.append(hand)
        elif is_three_of_a_kind(scoring_hand):
            three_of_a_kind.append(hand)
        elif is_two_pair(scoring_hand):
            two_pair.append(hand)
        elif is_one_pair(scoring_hand):
            one_pair.append(hand)
        else:
            high_card.append(hand)

    five_of_a_kind = sort_hands(five_of_a_kind)
    four_of_a_kind = sort_hands(four_of_a_kind)
    full_house = sort_hands(full_house)
    three_of_a_kind = sort_hands(three_of_a_kind)
    two_pair = sort_hands(two_pair)
    one_pair = sort_hands(one_pair)
    high_card = sort_hands(high_card)

    merged_hands = high_card + one_pair + two_pair + \
        three_of_a_kind + full_house + four_of_a_kind + five_of_a_kind

    multiplier = 1
    sum = 0
    for hand in merged_hands:
        bid = next((bid for h, bid in hand_and_bids if h == hand), None)
        sum += bid * multiplier
        multiplier += 1

    return sum


if __name__ == '__main__':
    lines = read_lines_of_file('text.txt')
    print(part_one(lines))
