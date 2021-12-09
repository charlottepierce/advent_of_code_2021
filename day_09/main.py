def is_low_point(row, col, height_map):
    height = height_map[row][col]
    lowest_point = True
    # up
    if (row > 0) and (height_map[row - 1][col] <= height):
        lowest_point = False
    # down
    if ((row + 1) < len(height_map)) and (height_map[row + 1][col] <= height):
        lowest_point = False
    # left
    if (col > 0) and (height_map[row][col - 1] <= height):
        lowest_point = False
    # right
    if ((col + 1) < len(height_map[0])) and (height_map[row][col + 1] <= height):
        lowest_point = False

    return lowest_point


def flood_fill(row, col, height_map, seen):
    if (row, col) in seen: return 0, seen
    if height_map[row][col] == 9: return 0, seen

    seen.append((row, col))
    size = 1
    # up
    if row > 0:
        additional_size, seen = flood_fill(row - 1, col, height_map, seen)
        size += additional_size
    # down
    if (row + 1) < len(height_map):
        additional_size, seen = flood_fill(row + 1, col, height_map, seen)
        size += additional_size
    # left
    if (col > 0):
        additional_size, seen = flood_fill(row, col - 1, height_map, seen)
        size += additional_size
    # right
    if (col + 1) < len(height_map[0]):
        additional_size, seen = flood_fill(row, col + 1, height_map, seen)
        size += additional_size

    return size, seen


def part_two(height_map):
    basin_sizes = []

    seen = []
    for row in range(len(height_map)):
        for col in range(len(height_map[0])):
            if is_low_point(row, col, height_map):
                basin_size, seen = flood_fill(row, col, height_map, seen)
                basin_sizes.append(basin_size)

    three_largest_basin_sizes = sorted(basin_sizes)[-3:]
    result = 1
    for x in three_largest_basin_sizes:
        result *= x
    return result


def part_one(height_map):
    low_points = []
    for row in range(len(height_map)):
        for col in range(len(height_map[0])):
            if is_low_point(row, col, height_map):
                low_points.append(height_map[row][col])

    return sum([x + 1 for x in low_points])


if __name__ == "__main__":
    f = open("input.txt")
    height_map = []
    for line in f:
        heights = [int(x) for x in line.strip()]
        height_map.append(heights)
    f.close()

    # print(part_one(height_map))
    print(part_two(height_map))