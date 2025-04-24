## Implements a fast prime factorization algorithm
## based on the sieve method.

def prime_candidates(n):
    """
    sequence of prime number candidates
    :param n: number being tested for primality, which sets bound on prime candidates
    :return: sequence of integers not divisible by 2,3,5, or 7 or 11
    """
    #first_primes = [2,3,5]
    #next_primes = [7,11,13,17,19,23,29,31]
    first_primes = [2, 3, 5, 7]
    next_primes = [11, 13, 17, 19, 23, 29, 31, 37,
                   41, 43, 47, 53, 59, 61, 67, 71,
                   73, 79, 83, 89, 97, 101, 103, 107,
                   109, 113, 121, 127, 131, 137, 139, 143,
                   149, 151, 157, 163, 167, 169, 173, 179,
                   181, 187, 191, 193, 197, 199, 209, 211]  ## 221, 223, 227, 229, ... (add 210)

    p = 1
    for x in first_primes:
        if (x*x > n):
            return
        p = p * x
        yield x
    offset = 0
    while True:
        for x in next_primes:
            r = x + offset
            if (r*r > n):
                return
            if r % 11 or r == 11:
                yield r
        offset += p

def factorization(n):
    """
    prime factorization of n
    :param n: number to be factored
    :return: prime factorization of n as a list of (factor,power) tuples
    """
    for x in prime_candidates(n):
        #print(f"testing divisibility of {n} by {x}")
        if (n % x == 0):
            #print("it is divisible!")
            return [x] + factorization(n//x)
    return [n] ## n is prime

def is_relatively_prime(x,y):
    """
    relatively prime
    :param x: first number
    :param y: 2nd number
    :return: True if relatively prime, otherwise False
    """
    if (x==1) or (y==1) or (x==0):
        return False
    xf = set([k for k in factorization(x)])
    yf = set([k for k in factorization(y)])
    #print(xf)
    #print(yf)
    if xf.intersection(yf):
        return False
    return True
