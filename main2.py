import os
from dotenv import load_dotenv
import openai
import wikipedia
import requests
import random
from wikipedia.exceptions import PageError, DisambiguationError

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key


# Program settings
MAX_ERRORS = 10 # If 10 exceptions occur while retrieving random articles, give up.
PAGE_CONTENT_MIN_LENGTH = 1000 # Skip articles that are too short for quiz generation.
LANG = "EN" # The quiz is in English.
TOPIC = "Python_(programming_language)"

# Console prints
PROGRAM_TITLE = "S.A.T. READING COMPREHENSION TRAINER"
HEADER_WIDTH = 43

# Constant
PYTHON_PAGE_ID = 23862


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

# 1. Mit ChatGPT 5-nano (ohne das API key) in Webbrowser probieren um gute
#    output zu generieren
# 2. <<Wikipedia API>> nutzen irgendwo für Artikeltext ODER Link zu Artikel zu bekommen
# 3. OpenAI API nutzen für Fragetext zu generieren mit 4 Antwort
#    a. man konnte auch in der Prompt viele verschiedene Artikel geben so dass man
#       kriegt alle data zu viele Frage mit einem API-Call.
#    b. Man konnte auch zu eine Textstück viele Frage haben wie auf das SAT, das konnte
#       man als Parameter haben, steht wie viele Frage zum Textstück man habe will.
# 4. Console Input-Output schleife-basiertes Program schreiben um diese Funktion zu nutzen

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

# PLACEHOLDER UNTIL THE ABOVE REQUEST IS FIGURED OUT
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


def generate_quiz_question(topic, difficulty="medium"):
    """
    Erstellt eine Quizfrage zu einem bestimmten Thema.

    Args:
        topic (str): (z.B., "Python", "Geschichte")
        difficulty (str): Difficult Level ("easy", "medium", "hard")

    Returns:
        dict: Vokabelliste mit Frage, Antwortmöglichkeiten und der richtigen Antwort
    """
    prompt = f"""
    Erstelle eine Quizfrage zum Thema "{topic}" Schwierigkeitsgrad {difficulty}.

    Antwortformat (nur JSON):
    {{
        "question": "Fragetext",
        "options": ["A) Variant 1", "B) Variant 2", "C) Variant 3", "D) Variant 4"],
        "correct_answer": "A",
        "explanation": "Erklärung, warum dies die richtige Antwort ist"
    }}
    """

    response = openai.ChatCompletion.create(
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content": "Du bist Experte für die Erstellung von Lernquizzen."},
            {"role": "user", "content": prompt}
        ],
    )

    import json
    quiz_data = json.loads(response.choices[0].message.content)
    return quiz_data

# Printing functions
def print_with_margins(text, margin=8):
    """
    Prints text with indents on the left and right.

    Args:
        text (str): Text to print
        margin (int): Left indent (number of spaces)
    """
    # Breaking text into lines
    lines = text.split('\n')

    # Print each line with an indent
    for line in lines:
        print(' ' * margin + line)


def show_final_results(correct_answers, total_questions):

    percentage = (correct_answers / total_questions) * 100

    print("\n" + "=" * 30)
    print(" FINAL SCORE ")
    print("=" * 30)

    if percentage >= 90:
        print(f"🏆 AMAZING! Score: {percentage}%")
        print(f"You are a true {TOPIC} Master!")
    elif percentage >= 60:
        print(f"Good Job! Score: {percentage}%")
        print("You're getting there!")
    else:
        print(f"Score: {percentage}%")
        print("Keep practicing, you can do it!")
    print("=" * 30 + "\n")


def run_exercise():
    """ Fragen nach einen bestimmten Wikipedia-Artikel stellen.

    Args:
        num_questions (int): Wie viele Frage kommen
    Return:
        score (int): Wie viele Punkten der Schüler von diesem Teil bekommt
        num_questions (int): Wie viele Frage gab es
    """

    # Frage generieren
    # topic, article_content, questions = generate_exercise()
    #         generate_quiz_question() => generate_exercise()
    topic = "Princess Antonia of Luxembourg"
    questions = [
        {"question": "Choose the answer C) to win.",
         "correct_answer": "C",
         "options": [("A", "Text for A"),
                     ("B", "Text for B"),
                     ("C", "Text for C"),
                     ("D", "Text for D")]
         },
        {"question": "Choose the answer A) to win.",
         "correct_answer": "A",
         "options": [("A", "Text for A"),
                     ("B", "Text for B"),
                     ("C", "Text for C"),
                     ("D", "Text for D")]
         },
        {"question": "The correct answer is not A, is not the last answer, and is related to an animal that can meow.",
         "correct_answer": "C",
         "options": [("A", "Text for A"),
                     ("B", "Text for B"),
                     ("C", "Text for C"),
                     ("D", "Text for D")]
         },
    ]
    article_content = """In 1925, she served as patron of the first ever Chrysanthemum Ball in Munich.

    Being anti-Nazi and connected to a resistance plot, the family was forced to flee to the Kingdom of Italy and then Kingdom of Hungary in 1939.[4] Five years later, the Nazis had occupied Hungary and were looking to arrest her husband, Rupprecht, who was underground in Italy. It was Nazi policy, that if one family member was accused of a crime, the entire family would be held liable. Hitler personally ordered the arrest of Princess Antonia and her children. A meeting with the British Foreign Office's summary reports Rupprecht as telling George V that he "remained convinced that the Führer was insane."[4]

    During their imprisonment Antonia contracted typhus and was hospitalized in Innsbruck.[4] Once well, Antonia was shipped to the Sachsenhausen concentration camp where her adult children were also being imprisoned. As the Soviets got closer to the Third Reich, they were transported to Flossenburg concentration camp and finally to Dachau concentration camp.[4] The United States Army liberated the Dachau camp in 1945."""

    score = 0
    num_questions = len(questions)
    exercise_results = []

    print(f"Read the following excerpt about {topic} and choose the best answers to the following {num_questions} questions.")
    print()

    print(article_content)
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
    print("=" * HEADER_WIDTH)
    print(f"🎯  {PROGRAM_TITLE}  ⏰")
    print("=" * HEADER_WIDTH)
    print()

    score = 0
    max_score = 0

    exercise_score, num_questions = run_exercise()

    score += exercise_score
    max_score += num_questions


    show_final_results(exercise_score, max_score)


    # Explanation - Maybe after the quiz ask the user if they want
    #                to see explanations of missed questions?
    # print(f"\n💡 {quiz['explanation']}")
    # print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    main()