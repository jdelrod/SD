# Exercise 3 Template

# Do not modify the file name or function header

# Returns a list with the prime numbers in the [a, b] interval
def prime(a, b):
    if type(a) is not int or type(b) is not int or a is None or b is None:
        raise TypeError

    primes = []

    if a == 1:
        primes.append(1)

    for n1 in range(a, (b + 1)):
        esprimo = 0
        for n2 in range(2, (n1 + 1)):
            if n1 % n2 == 0:
                esprimo += 1
        if esprimo == 1:
            primes.append(n1)

    return primes
