f = open("input.txt", "r")

prev = None
count = 0
for line in f:
    num = int(line.strip())

    if prev is not None:
        if num > prev:
            count += 1

    prev = num

print(count)

f.close()