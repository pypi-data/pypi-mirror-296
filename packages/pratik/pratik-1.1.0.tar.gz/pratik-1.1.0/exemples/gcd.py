from pratik.functions import gcd


def basic_gcd_example():
    print("\n# Find the GCD of two simple numbers : (48, 18)")
    result = gcd(48, 18)
    print(f"Basic GCD: {result}")


def gcd_with_prime_numbers():
    print("\n# Find the GCD of two prime numbers : (17, 13)")
    result = gcd(17, 13)
    print(f"GCD of Prime Numbers: {result}")


def gcd_with_zero():
    print("\n# Handle GCD when one of the numbers is zero : (0, 34)")
    result = gcd(0, 34)
    print(f"GCD with Zero: {result}")


def large_numbers_gcd():
    print("\n# Find the GCD of two large numbers : (1234567890, 9876543210)")
    result = gcd(1234567890, 9876543210)
    print(f"GCD of Large Numbers: {result}")


def gcd_edge_case():
    print("\n# Handle an edge case where both numbers are the same : (42, 42)")
    result = gcd(42, 42)
    print(f"GCD of Identical Numbers: {result}")


if __name__ == "__main__":
    basic_gcd_example()
    gcd_with_prime_numbers()
    gcd_with_zero()
    large_numbers_gcd()
    gcd_edge_case()
