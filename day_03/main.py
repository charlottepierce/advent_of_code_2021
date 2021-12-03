def part_one(data):

    gamma_rate = ""

    for x in range(len(data[0])):
        all_bits = [line[x] for line in data]
        mcb = max(set(all_bits), key=all_bits.count)
        gamma_rate += mcb

    epsilon_rate = ''.join("1" if x == "0" else "0" for x in gamma_rate)

    gamma_rate = int(gamma_rate, 2)
    epsilon_rate = int(epsilon_rate, 2)
    print(gamma_rate)
    print(epsilon_rate)

    power_consumption = gamma_rate * epsilon_rate
    print(power_consumption)


f = open("input.txt")
data = [[c for c in line.strip()] for line in f]
f.close()

part_one(data)