def find_min(a, length):
    m = a[0]
    for i in range(1, length):
        if a[i] < m:
            m = a[i]
    return m
