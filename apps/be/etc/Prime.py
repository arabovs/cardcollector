def is_prime(n):
    for x in range(2,n-1):
        if n % x == 0:
            return False
    return True

def get_primes(n):
    result = []
    for x in range(1,n):
        if is_prime(x):
            result.append(x)
    return result
            
print(get_primes(100))
            