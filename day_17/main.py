def position_in_target(probe_x, probe_y, target_x_min, target_x_max, target_y_min, target_y_max):
    return target_x_min <= probe_x <= target_x_max and target_y_min <= probe_y <= target_y_max


def position_past_target(probe_x, probe_y, target_x_max, target_y_min):
    return probe_x > target_x_max or probe_y < target_y_min


def step(probe_x, probe_y, velocity_x, velocity_y):
    new_probe_x = probe_x + velocity_x
    new_probe_y = probe_y + velocity_y

    new_velocity_x = 0
    if velocity_x > 0:
        new_velocity_x = velocity_x - 1
    elif velocity_x < 0:
        new_velocity_x = velocity_x + 1
    new_velocity_y = velocity_y - 1

    return new_probe_x, new_probe_y, new_velocity_x, new_velocity_y


def part_one(target_x_min, target_x_max, target_y_min, target_y_max):
    heights = {}

    for x in range(0, target_x_max):
        for y in range(0, abs(target_y_max - target_y_min) * 10):
            probe_x = 0
            probe_y = 0
            init_velocity_x = x
            init_velocity_y = y
            velocity_x = init_velocity_x
            velocity_y = init_velocity_y
            height = 0
            while not position_past_target(probe_x, probe_y, target_x_max, target_y_min) and not position_in_target(probe_x, probe_y, target_x_min, target_x_max, target_y_min, target_y_max):
                probe_x, probe_y, velocity_x, velocity_y = step(probe_x, probe_y, velocity_x, velocity_y)
                if probe_y > height:
                    height = probe_y

            if position_in_target(probe_x, probe_y, target_x_min, target_x_max, target_y_min, target_y_max):
                heights[(init_velocity_x, init_velocity_y)] = height

    heights = sorted(heights.items(), key=lambda x: x[1], reverse=True)
    return heights[0][1]


if __name__ == "__main__":
    f = open("input.txt")

    info = f.readline().strip()

    f.close()

    info = info.replace("target area: ", "")
    x_lims, y_lims = info.split(",")
    target_x_min, target_x_max = [int(v) for v in x_lims.strip()[2:].split("..")]
    target_y_min, target_y_max = [int(v) for v in y_lims.strip()[2:].split("..")]

    print(part_one(target_x_min, target_x_max, target_y_min, target_y_max))