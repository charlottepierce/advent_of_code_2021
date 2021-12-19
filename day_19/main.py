import numpy as np


class Beacon(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "[" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + "]"


class Scanner(object):
    def __init__(self, number):
        self.beacons = []
        self.number = number


class Transform(object):
    def __init__(self, from_scanner, to_scanner, dist, coord_position, facing):
        self.from_scanner = from_scanner
        self.to_scanner = to_scanner
        self.dist = dist
        self.coord_position = coord_position
        self.facing = facing


def part_one(scanners):
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

    transforms = []

    for i in range(0, len(scanners)):
        test_scanner = scanners[i]
        test_beacon_positions = [[b.x, b.y, b.z] for b in test_scanner.beacons]
        for ii in range(i, len(scanners)):
            if i == ii:
                continue
            print("Comparing scanner", scanners[i].number, "with", scanners[ii].number)

            other_scanner = scanners[ii]
            for coord_position in coord_positions:
                # print("Using coord position", coord_position)
                for facing in facings:
                    # print("Using facing", facing)
                    other_beacon_positions = []
                    # transform beacon positions for other scanner to test position + facing
                    for b in other_scanner.beacons:
                        original_vec = [b.x, b.y, b.z]
                        vec = [original_vec[position] for position in coord_position]
                        vec = [vec[i] * facing[i] for i in range(len(vec))]
                        other_beacon_positions.append(vec)

                    # compare all points in scanner 0 with all transformed points from other scanner
                    # calculate distance between two points, see if applying that distance vector to all points
                    # from s2 makes 12 or more positions identical to those in s1
                    for p1 in test_beacon_positions:
                        for p2 in other_beacon_positions:
                            test_dist = np.array(p1) - np.array(p2)
                            resulting_s2_beacon_positions = [(np.array([position[0], position[1], position[2]]) + test_dist).tolist() for position in other_beacon_positions]
                            overlap = len([v for v in resulting_s2_beacon_positions if v in test_beacon_positions])
                            if overlap >= 12:
                                print("--- found transfer from scanner", scanners[ii].number, "to scanner", scanners[i].number)
                                transforms.append(Transform(other_scanner, test_scanner, test_dist, coord_position, facing))

    # apply transforms to get every scanner to the same coordinate system
    transformed_to_origin = []
    for i in range(1, len(scanners)):
        scanner_to_transform = scanners[i]
        print("Transforming scanner", scanner_to_transform.number)
        transformed_to = None
        while transformed_to != scanners[0]:
            transform_to_apply = [t for t in transforms if t.from_scanner == scanner_to_transform]
            if transformed_to is not None:
                transform_to_apply = [t for t in transforms if t.from_scanner == transformed_to]
            if len(transform_to_apply) == 0:
                print("no appropriate transform found")
                break
            transform_to_apply = transform_to_apply[0]
            print("transforming from", transform_to_apply.from_scanner.number, "to", transform_to_apply.to_scanner.number)
            new_beacon_positions = apply_transform(scanner_to_transform, transform_to_apply)
            scanner_to_transform.beacons = [Beacon(new_b[0], new_b[1], new_b[2]) for new_b in new_beacon_positions]
            transformed_to = transform_to_apply.to_scanner
            if transformed_to == scanners[0]:
                transformed_to_origin.append(scanner_to_transform)

    for s in transformed_to_origin:
        scanners[0].beacons.extend(s.beacons)
        scanners.remove(s)

    print("!!! Got", len(scanners), "scanner(s) left now")
    if len(scanners) > 1:
        part_one(scanners)

    unique_beacon_positions = []
    for scanner in scanners:
        for b in scanner.beacons:
            p = [b.x, b.y, b.z]
            if p not in unique_beacon_positions:
                unique_beacon_positions.append(p)

    print(len(unique_beacon_positions))


def apply_transform(scanner, transform):
    transformed_beacon_positions = []

    for b in scanner.beacons:
        original_vec = [b.x, b.y, b.z]
        vec = [original_vec[position] for position in transform.coord_position]
        vec = [vec[i] * transform.facing[i] for i in range(len(vec))]
        vec = (np.array(vec) + np.array(transform.dist)).tolist()
        transformed_beacon_positions.append(vec)

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
                s.beacons.append(Beacon(x, y, z))
                next_line = f.readline().strip()
            scanners.append(s)
            scanner_number += 1

    f.close()

    scanners[0].coords = (0, 0, 0) # first scanner is at the origin

    part_one(scanners)