from pratik.functions import enter


def enter_integer():
    print("\n# Prompt the user to enter an integer")
    number = enter("Enter an integer: ", int)
    print(f"You entered integer: {number}")


def enter_boolean():
    print("\n# Prompt the user to enter a boolean value")
    response = enter("Do you agree? (yes/no): ", bool)
    print(f"Boolean response: {response}")


def enter_list_of_numbers():
    print("\n# Prompt the user to enter a list of numbers")
    numbers = enter("Enter a list of numbers (spaces-separated): ", list)
    print(f"You entered list: {numbers}")


def enter_complex_number():
    print("\n# Prompt the user to enter a complex number")
    complex_num = enter("Enter a complex number (e.g., 1+2j): ", complex)
    print(f"You entered complex number: {complex_num}")


def enter_slice():
    print("\n# Prompt the user to enter a slice")
    slicing = enter("Enter a slice (e.g., 1:5): ", slice)
    print(f"You entered slice: {slicing}")


def enter_with_error_handling():
    print("\n# Handle invalid input with a retry loop")
    try:
        percentage = enter("Enter a float percentage (0.0 - 100.0): ", float)
        if not (0 <= percentage <= 100):
            raise ValueError("Percentage must be between 0 and 100.")
        print(f"Valid percentage: {percentage}")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    enter_integer()
    enter_boolean()
    enter_list_of_numbers()
    enter_complex_number()
    enter_slice()
    enter_with_error_handling()
