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

    def is_possible(self, bag_contents):
        return self.red <= bag_contents["red"] and self.green <= bag_contents["green"] and self.blue <= bag_contents["blue"]

@dataclass
class Game:
    id: int
    sets: List[Set]

    def __init__(self, game_str):
        self.id = int(game_str.split(": ")[0].split(" ")[1])
        self.sets = list(map(Set, game_str.split(": ")[1].split("; ")))

    def is_possible(self, bag_contents):
        for set in self.sets:
            if not set.is_possible(bag_contents):
                print(f"Game {self.id} (Sets: {len(self.sets)}): Not possible due to set {set}")
                print(f"Sets {self.sets}")
                return False
        print(f"Game {self.id} (Sets: {len(self.sets)}): Possible")
        print(f"Sets {self.sets}")
        return True


with open("02/day2-input.txt", "r", encoding="utf-8") as input_file:
    games = []
    for line in input_file:
        line = line.strip()
        games.append(Game(line))
    
    bag_contents = {
        "red" : 12,
        "green" : 13,
        "blue" : 14
    }

    id_total = 0
    for game in games:
        if game.is_possible(bag_contents):
            id_total += game.id
    
    print(f"Sum of possible game IDs: {id_total}")


