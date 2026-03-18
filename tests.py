from termcolor import colored
import json
import wikipedia

from main import (
    random_wikipedia_articles,
    get_category_members,
    print_with_margins,
    generate_exercise,
)

#PINK + 'clean strings schreiben' + ENDC
#colors.get("pink") + 'my string is here' + colors.get("finished")

print("running tests.py")

def test_prompter():
    output = generate_exercise()

    reading_text = output[0]
    questions = output[1]
    topic = output[2]

    print("The text to read for the question will be:")
    print(reading_text)
    print("The questions will be (3 questions):")
    num_questions = len(questions)
    for i in range(num_questions):
        print(f"{i + 1}. {questions[i]["question"]}")
        for letter, text in questions[i]["options"]:
            print(f"{letter}) {text}")
            print(f"Correct answer: {questions[i]["answer"]}")
        print()

def test_category_function():
    category_name = "Python_(programming_language)"
    category_members = get_category_members(category_name)
    print("category members are", category_members)

test_category_function()

#print(colored('Hallo Ninja (Player), Willkommen zum Pink Coders Quiz', 'blue', 'on_white'))

# colored wrapper functions
# pass everything to print
#def print_blue(text, end="\n"):
#    print(colored(text, 'blue'), end)
