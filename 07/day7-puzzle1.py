from dataclasses import dataclass
from enum import Enum
from functools import cmp_to_key

class HandType(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

strength_order = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]

@dataclass
class Hand:
    cards: str
    bid: int

    def type(self):
        counts = sorted(list(map(self.cards.count, set(list(self.cards)))))

        match counts:
            case [5]:
                return HandType.FIVE_OF_A_KIND
            case [1,4]:
                return HandType.FOUR_OF_A_KIND
            case [2,3]:
                return HandType.FULL_HOUSE
            case [1,1,3]:
                return HandType.THREE_OF_A_KIND
            case [1,2,2]:
                return HandType.TWO_PAIR
            case [1,1,1,2]:
                return HandType.ONE_PAIR
            case [1,1,1,1,1]:
                return HandType.HIGH_CARD
            
    def relative_strength(self, hand):
        if self.type() == hand.type():
            for (card1, card2) in zip(self.cards, hand.cards):
                if card1 == card2:
                    continue
                if strength_order.index(card1) < strength_order.index(card2):
                    return -1
                else:
                    return 1
            return 0
        if self.type().value < hand.type().value:
            return -1
        else:
            return 1
            
def compare_hands(hand1, hand2):
    return hand1.relative_strength(hand2) 

def rank(hands):
    return sorted(hands, key=cmp_to_key(compare_hands))

def parse_hand(str):
    cards =str.split()[0]
    bid = int(str.split()[1])
    return Hand(cards, bid)

with open("07/day7-input.txt", "r", encoding="utf-8") as file:
    hands = []
    for line in file:
        hand = parse_hand(line.strip())
        hands.append(hand)

    ranked = rank(hands)

    total_winnings = 0
    for index, hand in enumerate(ranked):
        rank = index + 1
        winnings = hand.bid * rank
        print(f"Cards: {hand.cards} Type: {hand.type()} Bid {hand.bid} Rank: {rank} Winnings: {winnings}")
        total_winnings += winnings
    print(f"Total Winnings: {total_winnings}")
    