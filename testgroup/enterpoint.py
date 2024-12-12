def fibbonachi(n: int = 1):
    sequence = []
    if n <= 0:
        return sequence
    if n >= 1:
        sequence.append(1)
    if n >= 2:
        sequence.append(1)
    for i in range(2, n):
        sequence.append(sequence[i - 1] + sequence[i - 2])
    return sequence

m = fibbonachi(7)
print(m)
