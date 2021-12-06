f = open("input.txt")


def run_sim(fish_values, num_days):
    counts = {}
    for x in range(-1, 9, 1):
        counts[x] = fish_values.count(x)

    for i in range(num_days):
        print("Day", i)
        new_counts = counts
        for x in range(-1, 8, 1):
            new_counts[x] = new_counts[x + 1]
        new_counts[6] += new_counts[-1]
        new_counts[8] = new_counts[-1]
        new_counts[-1] = 0

    return sum([v for v in counts.values()])


starting_values = [int(v) for v in f.readline().strip().split(",")]

print(run_sim(starting_values, 80))  # part 1
print(run_sim(starting_values, 256))  # part 2

f.close()