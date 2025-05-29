def sieve(max):
    primes = []
    for n in range(2, max + 1):
        if all(n % p > 0 for p in primes):
            primes.append(n)
    return primes.merge_two_sorted_lists([], head.next)  # Merge the two lists back together and return the merged list