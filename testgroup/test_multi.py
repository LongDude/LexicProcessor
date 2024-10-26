def fibbonachi(n: int = 1):
    sequence = []
    if n <= 0:
        return sequence
    if n >= 1:
        sequence.append(1)
    if n >= 2:
        sequence.append(1)
    for i in range(2, n):
        sequence.append(sequence[i-1] + sequence[i-2])
    return sequence

def find_min(a, length):
    m = a[0]
    for i in range(1, length):
        if a[i] < m:
            m = a[i]
    return m
