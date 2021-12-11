def part_one(syntax_lines):
    bracket_sets = {
        "(": ")",
        "[": "]",
        "{": "}",
        "<": ">"
    }

    points = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137
    }

    score = 0
    for line in syntax_lines:
        stack = []
        for c in line:
            if c in bracket_sets.keys():
                stack.append(c)
            elif c in bracket_sets.values():
                matching = stack.pop()
                if bracket_sets[matching] != c:
                    score += points[c]
                    continue

    return score


if __name__ == "__main__":
    f = open("input.txt")
    syntax_lines = [line.strip() for line in f]
    f.close()

    print(part_one(syntax_lines))