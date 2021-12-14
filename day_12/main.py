class Cave(object):
    def __init__(self, name):
        self.name = name
        self.connected_caves = []


def explore_part_one(current_node, path, seen):
    path.append(current_node)
    if current_node.name == "start":
        seen.append(current_node)
    elif current_node.name == "end":
        return 1
    elif current_node.name.islower():
        seen.append(current_node)

    path_count = 0
    for connected in current_node.connected_caves:
        if connected in seen:
            continue
        path_count += explore_part_one(connected, path[:], seen[:])

    return path_count


def part_one(start_cave):
    return explore_part_one(start_cave, [], [])


def explore_part_two(current_node, path, seen, known_paths, used_double_visit=False):
    path.append(current_node)
    if current_node.name == "start":
        seen.append(current_node)
    elif current_node.name == "end":
        if path not in known_paths:
            known_paths.append(path)
        return known_paths
    elif current_node.name.islower():
        seen.append(current_node)

    for connected in current_node.connected_caves:
        if connected in seen:
            continue
        known_paths = explore_part_two(connected, path[:], seen[:], known_paths, used_double_visit)
        if current_node.name.islower() and current_node.name != "start" and current_node.name != "end" and not used_double_visit:
            known_paths = explore_part_two(connected, path[:], [c for c in seen if c != current_node], known_paths, used_double_visit=True)

    return known_paths


def part_two(start_cave):
    known_paths = explore_part_two(start_cave, [], [], [])
    return len(known_paths)


if __name__ == "__main__":
    f = open("input.txt")

    caves = {}
    for line in f:
        origin, dest = line.strip().split("-")

        origin_cave = caves[origin] if origin in caves.keys() else Cave(origin)
        dest_cave = caves[dest] if dest in caves.keys() else Cave(dest)

        if origin not in caves.keys():
            caves[origin] = origin_cave
        if dest not in caves.keys():
            caves[dest] = dest_cave

        origin_cave.connected_caves.append(dest_cave)
        dest_cave.connected_caves.append(origin_cave)

    f.close()

    start_cave = caves["start"]

    print(part_one(start_cave))
    print(part_two(start_cave))