def part_one(height_map):
    low_points = []
    for row in range(len(height_map)):
        for col in range(len(height_map[0])):
            height = height_map[row][col]
            lowest_point = True
            # up
            if (row > 0) and (height_map[row-1][col] <= height):
                lowest_point = False
            # down
            if ((row + 1) < len(height_map)) and (height_map[row+1][col] <= height):
                lowest_point = False
            # left
            if (col > 0) and (height_map[row][col-1] <= height):
                lowest_point = False
            # right
            if ((col + 1) < len(height_map[0])) and (height_map[row][col+1] <= height):
                lowest_point = False

            if lowest_point:
                low_points.append(height)

    return sum([x + 1 for x in low_points])


if __name__ == "__main__":
    f = open("input.txt")
    height_map = []
    for line in f:
        heights = [int(x) for x in line.strip()]
        height_map.append(heights)
    f.close()

    print(part_one(height_map))