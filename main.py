from pink_python_quiz import run_pink_python_quiz
from sat_reading_trainer import run_sat_reading_trainer
from console import print_pink_message
from settings import QUIT_SIGNALS


# Menu functions

def main_menu():
    choice_list = [
        ("Pink Python Quiz", run_pink_python_quiz),
        ("S.A.T. ReadComp", run_sat_reading_trainer),
    ]

    print_pink_message("THE PINK CODERS WIKIPEDIA CHALLENGE PACK", is_header=True)

    done = False
    while not done:
            show_menu_choices(choice_list)
            print()

            # Repeat until valid input or quit
            while True:
                try:
                    user_choice = input("Go to: ")

                    if user_choice.lower() in QUIT_SIGNALS:
                        print()
                        print_pink_message("Giving up so soon? Fine, take a break if you must. But you'll be back...")
                        done = True
                        break


                    index = int(user_choice) - 1
                    func = choice_list[index][1]
                    print()
                    func()
                    break

                except Exception:
                    pass

            print()


def show_menu_choices(choice_list):
    """
        Args:
            choice_list: [("Description", callable)]
    """
    for i in range(len(choice_list)):
        print(f"{i + 1}" + f": {choice_list[i][0]}")


def execute_user_choice(choice_list, choice):
    """
        Calls the function from the choice list.
        Args:
            choice_list: [("Description", callable)]
            choice: int
        Returns:
            executed_successfully: boolean
    """
    index = choice - 1
    if not 0 <= index <= len(choice_list) - 1:  # catch wrong indices
        return False

    print()

    description, function = choice_list[index]
    if not function:
        print("That function is not yet implemented!")
    else:
        function()
    return True




def main():
    main_menu()


if __name__ == "__main__":
    main()