import random
import urllib
import json
import openai
import wikipedia
from wikipedia.exceptions import PageError, DisambiguationError
from console import (
    pluralize,
    print_with_margins,
    print_pink_message,
    get_user_input,
    confirm_setting,
)
from settings import MARGIN, CONSOLE_WIDTH, load_openai_api_key

load_openai_api_key()

# If 10 exceptions occur while retrieving random articles, give up.
MAX_ERRORS = 10
# Skip articles that are too short for quiz generation.
PAGE_CONTENT_MIN_LENGTH = 1000

AVAILABLE_CATEGORIES = [
    "Python_(programming_language)",
    "Graphic_design",
    "Birds",
    "Music",
]
num_exercises = 1
category = AVAILABLE_CATEGORIES[0]


def set_num_exercises():
    while True:
        try:
            user_input = get_user_input("Number of reading exercises: ")
            number = int(user_input)
            if number < 1:
                print("Must be at least 1.")
                raise ValueError
            if number > 3:
                print("Maximum of 3 reading exercises per test allowed.")
                raise ValueError
            global num_exercises
            num_exercises = number
            confirm_setting()
            return

        except Exception:
            pass


def set_category():
    print("Available categories are:")
    for cat in AVAILABLE_CATEGORIES:
        print(cat)
    print()
    while True:
        try:
            user_input = get_user_input("Change to: ")
            if user_input not in AVAILABLE_CATEGORIES:
                print("Not supported. Please type the category name perfectly.")
                raise ValueError
            global category
            category = user_input
            confirm_setting()
            return

        except Exception:
            pass


# API Functions

# OpenAI API Functions

def gpt_nano_reading_exercises(wiki_articles):

    prompt_material = ""
    for i in range(len(wiki_articles)):
        article = wiki_articles[i]
        prompt_material += f"Article {i + 1}. {article['title']}\n\n"
        prompt_material += article["content"] + '\n'
        prompt_material += "-------------------------------------\n\n"


    prompt_format = """ [{
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
        }]
        """
    prompt = "The user will give you the content of several Wikipedia articles. For each article, I want you to select a short, readable snippet of about 100-200 words from the article. Create 3 questions about the text, each with 4 possible answers labeled A, B, C, and D. Please structure your response as JSON data that can be used directly in a program to run a reading comprehension quiz, like on the SAT. One reading snippet along with its 3 questions make up an exercise. I want there to be " + str(len(wiki_articles)) + " exercises in total. If the same article appears twice, don't worry. Just make sure that the reading material for all 3 exercises are different. The output format should look like: " + prompt_format

    print("Generating questions (may take a minute)...")
    response = openai.ChatCompletion.create(
        model="gpt-5-nano",
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": prompt_material
            }
        ],
    )

    data = json.loads(response.choices[0].message.content)

    exercises = data
    print("exercises are ", exercises)

    return exercises


# Wikipedia API Functions

def get_category_members(category_name):
    url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&list=categorymembers&cmtitle=Category:{category_name}"
    headers = {'User-Agent': 'Mozilla/5.0'}

    request = urllib.request.Request(url, headers=headers)
    response_text = urllib.request.urlopen(request).read()
    data = json.loads(response_text)

    return [member['title'] for member in data['query']['categorymembers']]


def get_random_category_page():
    page_titles = get_category_members(category)
    return random.choice(page_titles)


def random_wikipedia_articles(number):
    """ Gets `number` of articles as {'title': '...', 'content': '...'} .
        MAY return less than number.
    """

    print("Retrieving articles from Wikipedia...")

    num_errors = 0
    articles = []

    grabbed_articles = []

    while len(articles) < number and num_errors < MAX_ERRORS:
        try:
            article_title = get_random_category_page()
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
            if len(articles) == 0 and num_errors >= MAX_ERRORS:
                print("There was an error, no Wikipedia articles could be retrieved.")

    return articles


def generate_exercises():
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

    articles = random_wikipedia_articles(num_exercises)
    exercises = gpt_nano_reading_exercises(articles)

    return exercises


def run_exercise(exercise):
    """Eine Leseübung zu Nutzern zeigen und die
    Antworte sammeln.

    Return:
        score (int): Wie viele Punkten der Schüler von diesem Teil bekommt
        num_questions (int): Wie viele Frage gab es
    """

    topic = exercise["topic"]
    article_content = exercise["reading_text"]
    questions = exercise["questions"]

    score = 0
    num_questions = len(questions)
    exercise_results = []

    questions_ = pluralize("question", num_questions)

    print()
    print("DIRECTIONS:")
    print(f"Read the following excerpt about {topic} and choose the best answers to the following {num_questions} {questions_}.")
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
        user_answer = get_user_input(f"Your answer for question {i + 1} (A/B/C/D): ").strip().upper()

        # Check user´s answer
        if user_answer == questions[i]["answer"]:
            score += 1
            exercise_results.append('✅')
        else:
            exercise_results.append('❌')

    # Give a little feedback after each section
    print("Your answers for this article: ", end="")
    for emoji in exercise_results:
        print(emoji, end=" ")
    print(); print()

    # Return the score tallies
    return score, num_questions


def show_final_results(correct_answers, total_questions):

    percentage = (correct_answers / total_questions) * 100

    print("\n" + "=" * CONSOLE_WIDTH)
    print(f"{'FINAL SCORE'.center(CONSOLE_WIDTH)}", end="")

    if percentage >= 90:
        win_message = f"🏆 AMAZING! Score: {percentage:.2f}%\nYou are a true test taking Master!"
    elif percentage >= 60:
        win_message = f"Good Job! Score: {percentage:.2f}%\nYou're getting there!"
    else:
        win_message = f"Score: {percentage:.2f}%\nKeep practicing, you can do it!"

    print_pink_message(win_message, is_header=True)


def run_sat_reading_trainer():
    print_pink_message(f"🎯  S.A.T. READING COMPREHENSION TRAINER  ⏰", is_header=True)
    print()

    articles = pluralize("article", num_exercises)

    print(f"Practice test length: {num_exercises} {articles}")
    print("Let's get ready!  🧠")
    print("=" * CONSOLE_WIDTH)
    print()

    # Content generieren
    exercises = generate_exercises()

    score = 0
    max_score = 0

    for exercise in exercises:
        exercise_score, num_questions = run_exercise(exercise)
        score += exercise_score
        max_score += num_questions

    show_final_results(score, max_score)

    # Explanation - Maybe after the quiz ask the user if they want
    #                to see explanations of missed questions?
    # print(f"\n💡 {quiz['explanation']}")
    # print("\n" + "=" * 50 + "\n")