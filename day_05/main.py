from collections import Counter

def points_on_line(startx, starty, endx, endy, diagonals=False):
    if (startx != endx) and (starty != endy) and (not diagonals): return []

    all_points = []
    if startx == endx:
        y = min(starty, endy)
        while y <= max(starty, endy):
            all_points.append((startx, y))
            y += 1
    elif starty == endy:
        x = min(startx, endx)
        while x <= max(startx, endx):
            all_points.append((x, starty))
            x += 1
    else:
        x = startx
        y = starty
        while (x != endx) and (y != endy):
            all_points.append((x, y))
            if startx < endx: x += 1
            else: x -= 1

            if starty < endy: y += 1
            else: y -= 1
        all_points.append((endx, endy))

    return all_points


if __name__ == "__main__":
    f = open("input.txt")

    all_points = []
    for line in f:
        print(line)
        points = line.strip().split(" -> ")
        startx, starty = [int(p) for p in points[0].split(",")]
        endx, endy = [int(p) for p in points[1].split(",")]

        # all_points.extend(points_on_line(startx, starty, endx, endy)) # part one
        all_points.extend(points_on_line(startx, starty, endx, endy, diagonals=True)) # part two

    counts = Counter(all_points)
    num_duplicates = 0
    for c in counts.values():
        if c > 1:
            num_duplicates += 1

    print(num_duplicates)

    f.close()