f = open("input.txt", "r")

win_size = 3
nums = [int(line.strip()) for line in f]

prev_win_sum = None
count = 0
for i in range(len(nums) - win_size + 1):
    win_sum = sum(nums[i:i+win_size])

    if prev_win_sum is not None:
        if win_sum > prev_win_sum:
            count += 1

    prev_win_sum = win_sum

print(count)

f.close()