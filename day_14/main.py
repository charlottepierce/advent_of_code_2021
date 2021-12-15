import math


def run_step(pairs, insertion_rules):
    new_pairs = {}
    for p in pairs.keys():
        inserted = insertion_rules[p]
        new_pair1 = p[0] + inserted
        new_pair2 = inserted + p[1]

        new_pairs[new_pair1] = new_pairs.get(new_pair1, 0) + 1 * pairs[p]
        new_pairs[new_pair2] = new_pairs.get(new_pair2, 0) + 1 * pairs[p]

    return new_pairs


def run_logic(template, insertion_rules, num_steps):
    pair_counts = {}
    for i in range(len(template) - 1):
        pair = template[i:i+2]
        pair_counts[pair] = 1

    for step in range(num_steps):
        pair_counts = run_step(pair_counts, insertion_rules)

    element_counts = {}
    for pair in pair_counts.keys():
        element1, element2 = [c for c in pair]
        element_counts[element1] = element_counts.get(element1, 0) + pair_counts[pair]
        element_counts[element2] = element_counts.get(element2, 0) + pair_counts[pair]

    for element in element_counts.keys():
        element_counts[element] = math.floor(element_counts[element] / 2)

    element_counts[template[0]] += 1
    element_counts[template[-1]] += 1

    element_counts = sorted(element_counts.items(), key=lambda x: x[1], reverse=True)

    answer = element_counts[0][1] - element_counts[-1][1]
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

    # print(run_logic(template, insertion_rules, 10))
    print(run_logic(template, insertion_rules, 40))