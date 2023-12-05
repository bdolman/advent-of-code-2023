import re

symbol_pattern = re.compile(r"[^\d.]+")

def has_adjacent_symbol(match, lines):
    start = max(match.start() - 1, 0)
    end = match.end()+1

    for line in lines:
        if symbol_pattern.search(line[start:end]):
            return True
        
    return False

with open("03/day3-input.txt", "r", encoding="utf-8") as file:
    dataset = []
    for line in file:
        dataset.append(line.strip())
    
    pattern = re.compile(r"[\d]+")

    part_number_sum = 0
    for line_index in range(len(dataset)):
        prev = dataset[line_index - 1] if line_index > 0 else None
        curr = dataset[line_index]
        next = dataset[line_index + 1] if line_index < len(dataset) - 1 else None

        matches = pattern.finditer(curr)
        for match in matches:
            adjacent_lines = [item for item in [prev, curr, next] if item is not None]
            is_part = has_adjacent_symbol(match, adjacent_lines)
            if is_part:
                part_number = int(match.group())
                part_number_sum += part_number

    print(f"Part number sum: {part_number_sum}")



