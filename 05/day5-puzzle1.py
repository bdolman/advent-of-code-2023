from dataclasses import dataclass
from typing import List
from enum import Enum

class Category(Enum):
    SEED = "seed"
    SOIL = "soil"
    FERTILIZER = "fertilizer"
    WATER = "water"
    LIGHT = "light"
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    LOCATION = "location"

@dataclass
class Range:
    dest_range_start: int
    source_range_start: int
    range_len: int

    def source_range(self):
        return range(self.source_range_start, self.source_range_start+self.range_len)

@dataclass
class Mapping:
    source: Category
    dest: Category
    ranges: List[int]

    def map_item(self, item):
        for range in self.ranges:
            if item in range.source_range():
                relative_index = item - range.source_range_start
                return range.dest_range_start + relative_index
        return None
            

@dataclass
class Almanac:
    mappings: List[Mapping]

    def find_mapping(self, source):
        for mapping in self.mappings:
            if mapping.source == source:
                return mapping
        return None

    def map_item(self, source, dest, source_item):
        current_source = source
        current_item = source_item
        while True:
            mapping = self.find_mapping(current_source)
            current_item = mapping.map_item(current_item) or current_item
            if mapping.dest == dest:
                return current_item
            current_source = mapping.dest

def parse_seeds(line):
    seeds = list(map(int, line.split()[1:]))
    return seeds

def parse_range(line):
    int_values = list(map(int, line.split()))
    return Range(int_values[0], int_values[1], int_values[2])

def parse_almanac(file):
    mappings = []
    while True:
        mapping = read_mapping(file)
        if not mapping:
            break
        mappings.append(mapping)
    return Almanac(mappings)

def read_mapping(file):
    line = file.readline()
    if not line:
        return None

    mapping_name = line.split()[0].split("-")
    source = Category(mapping_name[0])
    dest = Category(mapping_name[2])

    ranges = []
    for line in file:
        if not line.strip():
            break
        ranges.append(parse_range(line.strip()))

    mapping = Mapping(source, dest, ranges)
    return mapping

with open("05/day5-input.txt", "r", encoding="utf-8") as file:
    seeds = parse_seeds(file.readline().strip())
    file.readline()

    almanac = parse_almanac(file)
    print(almanac)

    locations = []
    for seed in seeds:
        location = almanac.map_item(Category.SEED, Category.LOCATION, seed)
        print(f"Seed {seed} - Location {location}")
        locations.append(location)
    
    min_location = min(locations)
    print(f"Min location: {min_location}")
