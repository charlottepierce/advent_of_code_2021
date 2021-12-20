import numpy as np


class Scanner(object):
    def __init__(self, number):
        self.beacons = []
        self.number = number
        self.position = [0, 0, 0]


class Transform(object):
    def __init__(self, from_scanner, to_scanner, dist, coord_position, facing):
        self.from_scanner = from_scanner
        self.to_scanner = to_scanner
        self.dist = dist
        self.coord_position = coord_position
        self.facing = facing


def find_transform(test_scanner, other_scanner):
    coord_positions = [
        [0, 1, 2],
        [0, 2, 1],
        [1, 0, 2],
        [1, 2, 0],
        [2, 1, 0],
        [2, 0, 1]
    ]
    facings = [
        [1, 1, 1],
        [1, 1, -1],
        [1, -1, 1],
        [1, -1, -1],
        [-1, 1, 1],
        [-1, 1, -1],
        [-1, -1, 1],
        [-1, -1, -1]
    ]

    test_beacon_positions = [[b[0], b[1], b[2]] for b in test_scanner.beacons]
    for coord_position in coord_positions:
        for facing in facings:
            other_beacon_positions = []
            # transform beacon positions for other scanner to test position + facing
            for b in other_scanner.beacons:
                original_vec = [b[0], b[1], b[2]]
                vec = [original_vec[position] for position in coord_position]
                vec = [vec[i] * facing[i] for i in range(len(vec))]
                other_beacon_positions.append(vec)

            # compare all points in scanner 0 with all transformed points from other scanner
            # calculate distance between two points, see if applying that distance vector to all points
            # from s2 makes 12 or more positions identical to those in s1
            for p1 in test_beacon_positions:
                for p2 in other_beacon_positions:
                    test_dist = np.array(p1) - np.array(p2)
                    resulting_s2_beacon_positions = [
                        (np.array([position[0], position[1], position[2]]) + test_dist).tolist() for position in
                        other_beacon_positions]
                    overlap = len([v for v in resulting_s2_beacon_positions if v in test_beacon_positions])
                    if overlap >= 12:
                        print("--- found transform from scanner", other_scanner.number, "to scanner", test_scanner.number)
                        return Transform(other_scanner, test_scanner, test_dist, coord_position, facing)
    return None


def solve(scanners):
    non_matched_beacons = []
    for i in range(1, len(scanners)):
        non_matched_beacons.extend(scanners[i].beacons)
    while len(non_matched_beacons) > 0:
        for i in range(0, 1):
            test_scanner = scanners[i]
            for ii in range(i, len(scanners)):
                if i == ii:
                    continue
                print("Trying to find transform from scanner scanner", scanners[ii].number, "to scanner", scanners[i].number)
                other_scanner = scanners[ii]
                t = find_transform(test_scanner, other_scanner)
                if t is not None:
                    other_scanner.position = transform_vector(other_scanner.position, t)
                    new_beacon_positions = apply_transform(other_scanner, t)
                    test_scanner.beacons.extend(new_beacon_positions)
                    other_scanner.beacons = []

        non_matched_beacons = []
        for i in range(1, len(scanners)):
            non_matched_beacons.extend(scanners[i].beacons)

    print(len(set([tuple(x) for x in scanners[0].beacons])), "unique beacons") # part 1 answer

    scanner_positions = [s.position for s in scanners]
    distances = []
    for p1 in scanner_positions:
        for p2 in scanner_positions:
            dist = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2])
            distances.append(dist)

    print("The largest distance between two scanners is:", max(distances)) # part 2 answer


def transform_vector(original_vec, transform):
    vec = [original_vec[position] for position in transform.coord_position]
    vec = [vec[i] * transform.facing[i] for i in range(len(vec))]
    vec = (np.array(vec) + np.array(transform.dist)).tolist()
    return vec


def apply_transform(scanner, transform):
    transformed_beacon_positions = []

    for b in scanner.beacons:
        original_vec = [b[0], b[1], b[2]]
        transformed_beacon_positions.append(transform_vector(original_vec, transform))

    return transformed_beacon_positions


if __name__ == "__main__":
    f = open("input.txt")

    scanners = []

    scanner_number = 0
    for line in f:
        if "---" in line:
            s = Scanner(scanner_number)
            next_line = f.readline().strip()
            while len(next_line) > 0:
                x, y, z = [int(v) for v in next_line.split(",")]
                s.beacons.append([x, y, z])
                next_line = f.readline().strip()
            scanners.append(s)
            scanner_number += 1

    f.close()

    scanners[0].coords = (0, 0, 0) # first scanner is at the origin

    solve(scanners)