horizontal = 0
depth = 0
aim = 0

f = open("input.txt")

for line in f:
    direction, amount = line.strip().split(" ")

    if direction == "down":
        aim += int(amount)
    elif direction == "up":
        aim -= int(amount)
    elif direction == "forward":
        horizontal += int(amount)
        depth += aim * int(amount)

answer = horizontal * depth
print(answer)

f.close()