import textwrap
from settings import CONSOLE_WIDTH

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
    if n == 1:
        return text
    else:
        return text + 's'


def print_with_margins(input_text, margin_size):

    margin = " " * margin_size

    wrapper = textwrap.TextWrapper(width=CONSOLE_WIDTH)
    lines = wrapper.wrap(input_text)

    print("\n")
    for line in lines:
        print(f"{margin}{line}{margin}")
    print("\n")
