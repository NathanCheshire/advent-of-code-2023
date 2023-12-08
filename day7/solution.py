CARD_ORDER = 'AKQJT98765432'
PART_TWO_CARD_ORDER = 'AKQT98765432J'


def read_lines_of_file(file) -> list[str]:
    """
    Reads the lines of the provided file and returns a tuple.
    """
    return open(file).read().split('\n')


def card_value(card):
    return PART_TWO_CARD_ORDER.index(card)


def get_hand_and_bid(line: str) -> tuple[str, int]:
    hand, bid = line.split(" ")
    return hand, int(bid)


def first_hand_stronger(hand_one: str, hand_two: str) -> bool:
    for card1, card2 in zip(hand_one, hand_two):
        if card_value(card1) < card_value(card2):
            return True
        elif card_value(card1) > card_value(card2):
            return False

    return False


def count_with_joker(counts, jokers):
    return {card: count + jokers for card, count in counts.items()}


def is_five_of_a_kind(hand):
    counts = {card: hand.count(card) for card in set(hand) if card != 'J'}
    jokers = hand.count('J')
    return 5 in count_with_joker(counts, jokers).values()


def is_four_of_a_kind(hand):
    counts = {card: hand.count(card) for card in set(hand) if card != 'J'}
    jokers = hand.count('J')
    return 4 in count_with_joker(counts, jokers).values()


def is_full_house(hand):
    counts = {card: hand.count(card) for card in set(hand) if card != 'J'}
    jokers = hand.count('J')
    modified_counts = count_with_joker(counts, jokers)
    return set(modified_counts.values()) == {2, 3} or (3 in modified_counts.values() and jokers > 0)


def is_three_of_a_kind(hand):
    counts = {card: hand.count(card) for card in set(hand) if card != 'J'}
    jokers = hand.count('J')
    return 3 in count_with_joker(counts, jokers).values()


def is_two_pair(hand):
    counts = {card: hand.count(card) for card in set(hand) if card != 'J'}
    jokers = hand.count('J')
    return list(count_with_joker(counts, jokers).values()).count(2) >= 2 or (2 in counts.values() and jokers > 0)


def is_one_pair(hand):
    counts = {card: hand.count(card) for card in set(hand) if card != 'J'}
    jokers = hand.count('J')
    return list(count_with_joker(counts, jokers).values()).count(2) >= 1 or (1 in counts.values() and jokers > 0)


def sort_hands(hands):
    return sorted(hands, key=lambda hand: [-card_value(card) for card in hand])


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
        if is_five_of_a_kind(hand):
            five_of_a_kind.append(hand)
        elif is_four_of_a_kind(hand):
            four_of_a_kind.append(hand)
        elif is_full_house(hand):
            full_house.append(hand)
        elif is_three_of_a_kind(hand):
            three_of_a_kind.append(hand)
        elif is_two_pair(hand):
            two_pair.append(hand)
        elif is_one_pair(hand):
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
