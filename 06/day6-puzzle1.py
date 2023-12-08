def calc_distances(race_time):
    distances = []
    for hold_time in range(race_time + 1):
        remaining_time = race_time - hold_time
        speed = hold_time
        distance = remaining_time * speed
        distances.append(distance)
    return distances


with open("06/day6-input.txt", "r", encoding="utf-8") as file:
    times = list(map(int, file.readline().split()[1:]))
    record_distances = list(map(int, file.readline().split()[1:]))


win_count_product = 1
for time, record_distance in zip(times, record_distances):
    distances = calc_distances(time)
    winning_condition = lambda d: d > record_distance
    winning_hold_times = [hold_time for (hold_time, dist) in enumerate(distances) if winning_condition(dist)]
    win_count = len(winning_hold_times)
    win_count_product *= win_count

    print(f"Time: {time} Winning count product: {win_count_product}")