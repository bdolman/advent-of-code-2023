forward_word_dict = {
    'zero': "0",
    'one': "1",
    'two': "2",
    'three': "3",
    'four': "4",
    'five': "5",
    'six': "6",
    'seven': "7",
    'eight': "8",
    'nine': "9"
}

# Reverse all the keys in the forward dict so we can search a string in reverse
reverse_word_dict = dict(map(lambda kv: (kv[0][::-1], kv[1]), forward_word_dict.items()))

"""
Find a word digit (e.g. "one") and return string with the numeric digit (e.g. "1")
"""
def find_word_digit(string, word_dict):
    for word, digit in word_dict.items():
        if string.startswith(word):
            return digit
    return None

"""
Find the first digit in the string that is a digit (e.g. either "one" or "1")
"""
def find_first_digit_char(string, word_dict):
    for i, char in enumerate(string):
        if char.isdigit():
            return char 
        word_digit = find_word_digit(string[i::], word_dict)
        if word_digit:
            return word_digit
    return None

try:
    with open("day1-input.txt", "r", encoding="utf-8") as input_file:
        calibration_values = []
        for line in input_file:
            line = line.strip()
            first_digit = find_first_digit_char(line, forward_word_dict)
            last_digit = find_first_digit_char(line[::-1], reverse_word_dict)
            if first_digit is not None and last_digit is not None:
                value = int(f"{first_digit}{last_digit}")
                calibration_values.append(value)
            else:
                print(f"Skipping line doesn't contain digits: {line}")
        final_value = sum(calibration_values)
        print(f"Sum of calibration values: {final_value}")

except IOError as e:
    print(f"Error opening file: {e}")