import numpy as np
from scipy.spatial.transform import Rotation as R

class Beacon(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "{" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + "}"


class Scanner(object):
    def __init__(self):
        self.beacons = []
        self.coords = None


# def part_one(scanners):
#     scanner_0_beacons = [[b.x, b.y, b.z] for b in scanners[0].beacons]
#
#     coord_positions = [
#         [0, 1, 2],
#         [0, 2, 1],
#         [1, 0, 2],
#         [1, 2, 0],
#         [2, 1, 0],
#         [2, 0, 1]
#     ]
#     facings = [
#         [1, 1, 1],
#         [1, 1, -1],
#         [1, -1, 1],
#         [1, -1, -1],
#         [-1, 1, 1],
#         [-1, 1, -1],
#         [-1, -1, 1],
#         [-1, -1, -1]
#     ]
#
#     for i in range(1, len(scanners)):
#         print("Scanner", i)
#         for coord_position in coord_positions:
#             print("- Position", coord_position)
#             for facing in facings:
#                 print("- Facing", facing)
#                 set_of_beacon_positions = []
#                 for b in scanners[i].beacons:
#                     original_vec = [b.x, b.y, b.z]
#                     print("- Original", original_vec)
#                     vec = [original_vec[position] for position in coord_position]
#                     vec = [vec[i] * facing[i] for i in range(len(vec))]
#                     set_of_beacon_positions.append(vec)

def manhattan(b1, b2):
    return abs(b1.x - b2.x) + abs(b1.y - b2.y) + abs(b1.z - b2.z)


def part_one(scanners):
    s0_distances = {}
    for b in scanners[0].beacons:
        s0_distances[b] = [manhattan(b, b2) for b2 in scanners[0].beacons]

    s1_distances = {}
    for b in scanners[1].beacons:
        s1_distances[b] = [manhattan(b, b2) for b2 in scanners[1].beacons]

    for s0 in s0_distances.keys():
        for s1 in s1_distances.keys():
            overlap = list(set(s0_distances[s0]) & set(s1_distances[s1]))
            if len(overlap) >= 12:
                print("WHAT")


if __name__ == "__main__":
    f = open("input.txt")

    scanners = []

    for line in f:
        if "---" in line:
            s = Scanner()
            next_line = f.readline().strip()
            while len(next_line) > 0:
                x, y, z = [int(v) for v in next_line.split(",")]
                s.beacons.append(Beacon(x, y, z))
                next_line = f.readline().strip()
            scanners.append(s)

    f.close()

    scanners[0].coords = (0, 0, 0) # first scanner is at the origin

    part_one(scanners)