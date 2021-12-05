def points_on_line(startx, starty, endx, endy, diagonals=False):
    all_points = []
    if (startx != endx) and (starty != endy) and (not diagonals): return []

    x = min(startx, endx)
    while x <= max(startx, endx):
        y = min(starty, endy)
        while y <= max(starty, endy):
            all_points.append((x, y))
            y += 1
        x += 1
    return all_points


if __name__ == "__main__":
    f = open("input.txt")

    seen_points = []
    doubly_seen_points = []
    for line in f:
        print(line)
        points = line.strip().split(" -> ")
        startx, starty = [int(p) for p in points[0].split(",")]
        endx, endy = [int(p) for p in points[1].split(",")]
        for p in points_on_line(startx, starty, endx, endy):
            if p in seen_points and p not in doubly_seen_points:
                doubly_seen_points.append(p)
            else:
                seen_points.append(p)

    print(len(doubly_seen_points))

    f.close()