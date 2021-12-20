def print_image(image_data):
    for row in image_data:
        print("".join([v for v in row]))
    print()


def add_border(image_data, border_char):
    bordered_data = []
    # above
    bordered_data.append([border_char] * (len(image_data[0]) + 2))
    # left and right
    for row in image_data:
        new_row = [border_char]
        new_row.extend([x for x in row])
        new_row.append(border_char)
        bordered_data.append(new_row)
    # below
    bordered_data.append([border_char] * (len(image_data[0]) + 2))

    return bordered_data


def enhance(enhacement_algorithm, image_data, buffer_char):
    max_row = len(image_data)
    max_col = len(image_data[0])

    enhanced_image_data = []
    for row_num in range(len(image_data)):
        new_row = []
        for col_num in range(len(image_data[0])):
            square_vals = []
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    square_row = row_num + dx
                    square_col = col_num + dy
                    if 0 <= square_row < max_row and 0 <= square_col < max_col:
                        square_vals.append(image_data[square_row][square_col])
                    else:
                        square_vals.append(buffer_char)
            square_vals = ["1" if v == "#" else "0" for v in square_vals]
            square_bin = "".join(square_vals)
            square_dec = int(square_bin, base=2)
            new_middle_val = enhacement_algorithm[square_dec]
            new_row.append(new_middle_val)
        enhanced_image_data.append(new_row)

    return enhanced_image_data


def num_lights(image_data):
    count = 0
    for row in image_data:
        count += row.count("#")
    return count


def run(enhancement_algorithm, image_data, steps):
    buffer_char = '.'
    image_data = add_border(image_data, buffer_char)
    for x in range(steps):
        image_data = enhance(enhancement_algorithm, image_data, buffer_char)

        # update buffer character
        buffer_char_square = [buffer_char] * 9
        buffer_char_idx = int("".join(["1" if v == "#" else "0" for v in buffer_char_square]), base=2)
        buffer_char = enhancement_algorithm[buffer_char_idx]

        # add new border
        image_data = add_border(image_data, buffer_char)

    print(num_lights(image_data), "lights")


if __name__ == "__main__":
    f = open("input.txt")

    enhacement_algorithm = [c for c in f.readline().strip()]
    image_data = []
    for line in f:
        if len(line.strip()) > 0:
            image_data.append([c for c in line.strip()])
    f.close()

    run(enhacement_algorithm, image_data, 2)  # part 1
    run(enhacement_algorithm, image_data, 50)  # part 2
