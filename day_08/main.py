def part_one(data):
    unique_lengths = [2, 4, 3, 7] # number of signals to render the numbers 1, 4, 7, 8

    all_outputs = []
    for sub_list in [d[1] for d in data]:
        all_outputs.extend(sub_list)

    count = 0
    for output in all_outputs:
        if len(output) in unique_lengths:
            count += 1

    return count


if __name__ == "__main__":
    f = open("input.txt")
    data = []
    for line in f:
        signals, outputs = line.strip().split("|")
        signals = [x for x in signals.strip().split()]
        outputs = [x for x in outputs.strip().split()]
        data.append((signals, outputs))

    f.close()

    print(part_one(data))