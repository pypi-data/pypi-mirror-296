from pratik.functions import humanize_number


def basic_humanize_example():
    # Format a simple large number
    print("\n# Format a simple large number")
    number = 1234567890
    formatted = humanize_number(number)
    print(f"Basic Humanized Number: {formatted}")


def custom_separator_example():
    # Use a custom separator
    print("\n# Use a custom separator")
    number = 9876543210
    formatted = humanize_number(number, '_')
    print(f"Custom Separator: {formatted}")


def small_number_example():
    # Handle a small number
    print("\n# Handle a small number")
    number = 123
    formatted = humanize_number(number)
    print(f"Small Number: {formatted}")


def large_number_example():
    # Handle a very large number
    print("\n# Handle a very large number")
    number = 987654321098765432109876543210
    formatted = humanize_number(number)
    print(f"Large Number: {formatted}")


def edge_case_example():
    # Handle an edge case of 0
    print("\n# Handle an edge case of 0")
    number = 0
    formatted = humanize_number(number)
    print(f"Edge Case - Zero: {formatted}")


if __name__ == "__main__":
    basic_humanize_example()
    custom_separator_example()
    small_number_example()
    large_number_example()
    edge_case_example()
