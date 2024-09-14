import time

from src.pratik.functions import progress_bar


def basic_progress_example():
    # Simple progress bar for a task
    print("\n# Bar 0 -> 50, without other parameters")
    total = 50
    for i in range(total):
        time.sleep(0.05)
        progress_bar(i + 1, total)
    print("\nTask Complete!")


def long_task_progress():
    # Progress bar for a long task
    print("\n# Bar 0 -> 100, without other parameters")
    total = 100
    for i in range(total):
        time.sleep(0.1)
        progress_bar(i + 1, total)
    print("\nLong Task Complete!")


def small_task_progress():
    # Progress bar for a small task
    print("\n# Bar 0 -> 10, without other parameters")
    total = 10
    for i in range(total):
        time.sleep(0.2)
        progress_bar(i + 1, total)
    print("\nSmall Task Complete!")


def progress_with_custom_size():
    # Progress bar with custom size
    print("\n# Bar 0 -> 50, with width at 50")
    total = 50
    for i in range(total):
        time.sleep(0.05)
        progress_bar(i + 1, total, width=50)
    print("\nTask with Custom Size Complete!")


def interrupted_task_progress():
    # Simulate an interrupted task
    print("\n# Bar 0 -> 50, with interruption.")
    total = 50
    for i in range(total):
        time.sleep(0.05)
        progress_bar(i + 1, total)
        if i == 24:
            print("\nTask Interrupted at 50%!")
            break


if __name__ == "__main__":
    basic_progress_example()
    long_task_progress()
    small_task_progress()
    progress_with_custom_size()
    interrupted_task_progress()
