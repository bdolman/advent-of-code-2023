from dataclasses import dataclass
from typing import List
from typing import Set

@dataclass
class Card:
    id: int
    my_nums: Set[int]
    winning_nums: Set[int]

    def my_winners(self):
        return self.my_nums & self.winning_nums
    
    def points(self):
        win_count = len(self.my_winners())
        if win_count == 0:
            return 0
        return 2 ** (win_count - 1)


def parse_card(str):
    card_id = int(str.split(": ")[0].split()[1])
    num_info = str.split(": ")[1].split(" | ")
    winning_nums = set(map(lambda s: int(s), num_info[0].split()))
    my_nums = set(map(lambda s: int(s), num_info[1].split()))

    return Card(card_id, my_nums, winning_nums)

def winning_cards_count(card, all_cards):
    next_card_index = card.id
    win_count = len(card.my_winners())
    winning_cards = all_cards[next_card_index:next_card_index + win_count]
    return len(winning_cards) + sum(list(map(lambda c: winning_cards_count(c, all_cards), winning_cards)))

with open("04/day4-input.txt", "r", encoding="utf-8") as file:
    cards = list(map(lambda s: parse_card(s.strip()), file))

    winning_cards = len(cards)
    for card in cards:
        winning_cards += winning_cards_count(card, cards)
        print(f"Card {card.id} - Winners: {card.my_winners()} - Total winning cards: {winning_cards}")

    print(f"Total cards: {winning_cards}")