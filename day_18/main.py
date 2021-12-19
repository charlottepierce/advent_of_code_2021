import math
import re


class Node(object):
    def __init__(self):
        self.left_child = None
        self.right_child = None
        self.parent = None

    def __str__(self):
        return "[" + str(self.left_child) + "," + str(self.right_child) + "]"

    def magnitude(self):
        mag = None
        if isinstance(self.left_child, int):
            mag = 3 * self.left_child
        else:
            mag = 3 * self.left_child.magnitude()

        if isinstance(self.right_child, int):
            mag += 2 * self.right_child
        else:
            mag += 2 * self.right_child.magnitude()

        return mag


def read_number(text):
    number = ""
    while len(text) > 0 and text[0].isnumeric():
        number += text[0]
        text = text[1:]

    return int(number), text


def parse(text):
    root = Node()
    text = text[1:]  # remove opening left bracket
    text = text[:-1]  # remove closing left bracket

    curr_node = root
    while len(text) > 0:
        if text[0].isnumeric():
            if curr_node.left_child is None:
                curr_node.left_child, text = read_number(text)
            elif curr_node.right_child is None:
                curr_node.right_child, text = read_number(text)
        elif text[0] == "[":
            text = text[1:]
            child_node = Node()
            child_node.parent = curr_node
            if curr_node.left_child is None:
                curr_node.left_child = child_node
            elif curr_node.right_child is None:
                curr_node.right_child = child_node
            curr_node = child_node
        elif text[0] == ",":
            text = text[1:]
        elif text[0] == "]":
            text = text[1:]
            curr_node = curr_node.parent

    return root


def add(snail_num_one, snail_num_two):
    new_root = Node()

    new_root.left_child = snail_num_one
    snail_num_one.parent = new_root

    new_root.right_child = snail_num_two
    snail_num_two.parent = new_root

    return new_root


def split(snailfish_num):
    num_str = str(snailfish_num)

    all_numbers = []
    num_found = ""
    for i in range(len(num_str)):
        if num_str[i].isnumeric():
            num_found += num_str[i]
        else:
            if len(num_found) > 0:
                all_numbers.append(int(num_found))
            num_found = ""

    all_numbers = [x for x in all_numbers if x >= 10]
    if len(all_numbers) == 0:
        return None

    first_two_digit_num = all_numbers[0]
    replacement = "[" + str(math.floor(first_two_digit_num / 2)) + "," + str(math.ceil(first_two_digit_num / 2)) + "]"
    num_str = num_str.replace(str(first_two_digit_num), replacement, 1)
    return parse(num_str)


def explode(snailfish_num):
    # find value with depth of 4
    num_str = str(snailfish_num)
    open_brackets = 0
    found = ""
    start_recording = False
    for c in num_str:
        if c == "[":
            open_brackets += 1
            found = ""
        elif c == "]":
            open_brackets -= 1
            start_recording = False
            pattern = re.compile("^[0-9]*,[0-9]*$")
            if pattern.match(found):
                break
        elif c.isnumeric():
            start_recording = True

        if open_brackets > 4 and start_recording and c != "[":
            found += c

    if len(found) == 0:
        return None

    found += "]"
    found = "[" + found

    # process replacements
    found_index_start = num_str.index(found)
    found_index_end = found_index_start + len(found)
    before = num_str[0:found_index_start]
    after = num_str[found_index_end:]
    leftmost_num = ""
    leftmost_num_index = None
    for i in range(len(before) - 1, 0, -1):
        if before[i].isnumeric():
            leftmost_num_index = i
            leftmost_num += before[i]
        elif len(leftmost_num) > 0:
            break # finished reading the number, hit another bracket or comma
    leftmost_num = int(leftmost_num[::-1]) if len(leftmost_num) > 0 else leftmost_num

    rightmost_num = ""
    rightmost_num_index = None
    for i in range(len(after)):
        if after[i].isnumeric():
            if rightmost_num_index is None:
                rightmost_num_index = i
            rightmost_num += after[i]
        elif len(rightmost_num) > 0:
            break  # finished reading the number, hit another bracket or comma
    rightmost_num = int(rightmost_num) if len(rightmost_num) > 0 else rightmost_num

    if isinstance(leftmost_num, int):
        node_left_val = int(found.split(",")[0][1:])
        new_before = before[0:leftmost_num_index]
        new_before += str(node_left_val + leftmost_num)
        new_before += before[leftmost_num_index+len(str(leftmost_num)):]
        before = new_before

    if isinstance(rightmost_num, int):
        node_right_val = int(found.split(",")[1][:-1])
        new_after = after[0:rightmost_num_index]
        new_after += str(node_right_val + rightmost_num)
        new_after += after[rightmost_num_index+len(str(rightmost_num)):]
        after = new_after

    new_num_str = before + "0" + after
    return parse(new_num_str)


def reduce(snailfish_num):
    done = False
    while not done:
        new_num = explode(snailfish_num)
        if new_num is None:
            new_num = split(snailfish_num)
            if new_num is None:
                done = True
            else:
                snailfish_num = new_num
        else:
            snailfish_num = new_num

    return snailfish_num


def part_one(snail_numbers):
    snail_num = snail_numbers[0]
    for i in range(1, len(snail_numbers)):
        snail_num = add(snail_num, snail_numbers[i])
        snail_num = reduce(snail_num)

    return snail_num


if __name__ == "__main__":
    f = open("input.txt")
    number_text = [line.strip() for line in f]
    f.close()

    snail_numbers = []
    for text in number_text:
        snail_numbers.append(parse(text))

    print(part_one(snail_numbers).magnitude())