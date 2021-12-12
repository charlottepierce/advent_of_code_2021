def print_state(octopi_states):
    for row in range(len(octopi_states)):
        for col in range(len(octopi_states[0])):
            print(octopi_states[row][col], end='')
        print()
    print()


def run_step(octopi_states):
    flashes = False
    # increment
    for row in range(len(octopi_states)):
        for col in range(len(octopi_states[0])):
            octopi_states[row][col] += 1
            if octopi_states[row][col] > 9:
                flashes = True

    # skip if there are no flashes to process
    if not flashes:
        return octopi_states, 0, False

    # process flashes
    flashed = []
    while flashes:
        flashes = False
        flashes_this_round = 0
        for row in range(len(octopi_states)):
            for col in range(len(octopi_states[0])):
                if octopi_states[row][col] > 9:
                    octopi_states[row][col] = 0
                    flashed.append((row, col))
                    flashes_this_round += 1
                    for x_change in [-1, 0, 1]:
                        for y_change in [-1, 0, 1]:
                            new_row = row + x_change
                            new_col = col + y_change

                            if 0 <= new_row < len(octopi_states) and 0 <= new_col < len(octopi_states[0]):
                                if (new_row, new_col) not in flashed and octopi_states[new_row][new_col] <= 9:
                                    octopi_states[new_row][new_col] += 1
                                    if octopi_states[new_row][new_col] > 9:
                                        flashes = True

    all_flashed_at_once = True
    for row in range(len(octopi_states)):
        for col in range(len(octopi_states[0])):
            if octopi_states[row][col] > 0:
                all_flashed_at_once = False

    return octopi_states, len(flashed), all_flashed_at_once


def part_two(octopi_states):
    step = 0
    all_flashed_at_once = False
    while not all_flashed_at_once:
        step += 1
        octopi_states, new_flashed, all_flashed_at_once = run_step(octopi_states)

    return step


def part_one(octopi_states):
    total_flashes = 0
    for step in range(100):
        octopi_states, new_flashes, all_flashed_at_once = run_step(octopi_states)
        total_flashes += new_flashes

    return total_flashes


if __name__ == "__main__":
    f = open("input.txt")

    octopi_states = []
    for line in f:
        octopi_states.append([int(c) for c in line.strip()])

    f.close()

    # print(part_one(octopi_states[:]))
    print(part_two(octopi_states[:]))