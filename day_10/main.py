import math

bracket_sets = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}

def part_two(syntax_lines):
    points = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4
    }

    scores = []

    for line in syntax_lines:
        score = 0
        stack = []
        for c in line:
            if c in bracket_sets.keys():
                stack.append(c)
            elif c in bracket_sets.values():
                stack.pop()

        while len(stack) > 0:
            needs_matching = stack.pop()
            score *= 5
            score += points[bracket_sets[needs_matching]]

        scores.append(score)

    scores = sorted(scores)
    return scores[math.floor(len(scores) / 2)]


def part_one(syntax_lines):
    points = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137
    }

    score = 0
    incomplete_lines = []
    for line in syntax_lines:
        stack = []
        corrupted = False
        for c in line:
            if c in bracket_sets.keys():
                stack.append(c)
            elif c in bracket_sets.values():
                matching = stack.pop()
                if bracket_sets[matching] != c:
                    score += points[c]
                    corrupted = True
                    break
        if not corrupted:
            incomplete_lines.append(line)

    return score, incomplete_lines


if __name__ == "__main__":
    f = open("input.txt")
    syntax_lines = [line.strip() for line in f]
    f.close()

    part_one_score, incomplete_lines = part_one(syntax_lines)
    print(part_one_score)
    print(part_two(incomplete_lines))