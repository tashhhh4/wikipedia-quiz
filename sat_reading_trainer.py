from functions import (
    random_wikipedia_articles,
    gpt_nano_reading_exercise
)
from console import pluralize, print_with_margins, print_pink_message
from settings import MARGIN, CONSOLE_WIDTH


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

    topic, reading_text, questions = gpt_nano_reading_exercise(topic, article_text)

    return topic, reading_text, questions


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
        user_answer = input(f"Your answer for question {i + 1} (A/B/C/D): ").strip().upper()

        # Check user´s answer
        if user_answer == questions[i]["answer"]:
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
    num_exercises = 1

    print_pink_message(f"🎯  S.A.T. READING COMPREHENSION TRAINER  ⏰", is_header=True)
    print()

    articles = pluralize("article", num_exercises)

    print(f"Practice test length: {num_exercises} {articles}")
    print("Let's get ready!  🧠")
    print("=" * CONSOLE_WIDTH)
    print()

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