import re

symbol_pattern = re.compile(r"[^\d.]+")
gear_pattern = re.compile(r"[*]")
part_pattern = re.compile(r"[\d]+")

def ranges_overlap(range1, range2):
    start1, end1 = range1
    start2, end2 = range2
    return start1 < end2 and start2 < end1

def calc_gear_ratio(match, lines):
    start = max(match.start() - 1, 0)
    end = match.end()+1

    parts = []
    for line in lines:
        for part in part_pattern.finditer(line):
            if ranges_overlap((start, end), (part.start(), part.end())):
                parts.append(int(part.group()))
    if len(parts) == 2:
        print(f"Parts: {parts}")
        return parts[0] * parts[1]
    
    return 0

with open("03/day3-input.txt", "r", encoding="utf-8") as file:
    dataset = []
    for line in file:
        dataset.append(line.strip())

    gear_ratio_sum = 0
    for line_index in range(len(dataset)):
        prev = dataset[line_index - 1] if line_index > 0 else None
        curr = dataset[line_index]
        next = dataset[line_index + 1] if line_index < len(dataset) - 1 else None

        matches = gear_pattern.finditer(curr)
        for match in matches:
            adjacent_lines = [item for item in [prev, curr, next] if item is not None]
            gear_ratio = calc_gear_ratio(match, adjacent_lines)
            gear_ratio_sum += gear_ratio

    print(f"Gear ratio sum: {gear_ratio_sum}")



