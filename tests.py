from main2 import random_wikipedia_articles, get_category_members, print_with_margins, prompt_gpt_5_nano
import json
import wikipedia

print("running tests.py")

# test functions
#articles = random_wikipedia_articles(2)
#for i in range(len(articles)):
#    print(f"{i}. {articles[i]["title"]} (content={len(articles[i]["content"])} chars)")

#titles = get_category_members("Python_(programming_language)")
#for t in titles:
#    print(t)

# print("Normal printed console output.")
# print()

# text = """Here is some text printed from the print_with_margins(text)
# function. It prints the text with extra space to the right
# and left so that it sticks out from the other text above and
# below it in the console."""
#
# print_with_margins(text, 8)

def test_prompter():
    response = prompt_gpt_5_nano()
    data = json.loads(response.choices[0].message.content)

    reading_text = data["reading_text"]
    questions = data["questions"]
    topic = data["topic"]

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

test_prompter()