def fibbonachi_array(n):
    arr = [1, 1]
    for _ in range(n - 2):
        arr.append(arr[-1] + arr[-2])
    return arr

print(fibbonachi_array(1))
print(fibbonachi_array(2))
