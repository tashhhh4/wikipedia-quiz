import os
import json
import random
import textwrap
from dotenv import load_dotenv
import requests
import openai
import wikipedia
from wikipedia.exceptions import PageError, DisambiguationError


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key


######## Program settings #########
# If 10 exceptions occur while retrieving random articles, give up.
MAX_ERRORS = 10
# Skip articles that are too short for quiz generation.
PAGE_CONTENT_MIN_LENGTH = 1000
# The quiz is in English.
LANG = "EN"
# Wikipedia Page Categories the excerpts can come from.
TOPICS = ["Python_(programming_language)"]
# Length of the practice test.
NUM_EXERCISES = 1

######## Console print settings ########
PROGRAM_TITLE = "S.A.T. READING COMPREHENSION TRAINER"
CONSOLE_WIDTH = 43
MARGIN = 4

# Constant
PYTHON_PAGE_ID = 23862 # might be used to get categories


#### Desired Output ##################################
# (chatGPT: generates the content in the background)
#
# Read the following text and answer the question:
# # Snippet from Wikipedia 500 ~ 800 words
#
# (Specific comprehension question)
# a) ...    b) ...
# c) ...    d) ...
#
# # (and you only have 3 minutes to complete it)

# 1st version: no time limit

# Schritte:

# 1. ✅ Mit ChatGPT 5-nano (ohne das API key) in Webbrowser probieren um gute
#    output zu generieren
# 2. ✅ <<Wikipedia API>> nutzen irgendwo für Artikeltext ODER Link zu Artikel zu bekommen
# 3. ✅ OpenAI API nutzen für Fragetext zu generieren mit 4 Antwort
#    a. man konnte auch in der Prompt viele verschiedene Artikel geben so dass man
#       kriegt alle data zu viele Frage mit einem API-Call.
#    b. Man konnte auch zu eine Textstück viele Frage haben wie auf das SAT, das konnte
#       man als Parameter haben, steht wie viele Frage zum Textstück man habe will.
# 4. ✅ Console Input-Output schleife-basiertes Program schreiben um diese Funktion zu nutzen


def random_wikipedia_articles(number):
    """ Gets `number` of articles as {'title': '...', 'content': '...'} .
        MAY return less than number.
    """

    # https://en.wikipedia.org / wiki / Special: Random /
    print("Retrieving articles from Wikipedia...")

    num_errors = 0
    articles = []

    grabbed_articles = []

    while len(articles) < number and num_errors < MAX_ERRORS:
        try:
            # note: if we can get `get_category_members` to work then we don't need to use wikipedia.random() we can just use random() on the titles and then retrieve that page from the title.

            # article_title = wikipedia.random()

            article_title = get_category_page()
            if article_title in grabbed_articles:
                raise ValueError
            grabbed_articles.append(article_title)

            page_obj = wikipedia.page(title=article_title)
            article = {"title": page_obj.title, "content": page_obj.content}
            if len(article["content"]) < PAGE_CONTENT_MIN_LENGTH:
                raise ValueError
            articles.append(article)
        except DisambiguationError:
            num_errors += 1
        except PageError:
            num_errors += 1
        except ValueError:
            num_errors += 1

        finally:
            if len(articles) == 0:
                print("There was an error, no Wikipedia articles could be retrieved.")

    return articles


def get_category_members(category_name):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmpageid": PYTHON_PAGE_ID,
        "cmtitle": category_name,
        # "cmlimit": "500",  # Max. 500 Ergebnisse pro Anfrage
        "format": "json"
    }

    print("params are", params)

    response = requests.get(url, params=params).json()
    print("inside get_category_members. response is", response)
    return [member['title'] for member in response['query']['categorymembers']]

# PLACEHOLDER UNTIL THE ABOVE FUNCTION IS FIGURED OUT
def get_category_page():
    return random.choice([
        'Anaconda_(Python_distribution)',
        'Numba',
        'PyScript',
        'Python_Server_Pages',
        'Python_License',
        'PythonAnywhere',
        'Outline_of_the_Python_programming_language',
        'Flask_(web_framework)',
        'Django_Girls',
        'Docstring',
        'Django_(web_framework)',
        'Cython',
        'Zen_of_Python',
    ])


