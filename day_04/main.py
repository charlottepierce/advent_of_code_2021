class GridCell(object):
    def __init__(self, val):
        self.value = val
        self.marked = False

    def __str__(self):
        if self.marked: return "__" + str(self.value) + "__"
        else: return str(self.value)


class Grid(object):
    def __init__(self, data):
        self.grid_data = [[GridCell(element) for element in row] for row in data]

    def mark_off(self, value):
        for row in self.grid_data:
            for cell in row:
                if cell.value == value:
                    cell.marked = True

    def winner(self):
        # rows
        marked_vals = [val.marked for row in self.grid_data for val in row]
        if marked_vals.count(True) == len(marked_vals):
            return True
        # columns
        for x in range(len(self.grid_data[0])):
            column_vals = [row[x] for row in self.grid_data]
            marked_vals = [val.marked for val in column_vals]
            if marked_vals.count(True) == len(self.grid_data[0]):
                return True

    def sum_of_unmarked(self):
        return sum([int(val.value) for row in self.grid_data for val in row if not val.marked])

    def __str__(self):
        return str([[str(c) for c in row] for row in self.grid_data])


def part_one(all_grids, bingo_calls):
    for num in bingo_calls:
        for grid in all_grids:
            grid.mark_off(num)
            if grid.winner():
                return grid.sum_of_unmarked() * int(num)
    return "Aw shit."


if __name__ == '__main__':
    f = open("input.txt")

    bingo_calls = f.readline().strip().split(",")

    all_grid_data = [line.strip().split() for line in f if len(line.strip().split()) > 0]

    all_grids = []
    x = 0
    while x < len(all_grid_data):
        all_grids.append(Grid(all_grid_data[x:x + 5]))
        x += 5

    f.close()

    print(part_one(all_grids, bingo_calls))
