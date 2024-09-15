def clear():
    """
    simple function to clear the console by spamming 100 line skips
    :return: nothing
    """
    print("\n" * 100)


def wait_forintro():
    """
    simple function that waits for the user to press ENTER to continue, and then clears the console
    :return: nothing
    """
    print("PRESS ENTER TO CONTINUE")
    v1 = input(" ")
    print("\n" * 100)


def bubble_sort(arr):
    """
    just a model function for bubble sort.
    """
    for n in range(len(arr) - 1, 0, -1):
        for i in range(n):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]