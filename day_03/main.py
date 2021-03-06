def part_one(data):
    gamma_rate = ""

    for x in range(len(data[0])):
        all_bits = [line[x] for line in data]
        mcb = max(set(all_bits), key=all_bits.count)
        gamma_rate += mcb

    epsilon_rate = ''.join("1" if x == "0" else "0" for x in gamma_rate)

    gamma_rate = int(gamma_rate, 2)
    epsilon_rate = int(epsilon_rate, 2)
    power_consumption = gamma_rate * epsilon_rate
    print(power_consumption)


def filter(data, pos, ox=True):
    all_bits_in_pos_x = [line[pos] for line in data]
    num_ones = all_bits_in_pos_x.count("1")
    num_zeroes = all_bits_in_pos_x.count("0")

    num_to_keep = "0" if num_zeroes > num_ones else "1"
    if not ox: num_to_keep = "0" if num_to_keep == "1" else "1"

    data = [line for line in data if line[pos] == num_to_keep]

    return data


def calc_value(data, ox=True):
    for x in range(len(data[0])):
        data = filter(data, x, ox)
        if len(data) == 1:
            return data[0]


def part_two(data):
    oxygen_generator_rating = int(''.join(calc_value(data)), 2)
    c02_scrubber_rating = int(''.join(calc_value(data, False)), 2)

    life_support_rating = oxygen_generator_rating * c02_scrubber_rating
    print(life_support_rating)


f = open("input.txt")
data = [[c for c in line.strip()] for line in f]
f.close()

part_one(data)
part_two(data)