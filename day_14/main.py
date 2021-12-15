def run_step(template, insertion_rules):
    new_template = template[0]
    for i in range(len(template) - 1):
        pair = template[i:i+2]
        new_template += insertion_rules[pair] + pair[1]

    return new_template


def part_one(template, insertion_rules):
    for step in range(10):
        template = run_step(template, insertion_rules)

    elements = set([x for x in template])
    counts = {}
    for element in elements:
        counts[element] = template.count(element)

    counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    answer = counts[0][1] - counts[-1][1]
    return answer


if __name__ == "__main__":
    f = open("input.txt")

    template = f.readline().strip()

    insertion_rules = {}
    for line in f:
        if len(line.strip()) > 0:
            pair, inserted = [item.strip() for item in line.strip().split("->")]
            insertion_rules[pair] = inserted

    f.close()

    print(part_one(template, insertion_rules))