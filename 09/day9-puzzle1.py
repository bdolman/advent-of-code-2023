def calc_diffs(history):
    diffs = []
    for i in range(1,len(history)):
        diffs.append(history[i]-history[i-1])
    return diffs

def extrapolate_next_value(history):
    if all(map(lambda v: v == 0, history)):
        return 0
    diffs = calc_diffs(history)
    next_value = extrapolate_next_value(diffs)
    extrapolated_value = history[-1] + next_value
    return extrapolated_value


with open("09/day9-input.txt", "r", encoding="utf8") as file:
    histories = []
    for line in file:
        histories.append(list(map(int,line.split())))

    extrapolation_sum = 0
    for history in histories:
        extrapolated_value = extrapolate_next_value(history)
        print(f"Extrapolated value: {extrapolated_value}")
        extrapolation_sum += extrapolated_value

    print(f"Sum of extrapolated values: {extrapolation_sum}")
    