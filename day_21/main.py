import functools

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


@functools.lru_cache(maxsize=None)
def play_part_two(curr_turn_pos, other_pos, curr_turn_score, other_score):
    # possible totals of rolling the die 3 times
    possible_die_totals = []
    for d1 in [1, 2, 3]:
        for d2 in [1, 2, 3]:
            for d3 in [1, 2, 3]:
                possible_die_totals.append(d1 + d2 + d3)

    if curr_turn_score >= 21:
        return 1, 0
    if other_score >= 21:
        return 0, 1

    curr_turn_win_count = 0
    other_win_count = 0

    for die_total in possible_die_totals:
        new_pos = curr_turn_pos + die_total
        while new_pos > 10:
            new_pos -= 10
        new_score = curr_turn_score + new_pos

        other_player_win, curr_player_win = play_part_two(other_pos, new_pos, other_score, new_score)

        curr_turn_win_count += curr_player_win
        other_win_count += other_player_win

    return curr_turn_win_count, other_win_count


def part_two(p1_pos, p2_pos):
    p1_wins, p2_wins = play_part_two(p1_pos, p2_pos, 0, 0)
    print(max(p1_wins, p2_wins))


if __name__ == "__main__":
    f = open("input.txt")

    p1_pos = int(f.readline().split(":")[1].strip())
    p2_pos = int(f.readline().split(":")[1].strip())

    f.close()

    part_one(p1_pos, p2_pos)
    part_two(p1_pos, p2_pos)
