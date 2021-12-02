horizontal = 0
depth = 0

f = open("input.txt")

for line in f:
    direction, amount = line.strip().split(" ")

    if direction == "forward":
        horizontal += int(amount)
    elif direction == "down":
        depth += int(amount)
    elif direction == "up":
        depth -= int(amount)

answer = horizontal * depth
print(answer)

f.close()