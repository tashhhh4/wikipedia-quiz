from console import (
    print_pink_message,
    a_n,
    print_divider,
    print_with_margins,
    get_user_input
)
from settings import CONSOLE_WIDTH, MARGIN

SUBSTITUTE = '!���!'

def run_mad_libs():
    """Diese Funktion zeigt die Wörter in `hints` zum User und eine Liste Wörter sammelt.
    Dann zeigt es zum User das Story als Ergebnis.
    """
    print_pink_message("Wikipedia Mad Libs", is_header=True)

    print("Generating your story (with a little help from Wikipedia and ChatGPT)...")
    print()
    # story_with_blanks, hints = create_madlib()
    story_with_blanks = "My name is !���! !���! and I am in !���! grade!"
    hints = ["first name", "last name", "elementary school grade year"]
    words = []
    for hint in hints:
        a = a_n(hint)
        user_input = get_user_input(f"Gimme {a} {hint}: ")
        words.append(user_input)
    print()

    story = story_with_blanks
    for word in words:
        story = story.replace(SUBSTITUTE, word, 1)
    print("Result".center(CONSOLE_WIDTH))
    print_divider()
    print_with_margins(story, MARGIN)


# def create_madlib():
"""Diese Funktion nutzt das Wikipedia API und das OpenAI API um eine
   madlib zu erstellen.

   return: (text_with_blanks, hints)
            text_with_blanks [str]: Ein Text mit einigen Wörter mit "!���!" ersetzt.
            hints [str]: Eine liste von Hinweise strings
"""
#     # Einen Artikel von Wikipedia nehmen -> Funktion
#           - Random artikels probieren bis zu ein gut ist.
#           Check, um das Artikel gut Basismaterial ist -> bool Funktion
#               # ⬇️ Jede Punkt kann eine neue bool Funktion sein
    #           - Wenn das Artikel enthalt schlechte oder gefährliche Wörter
#                 kann das Thema vielleicht zu niedrig für eine Lustige Spiel sein.
#               - Wenn das Artikel zu klein ist gibt es nicht genug Text um einen
#                 Madlib zu machen
#               - Wenn das Artikel zu viele Zahlen, symbolen enthalt kann es eine zu
#                 technische Artikel über Programmierung oder Mathematik sein.
#               - Wenn das Artikel zu viele lange Wörter oder sehr schwerige Kemisprache
#                 etc. enthalt
#     # Ein String zu einem String mit einige Wörter zu ______ verändern.
#           # Prompt erstellen
#               # Was wenn es gibt schon "_" in das Text...
                # mit hilfe von ChatGPT -> chatgpt-rufe-funktion

#     # Eine Liste von die Grammatiktyp den Wörter machen.
#     return (madlibtext, words)

# ⬇️ AUFGAUBE
# def gpt_prompt(prompt):
#     # look in pink_python_quiz.py
# return result
def create_madlib():
    original_text = "some text here {nomen1}"

    print("--- Willkommen beim MadLibs-Spiel! ---")
    print("Bitte fülle die Lücken aus:\n")

    words = {
        "nomen1": get_user_input("Gib ein Nomen ein (z.B. Computer): "),
        "verb1": get_user_input("Gib ein Verb ein (z.B. lernen): "),
        "nomen2": get_user_input("Gib noch ein Nomen ein: "),
        "adjektiv1": get_user_input("Gib ein Adjektiv ein (z.B. schnell): "),
        "zahl": get_user_input("Gib eine Zahl ein: "),
        "verb2": get_user_input("Gib ein weiteres Verb ein: "),
        "nomen_pl": get_user_input("Gib ein Nomen im Plural ein (z.B. Leute): "),
        "adjektiv2": get_user_input("Gib ein letztes Adjektiv ein: ")
    }

    #  (Logic)
    madlib_story = original_text.format(**words)

    # 4. Ereignisse
    print("\n--- Hier ist dein fertiger Text: ---")
    print(madlib_story)

    return madlib_story, words


def gpt_prompt(prompt):
    # Diese Funktion wird später mit OpenAI API verbunden
    pass


if __name__ == "__main__":
    create_madlib()
