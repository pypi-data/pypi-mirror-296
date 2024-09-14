from pratik.functions import get_path


def basic_path_example():
    # Get a simple path for a file
    print("\n# Path : ./folder/file.txt")
    path = get_path("folder", "file.txt")
    print(f"Basic Path: {path}")


def nested_path_example():
    # Get a path for a nested directory structure
    print("\n# Path : ./root/subfolder/another_folder/file.txt")
    path = get_path("root", "subfolder", "another_folder", "file.txt")
    print(f"Nested Path: {path}")


def dynamic_path_example():
    # Use dynamic segments to build a path
    print("\n# Path : ./../logs/2024/August/logfile.txt")
    segments = ["..", "logs", "2024", "August", "logfile.txt"]
    path = get_path(*segments)
    print(f"Dynamic Path: {path}")


if __name__ == "__main__":
    basic_path_example()
    nested_path_example()
    dynamic_path_example()
