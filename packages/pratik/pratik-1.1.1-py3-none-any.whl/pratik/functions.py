import inspect
import pathlib

from pratik.text import Color


class Menu:
    """Class to manage an interactive menu.

    Attributes:
    -----------
    title : str
        The title of the menu.
    description : str
        The description of the menu.
    description_center : bool
        Whether to center the description text or not.
    choices : tuple
        The available options in the menu.
    back_button : str
        Text for the back button.
    selected : int
        Index of the currently selected option.
    """

    def __init__(self, *choices, title=..., description=..., back_button=..., description_center=False):
        # Initialize the menu with given choices, title, description, and back button
        self.title = ... if title is ... or title == '' or title.isspace() else title
        self.description = ... if description is ... or description == '' or description.isspace() else description
        self.description_center = description_center
        self.choices = choices
        self.back_button = back_button

        # Default selected option is the first one
        self.selected = 0

    def __len__(self):
        # Return the number of choices available in the menu
        return len(self.choices)

    def __str__(self):
        """Creates a string representation of the menu with a formatted structure."""

        def get_title():
            # Build the title section of the menu
            if isinstance(self.title, str):
                line1 = f"  ╔═{'═' * len(self.title)}═╗  ".center(width) + "\n"
                line2 = "╔" + f"═╣ {self.title} ╠═".center(width - 2, '═') + "╗\n"
                line3 = "║" + f" ╚═{'═' * len(self.title)}═╝ ".center(width - 2) + "║\n"

                return line1 + line2 + line3
            else:
                return f"╔{'═' * (width - 2)}╗\n"

        def get_description(desc=...):
            # Build the description section
            if desc is ...:
                if self.description is ...:
                    return ''
                desc: list[str] = self.description.split()

            result = ""

            while len(desc) != 0:
                word = desc.pop(0)
                if len(f"║{result} {word} ║") > width:
                    if self.description_center:
                        return "║" + result.center(width - 3) + " ║\n" + get_description([word] + desc)
                    else:
                        return "║" + result.ljust(width - 3) + " ║\n" + get_description([word] + desc)
                else:
                    result += f" {word}"

            if self.description_center:
                return "║" + result.center(width - 3) + " ║\n" + get_separator()
            else:
                return "║" + result.ljust(width - 3) + " ║\n" + get_separator()

        def get_choice_button(number, choice: str):
            # Build each choice button, highlighting the selected option
            if number == self.selected:
                return (
                    f"║ {Color.RED}╔═{'═' * nb_width}═╗╔═{'═' * (width - nb_width - 12)}═╗{Color.STOP} ║\n"
                    f"║ {Color.RED}║ {str(number).zfill(nb_width)} ╠╣ {choice.ljust(width - nb_width - 12)} ║{Color.STOP} ║\n"
                    f"║ {Color.RED}╚═{'═' * nb_width}═╝╚═{'═' * (width - nb_width - 12)}═╝{Color.STOP} ║\n"
                )
            else:
                return (
                    f"║ ┌─{'─' * nb_width}─┐┌─{'─' * (width - nb_width - 12)}─┐ ║\n"
                    f"║ │ {str(number).zfill(nb_width)} ├┤ {choice.ljust(width - nb_width - 12)} │ ║\n"
                    f"║ └─{'─' * nb_width}─┘└─{'─' * (width - nb_width - 12)}─┘ ║\n"
                )

        def get_back_button():
            # Optionally add a back button if provided
            if isinstance(self.back_button, str):
                return get_separator() + get_choice_button(0, self.back_button)
            else:
                return ''

        def get_separator():
            # Return a separator line
            return f"╟{'─' * (width - 2)}╢\n"

        def get_footer():
            # Return the footer line
            return f"╚{'═' * (width - 2)}╝"

        # If no choices are available, return a message indicating the menu is empty
        if len(self) == 0:
            return "The menu is empty."

        # Calculate width for formatting
        width = self._width
        nb_width = self._width_number

        # Construct the full menu string
        return (
                get_title() +
                get_description() +
                ''.join(get_choice_button(i + 1, self.choices[i]) for i in range(len(self.choices))) +
                get_back_button() +
                get_footer()
        )

    def __repr__(self):
        # Return a string representation useful for debugging
        return repr(self.choices)

    def __iter__(self):
        # Allow the menu to be iterable over choices
        return iter(self.choices)

    def __next__(self):
        # Move to the next option in the menu
        self.selected = (self.selected % len(self.choices)) + 1

    @property
    def _width(self):
        """Calculates the necessary width for the menu layout based on title, description, and choices."""
        if isinstance(self.title, str):
            title_size = len(f"╔═╣ {self.title} ╠═╗")
        else:
            title_size = 0

        if isinstance(self.description, str):
            desc_data = {
                len(word): word for word in self.description.split()
            }
            description_size = len(f"║ {desc_data[max(desc_data.keys())]} ║")
            del desc_data
        else:
            description_size = 0

        choice_data = {
            len(word): word for word in self.choices
        }
        choice_size = len(f"║ │ {len(self.choices)} ├┤ {choice_data[max(choice_data.keys())]} │ ║")
        del choice_data

        if isinstance(self.back_button, str):
            back_size = len(f"║ │ {len(self.choices)} ├┤ {self.back_button} │ ║")
        else:
            back_size = 0

        return max(title_size, description_size, choice_size, back_size)

    @property
    def _width_number(self):
        # Calculates the width needed to display the number of choices
        return len(str(len(self.choices)))

    def select(self):
        """Prompts the user to select an option from the menu.

        :return: The selected option index.
        :rtype: int
        :raise IndexError: If the input is out of the valid range.
        """
        chx = enter(">> ")
        if chx not in range(0 if isinstance(self.back_button, str) else 1, len(self.choices) + 1):
            raise IndexError
        self.selected = chx
        return chx


