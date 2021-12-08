class DisplaySegment(object):
    def __init__(self):
        self.val = None # change when we figure it out
        self.possible_vals = []

    def __eq__(self, other):
        return (self.val == other.val) and (self.possible_vals == other.possible_vals)


def part_two(data):
    total_val = 0
    for signals, output_vals in data:
        # set up data holders
        top_segment = DisplaySegment()
        top_left_segment = DisplaySegment()
        top_right_segment = DisplaySegment()
        middle_segment = DisplaySegment()
        bottom_left_segment = DisplaySegment()
        bottom_right_segment = DisplaySegment()
        bottom_segment = DisplaySegment()

        # process signals
        signals = sorted(signals, key=len)
        # first element has two vals, thus forms a 1, has to correspond to RHS segments
        top_right_segment.possible_vals = [x for x in signals[0]]
        bottom_right_segment.possible_vals = [x for x in signals[0]]
        # second element has three vals, thus forms a 1. Whatever is not in the RHS segments has to be the val for the top segment
        seven_vals = [x for x in signals[1]]
        top_segment.val = [x for x in seven_vals if x not in top_right_segment.possible_vals][0]
        # third element has 4 vals, thus forms a 4. Whatever is not in the RHS segment has to be the vals for the top left and middle segments
        four_vals = [x for x in signals[2]]
        top_left_segment.possible_vals = [x for x in four_vals if x not in top_right_segment.possible_vals]
        middle_segment.possible_vals = [x for x in four_vals if x not in top_right_segment.possible_vals]
        # 10th element has 7 vals, thus forms an 8. Whatever is not already used in the other segments has to be the vals for the bottom left and bottom segments
        eight_vals = [x for x in signals[9]]
        bottom_left_segment.possible_vals = [x for x in eight_vals if x not in top_right_segment.possible_vals and x != top_segment.val and x not in top_left_segment.possible_vals]
        bottom_segment.possible_vals = [x for x in eight_vals if x not in top_right_segment.possible_vals and x != top_segment.val and x not in top_left_segment.possible_vals]
        # the only element with 5 vals, two of which are the RHS segments must form a 3.
        five_segment_signals = [x for x in signals if len(x) == 5]
        for s in five_segment_signals:
            vals = [v for v in s]
            if len(set(vals).intersection(set(top_right_segment.possible_vals))) == 2:
                # remove elements that must go in other segments
                vals.remove(top_segment.val)
                for v in top_right_segment.possible_vals:
                    vals.remove(v)
                # the two elements left cover the middle and bottom segments, figure out which goes where based on already known possible vals
                # then if you know the middle segment val you know the top left segment val
                # then if you know the bottom segment val you know the bottom left segment val
                for v in vals:
                    if v in middle_segment.possible_vals:
                        middle_segment.val = v
                        middle_segment.possible_vals = []
                        top_left_segment.val = [x for x in top_left_segment.possible_vals if x != v][0]
                        top_left_segment.possible_vals = []
                    elif v in bottom_segment.possible_vals:
                        bottom_segment.val = v
                        bottom_segment.possible_vals = []
                        bottom_left_segment.val = [x for x in bottom_left_segment.possible_vals if x != v][0]
                        bottom_left_segment.possible_vals = []
                five_segment_signals.remove(s) # remove this set of signals because we've used all we can from it
                break # we found the one that helps us with this step, move on to the next step
        # whichever of the remaining five segment signals has the bottom left segment must have the top right
        # whichever has the top left segment must have the bottom right
        for s in five_segment_signals:
            vals = [v for v in s]
            if bottom_left_segment.val in vals:
                vals.remove(bottom_left_segment.val)
                vals.remove(top_segment.val)
                vals.remove(middle_segment.val)
                vals.remove(bottom_segment.val)
                top_right_segment.val = vals[0]
                top_right_segment.possible_vals = []
            elif top_left_segment.val in vals:
                vals.remove(top_left_segment.val)
                vals.remove(top_segment.val)
                vals.remove(middle_segment.val)
                vals.remove(bottom_segment.val)
                bottom_right_segment.val = vals[0]
                bottom_right_segment.possible_vals = []

        # map output values
        zero_sequence = "".join(sorted([top_segment.val, top_right_segment.val, top_left_segment.val, bottom_left_segment.val, bottom_right_segment.val, bottom_segment.val]))
        one_sequence = "".join(sorted([top_right_segment.val, bottom_right_segment.val]))
        two_sequence = "".join(sorted([top_segment.val, top_right_segment.val, middle_segment.val, bottom_left_segment.val, bottom_segment.val]))
        three_sequence = "".join(sorted([top_segment.val, top_right_segment.val, bottom_right_segment.val, middle_segment.val, bottom_segment.val]))
        four_sequence = "".join(sorted([top_left_segment.val, middle_segment.val, top_right_segment.val, bottom_right_segment.val]))
        five_sequence = "".join(sorted([top_segment.val, top_left_segment.val, middle_segment.val, bottom_right_segment.val, bottom_segment.val]))
        six_sequence = "".join(sorted([top_left_segment.val, bottom_left_segment.val, middle_segment.val, bottom_right_segment.val, bottom_segment.val, top_segment.val]))
        seven_sequence = "".join(sorted([top_segment.val, top_right_segment.val, bottom_right_segment.val]))
        eight_sequence = "".join(sorted([top_segment.val, top_left_segment.val, top_right_segment.val, middle_segment.val, bottom_left_segment.val, bottom_right_segment.val, bottom_segment.val]))
        nine_sequence = "".join(sorted([top_segment.val, top_left_segment.val, top_right_segment.val, middle_segment.val, bottom_right_segment.val, bottom_segment.val]))
        number_mappings = {
            zero_sequence: "0",
            one_sequence: "1",
            two_sequence: "2",
            three_sequence: "3",
            four_sequence: "4",
            five_sequence: "5",
            six_sequence: "6",
            seven_sequence: "7",
            eight_sequence: "8",
            nine_sequence: "9"
        }

        signal_val = int("".join([number_mappings["".join(sorted(output_val))] for output_val in output_vals]))
        total_val += signal_val

    return total_val


def part_one(data):
    unique_lengths = [2, 4, 3, 7] # number of signals to render the numbers 1, 4, 7, 8

    all_outputs = []
    for sub_list in [d[1] for d in data]:
        all_outputs.extend(sub_list)

    count = 0
    for output in all_outputs:
        if len(output) in unique_lengths:
            count += 1

    return count


if __name__ == "__main__":
    f = open("input.txt")
    data = []
    for line in f:
        signals, outputs = line.strip().split("|")
        signals = [x for x in signals.strip().split()]
        outputs = [x for x in outputs.strip().split()]
        data.append((signals, outputs))

    f.close()

    print(part_one(data))
    print(part_two(data))