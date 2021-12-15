def manhattan_heuristic(a_node, goal_row, goal_col):
    return abs(goal_row - a_node[0]) + abs(goal_col - a_node[1])


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from.keys():
        current = came_from[current]
        path.insert(0, current)

    return path


def a_star(risk_map):
    goal_row = len(risk_map) - 1
    goal_col = len(risk_map[0]) - 1

    start = (0, 0)
    open_set = [start]
    came_from = {}
    g_scores = {start: 0}
    f_scores = {start: manhattan_heuristic(start, goal_row, goal_col)}

    while len(open_set) > 0:
        current = min(open_set, key=lambda x: f_scores[x])

        if current[0] == goal_row and current[1] == goal_col:
            return reconstruct_path(came_from, current)

        open_set.remove(current)

        row = current[0]
        col = current[1]
        neighbours = []
        # up
        if row > 0:
            neighbours.append((row - 1, col))
        # down
        if (row + 1) < len(risk_map):
            neighbours.append((row + 1, col))
        # left
        if col > 0:
            neighbours.append((row, col - 1))
        # right
        if (col + 1) < len(risk_map[0]):
            neighbours.append((row, col + 1))

        for neighbour in neighbours:
            risk_level = risk_map[neighbour[0]][neighbour[1]]
            tentative_g_score = g_scores[current] + risk_level
            if neighbour not in g_scores.keys() or tentative_g_score < g_scores[neighbour]:
                came_from[neighbour] = current
                g_scores[neighbour] = tentative_g_score
                f_scores[neighbour] = tentative_g_score + manhattan_heuristic(neighbour, goal_row, goal_col)
                if neighbour not in open_set:
                    open_set.append(neighbour)


def part_one(risk_map):
    path = a_star(risk_map)
    risks = [risk_map[p[0]][p[1]] for p in path]
    risks = risks[1:] # remove first because we consider that 0, not what is in the risk map
    return sum(risks)


if __name__ == "__main__":
    f = open("input.txt")
    risk_map = []
    for line in f:
        risk_map.append([int(c) for c in line.strip()])
    f.close()

    print(part_one(risk_map))