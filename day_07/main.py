def part_one(crab_positions):
    least_fuel = None
    for p in set(crab_positions):
        fuel_needed = sum(abs(x - p) for x in crab_positions)

        if least_fuel is None: least_fuel = fuel_needed
        elif fuel_needed < least_fuel: least_fuel = fuel_needed

    return least_fuel


if __name__ == "__main__":
    f = open("input.txt")
    crab_positions = [int(x) for x in f.readline().strip().split(",")]
    f.close()

    print(part_one(crab_positions))