def get_path(*path):
    """Retrieves the file path, considering different execution environments.

    :param path: Additional paths to append.
    :type path: str
    :return: A string representing the complete path.
    :rtype: str
    """
    # Get the filename of the caller
    caller_frame = inspect.stack()[1]
    caller_file = caller_frame.filename

    # Compute the absolute path relative to the caller's file location
    caller_path = pathlib.Path(caller_file).parent
    for part_path in path:
        if part_path == '..':
            caller_path = caller_path.parent
        else:
            caller_path = caller_path.joinpath(part_path)
    return str(caller_path.absolute()).replace('\\', '/')


def enter(__prompt='', __type=int):
    """This function allows to input any type.

    Types:
    ------
    - bool
    - complex
    - float
    - int
    - list
    - set
    - slice
    - str

    :param __prompt:  Text to print before recovery.
    :type __prompt: str
    :param __type: The type to recover. [bool, complex, float, int, list, set, slice, str]
    :type __type: type

    :return: The input in the requested type.
    :rtype: bool | complex | float | int | list | set | slice | str

    :raise TypeError: If __type is not in return type.
    """
    if __type not in [
        bool, complex, float, int, list, set, slice, str
    ]:
        raise TypeError(f'{__type} is not a possible type.')
    var: str = input(__prompt)
    while True:
        try:
            '''  '''
            if __type == bool:
                if var.lower() in [
                    "yes", "是的", "हां", "sí", "si", "نعم", "হ্যাঁ", "oui", "да", "sim", "جی ہاں",
                    "y", "1", "true"
                ]:
                    return True
                elif var.lower() in [
                    "no", "不", "नहीं", "no", "لا", "না", "non", "нет", "não", "nao", "نہیں",
                    "n", "0", "false"
                ]:
                    return False
                else:
                    raise ValueError(f"could not convert string to bool: '{var}'")
            elif __type == slice:
                return slice(*var.split(':'))
            elif __type == list:
                return var.split()
            return __type(var)
        except ValueError:
            print(Color.RED + f"\"{var}\" is not of type {__type.__name__}" + Color.STOP)
            var: str = input(__prompt)


def humanize_number(__number, __fill_char='.'):
    """Formats a number with separators to enhance readability.

    :param __number: The number to format.
    :type __number: int
    :param __fill_char: The character to use as a separator.
    :type __fill_char: str

    :return: The formatted number as a string.
    :rtype: str
    """

    number = list(reversed(str(__number)))
    return ''.join(reversed(__fill_char.join(''.join(number[x:x+3])for x in range(0, len(number), 3))))


def gcd(a, b):
    """Computes the greatest common divisor of two numbers using recursion.

    :param a: The first number.
    :type a: int
    :param b: The second number.
    :type b: int
    :return: The greatest common divisor.
    :rtype: int
    """

    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def progress_bar(x, n, *, width=100) -> None:
    """ Displays a progress bar in the console.
    Please, use `\r` for overwrite the line.

    :param x: The current progress count.
    :type x: int
    :param n: The total count to reach 100%.
    :type n: int
    :param width: The width of the progress bar.
    :type width: int
    """
    pourcent = x / n
    size = round(pourcent * width)
    print(f"\r{x:0{len(str(n))}}/{n} | {'█'*size}{'░'*(width - size)} {round(pourcent * 100):3}%", end='')