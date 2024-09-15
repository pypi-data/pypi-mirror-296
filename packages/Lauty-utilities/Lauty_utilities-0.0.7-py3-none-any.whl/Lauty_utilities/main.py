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


def string_methods_with_desc():
    """
    capitalize()	Converts the first character to upper case

    casefold()	Converts string into lower case

    center()	Returns a centered string

    count()	Returns the number of times a specified value occurs in a string

    encode()	Returns an encoded version of the string

    endswith()	Returns true if the string ends with the specified value

    expandtabs()	Sets the tab size of the string

    find()	Searches the string for a specified value and returns the position of where it was found

    format()	Formats specified values in a string

    format_map()	Formats specified values in a string

    index()	Searches the string for a specified value and returns the position of where it was found

    isalnum()	Returns True if all characters in the string are alphanumeric

    isalpha()	Returns True if all characters in the string are in the alphabet

    isascii()	Returns True if all characters in the string are ascii characters

    isdecimal()	Returns True if all characters in the string are decimals

    isdigit()	Returns True if all characters in the string are digits

    isidentifier()	Returns True if the string is an identifier

    islower()	Returns True if all characters in the string are lower case

    isnumeric()	Returns True if all characters in the string are numeric

    isprintable()	Returns True if all characters in the string are printable

    isspace()	Returns True if all characters in the string are whitespaces

    istitle()	Returns True if the string follows the rules of a title

    isupper()	Returns True if all characters in the string are upper case

    join()	Converts the elements of an iterable into a string

    ljust()	Returns a left justified version of the string

    lower()	Converts a string into lower case

    lstrip()	Returns a left trim version of the string

    maketrans()	Returns a translation table to be used in translations

    partition()	Returns a tuple where the string is parted into three parts

    replace()	Returns a string where a specified value is replaced with a specified value

    rfind()	Searches the string for a specified value and returns the last position of where it was found

    rindex()	Searches the string for a specified value and returns the last position of where it was found

    rjust()	Returns a right justified version of the string

    rpartition()	Returns a tuple where the string is parted into three parts

    rsplit()	Splits the string at the specified separator, and returns a list

    rstrip()	Returns a right trim version of the string

    split()	Splits the string at the specified separator, and returns a list

    splitlines()	Splits the string at line breaks and returns a list

    startswith()	Returns true if the string starts with the specified value

    strip()	Returns a trimmed version of the string

    swapcase()	Swaps cases, lower case becomes upper case and vice versa

    title()	Converts the first character of each word to upper case

    translate()	Returns a translated string

    upper()	Converts a string into upper case

    zfill()	Fills the string with a specified number of 0 values at the beginning
    """


def list_methods_with_desc():
    """
    append()	Used for adding elements to the end of the List.

	copy()	It returns a shallow copy of a list

	clear()	This method is used for removing all items from the list.

	count()	These methods count the elements.

	extend()	Adds each element of an iterable to the end of the List

	index()	Returns the lowest index where the element appears.

	insert()	Inserts a given element at a given index in a list.

	pop()	Removes and returns the last value from the List or the given index value.

	remove()	Removes a given object from the List.

	reverse()	Reverses objects of the List in place.

	sort()	Sort a List in ascending, descending, or user-defined order

	min()	Calculates the minimum of all the elements of the List

	max()	Calculates the maximum of all the elements of the List
    """