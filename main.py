from pink_python_quiz import (
    run_pink_python_quiz,
    set_num_questions as set_ppq_num_questions,
    set_difficulty as set_ppq_difficulty,
)
from sat_reading_trainer import (
    run_sat_reading_trainer,
    set_num_exercises as set_sat_num_exercises,
    set_category as set_sat_category,
)
from console import (
    print_pink_message,
    get_user_input,
    print_centered,
    print_divider,
)


# Menu functions

def settings_menu():
    while True:
        choice_list = [
            ("Change number of questions", set_ppq_num_questions),
            ("Change difficulty", set_ppq_difficulty),
            ("Change number of exercises", set_sat_num_exercises),
            ("Change topic category", set_sat_category),
        ]
        print_centered("🔧  SETTINGS  ⚙️")
        print_divider()
        print("Pink Python Quiz")
        print(f"{0 + 1}. {choice_list[0][0]}")
        print(f"{1 + 1}. {choice_list[1][0]}")
        print()
        print("S.A.T ReadComp Trainer")
        print(f"{2 + 1}. {choice_list[2][0]}")
        print(f"{3 + 1}. {choice_list[3][0]}")
        print()
        print("0. Go Back")
        print()

        # Repeat until valid input
        while True:
            try:
                user_choice = get_user_input("Go to: ")

                if int(user_choice) == 0:
                    return

                index = int(user_choice) - 1
                func = choice_list[index][1]
                print()
                func()
                break

            except Exception:
                pass

        print()


def main_menu():
    choice_list = [
        ("Pink Python Quiz (de)", run_pink_python_quiz),
        ("S.A.T. ReadComp (en)", run_sat_reading_trainer),
        ("Settings", settings_menu),
    ]

    print_pink_message("THE PINK CODERS WIKIPEDIA CHALLENGE PACK", is_header=True)
    print("Note: Some challenges are in English, and others in German.")
    print()

    while True:
        show_menu_choices(choice_list)
        print()

        # Repeat until valid input
        while True:
            try:
                user_choice = get_user_input("Go to: ")
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