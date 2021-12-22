def roll_deterministic_dice(dice_val):
    dice_val += 1
    if dice_val > 100:
        dice_val = 1
    return dice_val


def part_one(p1_starting_pos, p2_starting_pos):
    p1_pos = p1_starting_pos
    p1_score = 0

    p2_pos = p2_starting_pos
    p2_score = 0

    roll_count = 0
    dice_val = 0
    while p1_score < 1000 and p2_score < 1000:
        # p1 turn
        for _ in range(3):
            roll_count += 1
            dice_val = roll_deterministic_dice(dice_val)
            p1_pos += dice_val
            while p1_pos > 10:
                p1_pos -= 10
        p1_score += p1_pos
        if p1_score >= 1000:
            break

        # p2 turn
        for _ in range(3):
            roll_count += 1
            dice_val = roll_deterministic_dice(dice_val)
            p2_pos += dice_val
            while p2_pos > 10:
                p2_pos -= 10
        p2_score += p2_pos

    print(roll_count * min(p1_score, p2_score))


if __name__ == "__main__":
    f = open("input.txt")

    p1_pos = int(f.readline().split(":")[1].strip())
    p2_pos = int(f.readline().split(":")[1].strip())

    f.close()

    part_one(p1_pos, p2_pos)