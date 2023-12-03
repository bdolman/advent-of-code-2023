def find_first_digit_char(string):
    for char in string:
        if char.isdigit():
            return char
    return None

try:
    with open("day1-input.txt", "r", encoding="utf-8") as input_file:
        calibration_values = []
        for line in input_file:
            first_digit = find_first_digit_char(line)
            last_digit = find_first_digit_char(line[::-1])
            if first_digit is not None and last_digit is not None:
                value = int(f"{first_digit}{last_digit}")
                calibration_values.append(value)
            else:
                print(f"Skipping line doesn't contain digits: {line}")
        final_value = sum(calibration_values)
        print(f"Sum of calibration values: {final_value}")

except IOError as e:
    print(f"Error opening file: {e}")