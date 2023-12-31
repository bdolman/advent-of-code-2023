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
    card_id = str.split(": ")[0].split()[1]
    num_info = str.split(": ")[1].split(" | ")
    winning_nums = set(map(lambda s: int(s), num_info[0].split()))
    my_nums = set(map(lambda s: int(s), num_info[1].split()))

    return Card(card_id, my_nums, winning_nums)

with open("04/day4-input.txt", "r", encoding="utf-8") as file:
    cards = list(map(lambda s: parse_card(s.strip()), file))
    
    total_points = 0
    for card in cards:
        total_points += card.points()
        print(f"Card {card.id} - Winners: {card.my_winners()} - Points: {card.points()}")

    print(f"Total points: {total_points}")