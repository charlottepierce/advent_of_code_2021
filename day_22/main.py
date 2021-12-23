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
    def __init__(self, xmin, xmax, ymin, ymax, zmin, zmax):
        self.dead = False
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
    cubes_on = []

    for instruction in instructions:
        instruction_cube = Cube(instruction.xmin, instruction.xmax, instruction.ymin, instruction.ymax, instruction.zmin, instruction.zmax)

        # if an existing cube is completely inside the new cube, remove the existing cube
        cubes_to_remove = []
        i = 0
        maxi = len(cubes_on)
        for c in cubes_on:
            i += 1
            if c.dead:
                continue
            print("- checking for enclosement of cube", i, "of", maxi, instruction)
            if c.inside(instruction_cube):
                c.dead = True

        # if any existing cubes intersect the new cube, split the existing cube into multiple,
        # which represent the original existing cube minus the intersection
        cubes_to_remove = []
        split_cubes = []
        i = 0
        maxi = len(cubes_on)
        for c in cubes_on:
            i += 1
            if c.dead:
                continue
            print("- checking for splits needed in cube", i, "of", maxi, instruction)
            intersect_cube = overlap(instruction_cube, c)
            if intersect_cube.volume() > 0:
                # an intersection was found - math from https://github.com/jkpr/advent-of-code-2021-kotlin/blob/master/src/day22/Day22.kt
                if c.xmin < intersect_cube.xmin:
                    split_cubes.append(Cube(c.xmin, intersect_cube.xmin - 1, c.ymin, c.ymax, c.zmin, c.zmax))
                    c.dead = True
                if c.xmax > intersect_cube.xmax:
                    split_cubes.append(Cube(intersect_cube.xmax + 1, c.xmax, c.ymin, c.ymax, c.zmin, c.zmax))
                    c.dead = True
                if c.ymin < intersect_cube.ymin:
                    split_cubes.append(Cube(intersect_cube.xmin, intersect_cube.xmax, c.ymin, intersect_cube.ymin - 1, c.zmin, c.zmax))
                    c.dead = True
                if c.ymax > intersect_cube.ymax:
                    split_cubes.append(Cube(intersect_cube.xmin, intersect_cube.xmax, intersect_cube.ymax + 1, c.ymax, c.zmin, c.zmax))
                    c.dead = True
                if c.zmin < intersect_cube.zmin:
                    split_cubes.append(Cube(intersect_cube.xmin, intersect_cube.xmax, intersect_cube.ymin, intersect_cube.ymax, c.zmin, intersect_cube.zmin - 1))
                    c.dead = True
                if c.zmax > intersect_cube.zmin:
                    split_cubes.append(Cube(intersect_cube.xmin, intersect_cube.xmax, intersect_cube.ymin, intersect_cube.ymax, intersect_cube.zmax + 1, c.zmax))
                    c.dead = True

        print("Adding split cubes...")
        cubes_on.extend(split_cubes)

        # add the instruction cube to the list of on cubes, if the instruction is to turn it on
        print("Adding instruction cube...")
        if instruction.on:
            cubes_on.append(instruction_cube)

    i = 0
    maxi = len(cubes_on)
    total_on = 0
    for c in cubes_on:
        i += 1
        print("- calculating final volume ...", i, "of", maxi)
        total_on += c.volume()
    print(total_on)


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
