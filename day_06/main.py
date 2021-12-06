f = open("input.txt")

def part_one(fish_values, num_days):
    for i in range(num_days):
        print("Day", i)
        new_values = []
        for v in fish_values:
            new_val = v - 1
            if new_val >= 0:
                new_values.append(new_val)
            elif new_val == -1:
                new_values.append(6)
                new_values.append(8)
        fish_values = new_values

    return len(new_values)


starting_values = [int(v) for v in f.readline().strip().split(",")]

print(part_one(starting_values, 80))

f.close()