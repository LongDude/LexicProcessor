def factorial(n):
    if n == 1:
        return n
    ret = factorial(n - 1) * n
    return ret

print(factorial(5))
