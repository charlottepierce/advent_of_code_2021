def enhance(enhacement_algorithm, image_data):
    pass


def part_one(enhacement_algorithm, image_data):
    pass


if __name__ == "__main__":
    f = open("input.txt")

    enhacement_algorithm = [c for c in f.readline().strip()]
    image_data = []
    for line in f:
        if len(line.strip()) > 0:
            image_data.append([c for c in line.strip()])
    f.close()

    part_one(enhacement_algorithm, image_data)