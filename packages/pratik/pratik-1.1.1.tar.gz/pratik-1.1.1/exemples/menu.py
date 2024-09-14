from pratik.functions import Menu


def basic_menu():
    # Basic menu with minimal setup
    print("\n# Menu with only options:")
    menu = Menu("Option 1", "Option 2", "Option 3")
    print(menu)
    choice = menu.select()
    print(f"Basic Menu: You selected Option {choice}")


def menu_with_title_and_description():
    # Menu with a title and a description
    print("\n# Menu with title and description:")
    menu = Menu(
        "Start", "Settings", "Exit",
        title="Main Menu",
        description="Welcome to the application. Please choose an option:"
    )
    print(menu)
    choice = menu.select()
    print(f"Menu with Title and Description: You selected Option {choice}")


def menu_with_back_button():
    # Menu with a back button
    print("\n# Menu with title and back button:")
    menu = Menu(
        "Play", "Load Game", "Options",
        title="Game Menu",
        back_button="Back"
    )
    print(menu)
    choice = menu.select()
    if choice == 0:
        print("You selected Back")
    else:
        print(f"Menu with Back Button: You selected Option {choice}")


def menu_with_centered_description():
    # Menu with centered description text
    print("\n# Menu with title and centered description:")
    menu = Menu(
        "New Game", "Continue", "Quit",
        title="Adventure Menu",
        description="Begin your journey or continue where you left off.",
        description_center=True
    )
    print(menu)
    choice = menu.select()
    print(f"Menu with Centered Description: You selected Option {choice}")


def large_menu_example():
    # Large menu with many options
    print("\n# Menu with title and many options:")
    options = [f"Option {i}" for i in range(1, 21)]
    menu = Menu(*options, title="Large Menu")
    print(menu)
    choice = menu.select()
    print(f"Large Menu: You selected Option {choice}")


def interactive_menu_example():
    # Interactive menu with dynamic selections
    print("\n# Menu with title and description with dynamic selection:")
    menu = Menu(
        "View Profile", "Edit Profile", "Logout",
        title="User Settings",
        description="Manage your account settings:"
    )
    while True:
        print(menu)
        choice = menu.select()
        if choice == 1:
            print("Viewing Profile...")
        elif choice == 2:
            print("Editing Profile...")
        elif choice == 3:
            print("Logging out...")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    basic_menu()
    menu_with_title_and_description()
    menu_with_back_button()
    menu_with_centered_description()
    large_menu_example()
    interactive_menu_example()
