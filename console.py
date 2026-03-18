import sys
import textwrap
from settings import CONSOLE_WIDTH, QUIT_SIGNALS

# styles
PINK = '\033[95m'
BOLD = '\033[1m'
RESET = '\033[0m'


# Console and Printing Utils

def print_pink_message(message, is_header=False):
    if is_header:
        print(f"\n{PINK}{BOLD}{'=' * CONSOLE_WIDTH}")
        print(f"{message.center(CONSOLE_WIDTH)}")
        print(f"{'=' * CONSOLE_WIDTH}{RESET}\n")
    else:
        #print(f"{PINK}>> {message}{RESET}")
        print(f"{PINK}{message}{RESET}")


def print_divider():
    print("=" * CONSOLE_WIDTH)


def pluralize(text, n):
    """Returns text with 's' or no 's'."""
    if n == 1:
        return text
    else:
        return text + 's'

def a_n(next_word):
    """Returns 'a' or 'an'."""
    if next_word[0].lower() in 'aeiou':
        return "an"
    else:
        return "a"


def print_with_margins(input_text, margin_size):
    """Prints input_text in a smooth column with margin spacing."""

    margin = " " * margin_size

    wrapper = textwrap.TextWrapper(width=CONSOLE_WIDTH)
    lines = wrapper.wrap(input_text)

    print("\n")
    for line in lines:
        print(f"{margin}{line}{margin}")
    print("\n")


# User IO Wrapper
DEFAULT_GOODBYE_MESSAGE = "Giving up so soon? Fine, take a break if you must. But you'll be back..."
def exit_program(message=DEFAULT_GOODBYE_MESSAGE):
    print()
    print_pink_message(message, is_header=False)
    sys.exit()

def get_user_input(prompt):
    user_input = input(prompt)

    if user_input.lower() in QUIT_SIGNALS:
        exit_program()

    return user_input