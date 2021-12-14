from copy import deepcopy

class Cave(object):
    def __init__(self, name):
        self.name = name
        self.connected_caves = []


def explore(current_node, path, seen):
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
        path_count += explore(connected, path[:], seen[:])

    return path_count


def part_one(start_cave):
    return explore(start_cave, [], [])
    # for x in paths:
    # print(paths)
    # print(paths)
#      1  procedure BFS(G, root) is
#  2      let Q be a queue
#  3      label root as explored
#  4      Q.enqueue(root)
#  5      while Q is not empty do
#  6          v := Q.dequeue()
#  7          if v is the goal then
#  8              return v
#  9          for all edges from v to w in G.adjacentEdges(v) do
# 10              if w is not labeled as explored then
# 11                  label w as explored
# 12                  Q.enqueue(w)

    # return len(paths)


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