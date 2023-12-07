"""
In Camel Cards, you get a list of hands, and your goal is to order them based on the strength of each hand. A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2. The relative strength of each card follows this order, where A is the highest and 2 is the lowest.

Every hand is exactly one type. From strongest to weakest, they are:

    Five of a kind, where all five cards have the same label: AAAAA
    Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
    Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
    One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    High card, where all cards' labels are distinct: 23456

Hands are primarily ordered based on type; for example, every full house is stronger than any three of a kind.

If two hands have the same type, a second ordering rule takes effect. Start by comparing the first card in each hand. If these cards are different, the hand with the stronger first card is considered stronger. If the first card in each hand have the same label, however, then move on to considering the second card in each hand. If they differ, the hand with the higher second card wins; otherwise, continue with the third card in each hand, then the fourth, then the fifth.

So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its first card is stronger. Similarly, 77888 and 77788 are both a full house, but 77888 is stronger because its third card is stronger (and both hands have the same first and second card).

To play Camel Cards, you are given a list of hands and their corresponding bid (your puzzle input). For example:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483

This example shows five hands; each hand is followed by its bid amount. Each hand wins an amount equal to its bid multiplied by its rank, where the weakest hand gets rank 1, the second-weakest hand gets rank 2, and so on up to the strongest hand. Because there are five hands in this example, the strongest hand will have rank 5 and its bid will be multiplied by 5.

So, the first step is to put the hands in order of strength:

    32T3K is the only one pair and the other hands are all a stronger type, so it gets rank 1.
    KK677 and KTJJT are both two pair. Their first cards both have the same label, but the second card of KK677 is stronger (K vs T), so KTJJT gets rank 2 and KK677 gets rank 3.
    T55J5 and QQQJA are both three of a kind. QQQJA has a stronger first card, so it gets rank 5 and T55J5 gets rank 4.

Now, you can determine the total winnings of this set of hands by adding up the result of multiplying each hand's bid with its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5). So the total winnings in this example are 6440.

Find the rank of every hand in your set. What are the total winnings?
"""

cards = [
    "J",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "T",
    "Q",
    "K",
    "A"
]

types = [
    "high card",
    "one pair",
    "two pair",
    "three of a kind",
    "full house",
    "four of a kind",
    "five of a kind"
]

hands = []

while True:
    try:
        line = input()
    except EOFError:
        break

    if not line:
        break

    # Parse the line
    match = line.split(" ")
    hand = match[0]
    bid = int(match[1])

    # Determine the type of hand
    hand_type = 0
    card_counts = {card: hand.count(card) for card in cards}

    # Take into account the jokers that act as any card to get a better hand
    jokers = card_counts["J"]
    del card_counts["J"]

    # Sort the cards by count
    card_counts_sorted = [list(x) for x in sorted(card_counts.items(), key=lambda x: x[1], reverse=True)]
    card_counts_sorted[0][1] += jokers
    
    if card_counts_sorted[0][1] == 5:
        hand_type = 6
    elif card_counts_sorted[0][1] == 4:
        hand_type = 5
    elif card_counts_sorted[0][1] == 3:
        if card_counts_sorted[1][1] == 2:
            hand_type = 4
        else:
            hand_type = 3
    elif card_counts_sorted[0][1] == 2:
        if card_counts_sorted[1][1] == 2:
            hand_type = 2
        else:
            hand_type = 1
    else:
        hand_type = 0

    # Add the hand to the list
    hands.append({
        "type": hand_type,
        "cards": [cards.index(card) for card in hand],
        "bid": bid
    })

# Sort the hands by rank then by card value left to right
hands.sort(key=lambda x: [x["type"]] + x["cards"])

# Calculate the total
print(sum(hand["bid"] * i for i, hand in enumerate(hands, start=1)))
