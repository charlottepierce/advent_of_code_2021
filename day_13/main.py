def execute_fold(grid, fold_instruction):
    fold_axis, fold_value = fold_instruction

    new_grid = []
    if fold_axis == "x":
        for row in grid:
            new_grid.append([row[i] for i in range(fold_value)])
        for row in range(len(grid)):
            for col in range(fold_value + 1, len(grid[0])):
                if grid[row][col] == "#":
                    new_col = abs((col - len(grid[0]) + 1))
                    new_grid[row][new_col] = "#"
    elif fold_axis == "y":
        for i in range(fold_value):
            new_grid.append(grid[i])
        for row in range(fold_value + 1, len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] == "#":
                    new_row = abs(row - len(grid) + 1)
                    new_grid[new_row][col] = "#"

    return new_grid


def dots_visible(grid):
    count = sum([row.count("#") for row in grid])
    return count


def part_one(grid, fold_instructions):
    grid = execute_fold(grid, fold_instructions[0])
    return dots_visible(grid)


if __name__ == "__main__":
    f = open("input.txt")

    dot_positions = []
    fold_instructions = []

    for line in f:
        if "," in line:
            x, y = line.strip().split(",")
            dot_positions.append((int(x), int(y)))
        elif "fold along" in line:
            pos, val = line.replace("fold along", "").strip().split("=")
            fold_instructions.append((pos, int(val)))

    f.close()

    max_x = max([p[0] for p in dot_positions])
    max_y = max([p[1] for p in dot_positions])

    grid = [["."] * (max_x + 1) for x in range(max_y + 1)]

    for row, col in dot_positions:
        grid[col][row] = "#"

    print(part_one(grid, fold_instructions))