def generate_exercise():
    """1-5 Fragen nach einen bestimmten Teil aus einem Wikipedia-Artikel als "Leseübung" stellen.

    Args:
        difficulty (str): Difficult Level ("easy", "medium", "hard")

    Returns:
        (
            topic (str): article's title
            reading_text (str): A few paragraphs
            questions: [
                { "question": str,
                  "answer": char,
                  "options": [(char, str)]
                }
            ]
        )
    """

    article_obj = random_wikipedia_articles(1)[0]
    topic = article_obj["title"]
    article_text = article_obj["content"]

    prompt_format = """ {
    "topic": "Here is 1-3 words describing the topic of the text (for instance a school subject like 'Biology' or an interesting theme like 'Celebrity Culture'",
    "reading_text": "Here is about 100-200 words of text to read.",
    "questions": [
        {
          "question": "What was the main character's name?",
          "answer": "A",
          "options": [
            ["A", "Text for answer A"],
            ["B", "Text for answer B"],
            ["C", "Text for answer C"],
            ["D", "Text for answer D"]
          ]
        },
        {
          "question": "How many pet characters were there in the story?",
          "answer": "B",
          "options": [
            ["A", "Text for answer A"],
            ["B", "Text for answer B"],
            ["C", "Text for answer C"],
            ["D", "Text for answer D"]
          ]
        },
        {
          "question": "Why was Jane angry at her mother?",
          "answer": "D",
          "options": [
            ["A", "Text for answer A"],
            ["B", "Text for answer B"],
            ["C", "Text for answer C"],
            ["D", "Text for answer D"]
          ]
        }
      ]
    }
    """

    response = openai.ChatCompletion.create(
        model="gpt-5-nano",
        messages=[
            {
                "role": "system",
                "content": "The user will prompt you with the title of a Wikipedia article along with some text content from the article. I want you to select a short, readable snippet of about 100-200 words from the article. Create 3 questions about the text, each with 4 possible answers labeled A, B, C, and D. Please structure your response as JSON data that can be used directly in a program to run a reading comprehension quiz, like on the SAT. The output format should look like: " + prompt_format
            },
            {
                "role": "user",
                "content": "Topic: " + topic + "\n" + "Article Text:\n\n" + article_text
            }
        ],
    )

    data = json.loads(response.choices[0].message.content)

    topic = data["topic"]
    reading_text = data["reading_text"]
    questions = data["questions"]

    return topic, reading_text, questions


# Printing functions

def print_with_margins(input_text, margin_size):

    margin = " " * margin_size

    wrapper = textwrap.TextWrapper(width=CONSOLE_WIDTH)
    lines = wrapper.wrap(input_text)

    print("\n")
    for line in lines:
        print(f"{margin}{line}{margin}")
    print("\n")


def show_final_results(correct_answers, total_questions):

    percentage = (correct_answers / total_questions) * 100

    print("\n" + "=" * CONSOLE_WIDTH)
    print(" FINAL SCORE ")
    print("=" * CONSOLE_WIDTH)

    if percentage >= 90:
        print(f"🏆 AMAZING! Score: {percentage}%")
        print(f"You are a true test taking Master!")
    elif percentage >= 60:
        print(f"Good Job! Score: {percentage}%")
        print("You're getting there!")
    else:
        print(f"Score: {percentage}%")
        print("Keep practicing, you can do it!")
    print("=" * CONSOLE_WIDTH + "\n")


def run_exercise():
    """Eine Leseübung zu Nutzern zeigen und die
    Antworte sammeln.

    Return:
        score (int): Wie viele Punkten der Schüler von diesem Teil bekommt
        num_questions (int): Wie viele Frage gab es
    """

    # Content generieren
    topic, article_content, questions = generate_exercise()

    score = 0
    num_questions = len(questions)
    exercise_results = []

    print(f"Read the following excerpt about {topic} and choose the best answers to the following {num_questions} questions.")
    print()

    print_with_margins(article_content, MARGIN)
    print()

    # Frage ausgeben
    print("QUESTIONS:")
    for i in range(num_questions):
        print(f"{i + 1}. {questions[i]["question"]}")

        # Wir listen die Antwortmöglichkeiten auf
        for letter, text in questions[i]["options"]:
            print(f"{letter}) {text}")
        print()

    # Antwort des Benutzers eingeben
    for i in range(num_questions):
        user_answer = input(f"Your answer for question {i + 1} (A/B/C/D): ").strip().upper()

        # Check user´s answer
        if user_answer == questions[i]["correct_answer"]:
            score += 1
            exercise_results.append('✅')
        else:
            exercise_results.append('❌')

        # if user_answer == quiz['correct_answer']:
        #    print("✅ Correct!")
        #    score += 1
        # else:
        #    print(f"❌ Falsch. Richtig ist: {quiz['correct_answer']}")

    # Give a little feedback after each section
    print("Your answers for this article: ", end="")
    for emoji in exercise_results:
        print(emoji, end=" ")
    print(); print()

    # Return the score tallies
    return score, num_questions


def main():
    print("=" * CONSOLE_WIDTH)
    print(f"🎯  {PROGRAM_TITLE}  ⏰")
    print("=" * CONSOLE_WIDTH)
    print()

    print("Practice test length: 1 question")
    print("Let's get ready!  🧠")
    print("=" * CONSOLE_WIDTH)
    print()

    num_exercises = 1

    score = 0
    max_score = 0

    for i in range(num_exercises):
        exercise_score, num_questions = run_exercise()
        score += exercise_score
        max_score += num_questions

    show_final_results(score, max_score)

    # Explanation - Maybe after the quiz ask the user if they want
    #                to see explanations of missed questions?
    # print(f"\n💡 {quiz['explanation']}")
    # print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    main()