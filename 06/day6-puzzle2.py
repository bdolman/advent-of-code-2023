def calc_distances(race_time):
    distances = []
    for hold_time in range(race_time + 1):
        remaining_time = race_time - hold_time
        speed = hold_time
        distance = remaining_time * speed
        distances.append(distance)
    return distances


with open("06/day6-input.txt", "r", encoding="utf-8") as file:
    times = file.readline().split()[1:]
    record_distances = file.readline().split()[1:]
    total_time = int("".join(times))
    total_record_distance = int("".join(record_distances))

    distances = calc_distances(total_time)
    winning_condition = lambda d: d > total_record_distance
    winning_hold_times = [hold_time for (hold_time, dist) in enumerate(distances) if winning_condition(dist)]
    win_count = len(winning_hold_times)
    
    print(f"Time: {total_time} Record: {total_record_distance} Win Count: {win_count}")
