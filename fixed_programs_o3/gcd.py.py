def gcd(a, b):
    """Compute the Greatest Common Divisor (GCD) of two nonnegative integers using Euclid's algorithm."""
    # Base case: if second number is zero, return the first number
    if b == 0:
        return a
    # Recursive case: correctly swap arguments so that we compute gcd(b, a % b)
    return gcd(b, a % b)

