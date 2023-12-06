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
    ranges: List[Range]

    def map_partial_range(self, source_range):
        for mapping_range in self.ranges:
            mapping_native_range = mapping_range.source_range()
            if source_range.start >= mapping_native_range.start and source_range.start <= mapping_native_range.stop:
                relative_start_index = source_range.start - mapping_range.source_range_start
                dest_start = mapping_range.dest_range_start+relative_start_index
                dest_end = min(mapping_range.dest_range_start+mapping_range.range_len, dest_start + len(source_range))
                dest_range = range(dest_start, dest_end)
                return dest_range
        return None

    def map_range(self, source_range):
        dest_ranges = []
        current_source_range = source_range
        current_dest_range = self.map_partial_range(current_source_range)
        while current_dest_range:
            dest_ranges.append(current_dest_range)
            current_source_range = range(current_source_range.start + len(current_dest_range), current_source_range.stop)
            if not len(current_source_range):
                break
            current_dest_range = self.map_partial_range(current_source_range)

        if len(current_source_range):
            dest_ranges.append(current_source_range)

        return dest_ranges
            

@dataclass
class Almanac:
    mappings: List[Mapping]

    def find_mapping(self, source):
        for mapping in self.mappings:
            if mapping.source == source:
                return mapping
        return None

    def map_range(self, source, dest, source_range):
        current_source = source
        current_ranges = [source_range]
        while True:
            mapping = self.find_mapping(current_source)
            new_ranges = []
            for r in current_ranges:
                new_ranges += mapping.map_range(r)
            print(f"Mapping: {mapping.source} -> {mapping.dest}: {current_ranges} -> {new_ranges}")
            current_ranges = new_ranges
            if mapping.dest == dest:
                return current_ranges
            current_source = mapping.dest

def parse_seed_ranges(line):
    raw_seed_numbers = list(map(int, line.split()[1:]))

    ranges = []
    index = 0
    while index < len(raw_seed_numbers):
        range_start = raw_seed_numbers[index]
        range_len = raw_seed_numbers[index+1]
        ranges.append(range(range_start, range_start+range_len))
        index += 2

    return ranges

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
    seed_ranges = parse_seed_ranges(file.readline().strip())
    file.readline()

    almanac = parse_almanac(file)

    all_location_ranges = []
    for seed_range in seed_ranges:
        seed_locations = almanac.map_range(Category.SEED, Category.LOCATION, seed_range)
        print(f"Seed Range: {seed_range} Location Ranges: {seed_locations}")
        all_location_ranges += seed_locations

    min_location = min(map(lambda r: r.start, all_location_ranges))
    print(f"Min Location: {min_location}")
