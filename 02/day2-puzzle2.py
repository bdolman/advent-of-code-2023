from dataclasses import dataclass
from typing import List

@dataclass
class Set:
    red: int
    green: int
    blue: int

    def __init__(self, set_str):
        draws_str = set_str.split(", ")
        keyvals = dict(map(lambda draw: (draw.split(" ")[1], draw.split(" ")[0]), draws_str))
        self.red = int(keyvals.get("red", 0))
        self.green = int(keyvals.get("green", 0))
        self.blue = int(keyvals.get("blue", 0))

@dataclass
class Game:
    id: int
    sets: List[Set]

    def __init__(self, game_str):
        self.id = int(game_str.split(": ")[0].split(" ")[1])
        self.sets = list(map(Set, game_str.split(": ")[1].split("; ")))

    def min_bag(self):
        bag = Bag(
            red = max(map(lambda s: s.red, self.sets)),
            green = max(map(lambda s: s.green, self.sets)),
            blue = max(map(lambda s: s.blue, self.sets))
        )
        return bag

    
@dataclass
class Bag:
    red: int
    green: int
    blue: int


with open("02/day2-input.txt", "r", encoding="utf-8") as input_file:
    games = []
    for line in input_file:
        line = line.strip()
        games.append(Game(line))
    
    bag = Bag(red=12, green=13, blue=14)

    total_power = 0
    for game in games:
        bag = game.min_bag()
        bag_power = bag.red * bag.green * bag.blue
        total_power += bag_power
        print(f"Game {game.id}: Min bag: {bag}: Power: {bag_power}")
    print(f"Total Power: {total_power}")