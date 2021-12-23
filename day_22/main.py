class Instruction(object):
    def __init__(self, on, xmin, xmax, ymin, ymax, zmin, zmax):
        self.on = on
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax

    def __str__(self):
        s = "on "
        if not self.on:
            s = "off "
        s += "x=" + str(self.xmin) + ".." + str(self.xmax) + ","
        s += "y=" + str(self.ymin) + ".." + str(self.ymax) + ","
        s += "z=" + str(self.zmin) + ".." + str(self.zmax)
        return s


class Cube(object):
    def __init__(self, xmin, xmax, ymin, ymax, zmin, zmax, positive=True):
        self.positive = positive
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax

    def volume(self):
        x = abs(self.xmax - self.xmin) + 1
        y = abs(self.ymax - self.ymin) + 1
        z = abs(self.zmax - self.zmin) + 1
        if self.xmin < 0 < self.xmax:
            x += 1
        if self.ymin < 0 < self.ymax:
            y += 1
        if self.zmin < 0 < self.zmax:
            z += 1

        return x * y * z

    def inside(self, other):
        return self.xmin >= other.xmin and self.xmax <= other.xmax \
            and self.ymin >= other.ymin and self.ymax <= other.ymax \
            and self.zmin >= other.zmin and self.zmax <= other.zmax


def part_one(instructions):
    lights = [[[False for k in range(101)] for j in range(101)] for i in range(101)]
    for instruction in instructions:
        xmin = instruction.xmin if instruction.xmin >= -50 else -50
        xmax = instruction.xmax if instruction.xmax <= 50 else 50
        ymin = instruction.ymin if instruction.ymin >= -50 else -50
        ymax = instruction.ymax if instruction.ymax <= 50 else 50
        zmin = instruction.zmin if instruction.zmin >= -50 else -50
        zmax = instruction.zmax if instruction.zmax <= 50 else 50
        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                for z in range(zmin, zmax + 1):
                    xidx = x + 50
                    yidx = y + 50
                    zidx = z + 50
                    if 0 <= xidx <= 100 and 0 <= yidx <= 100 and 0 <= zidx <= 100:
                        if instruction.on:
                            lights[xidx][yidx][zidx] = True
                        else:
                            lights[xidx][yidx][zidx] = False

    true_count = 0
    for x in lights:
        for y in x:
            for z in y:
                if z is True:
                    true_count += 1
    print(true_count, "lights are on")


def overlap(cube_a, cube_b):
    # https://stackoverflow.com/questions/5556170/finding-shared-volume-of-two-overlapping-cuboids
    xmax = min(cube_b.xmax, cube_a.xmax)
    xmin = max(cube_b.xmin, cube_a.xmin)
    ymax = min(cube_b.ymax, cube_a.ymax)
    ymin = max(cube_b.ymin, cube_a.ymin)
    zmax = min(cube_b.zmax, cube_a.zmax)
    zmin = max(cube_b.zmin, cube_a.zmin)

    return Cube(xmin, xmax, ymin, ymax, zmin, zmax)


def part_two(instructions):
    boxes = []

    inst_i = 0
    max_inst_i = len(instructions)
    for instruction in instructions:
        inst_i += 1
        instruction_cube = Cube(instruction.xmin, instruction.xmax, instruction.ymin, instruction.ymax, instruction.zmin, instruction.zmax)

        to_add = []
        i = 0
        maxi = len(boxes)
        for b in boxes:
            i += 1
            print("-- checking intersections with box", i, "of", maxi, "( instruction", inst_i, "of", max_inst_i, ") --", instruction)
            intersecting_box = overlap(instruction_cube, b)
            if intersecting_box.volume() > 0:
                intersecting_box.positive = not b.positive
                to_add.append(intersecting_box)
        boxes.extend(to_add)

        if instruction.on:
            boxes.append(instruction_cube)

    sum = 0
    for b in boxes:
        if b.positive:
            sum += b.volume()
        else:
            sum -= b.volume()

    print(sum)


if __name__ == "__main__":
    f = open("input.txt")

    instructions = []
    for line in f:
        instruction_elements = line.split()
        on = True if instruction_elements[0] == "on" else False
        xyz_text = instruction_elements[1].split(",")
        xmin, xmax = [int(v) for v in xyz_text[0][2:].split("..")]
        ymin, ymax = [int(v) for v in xyz_text[1][2:].split("..")]
        zmin, zmax = [int(v) for v in xyz_text[2][2:].split("..")]
        instructions.append(Instruction(on, xmin, xmax, ymin, ymax, zmin, zmax))

    f.close()

    # part_one(instructions)
    part_two(instructions)
