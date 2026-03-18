import openai
from console import get_user_input
from settings import CONSOLE_WIDTH, load_openai_api_key

load_openai_api_key()


def generate_quiz_questions(topic, num_questions, difficulty="medium"):
    """
    Erstellt eine Quizfrage zu einem bestimmten Thema.

    Args:
        topic (str): (z.B., "Python", "Geschichte")
        difficulty (str): Difficult Level ("easy", "medium", "hard")

    Returns:
        dict: Vokabelliste mit Frage, Antwortmöglichkeiten und der richtigen Antwort
    """
    format_prompt = """
    [{
        "question": "Fragetext",
        "options": ["A) Variant 1", "B) Variant 2", "C) Variant 3", "D) Variant 4"],
        "correct_answer": "A",
        "explanation": "Erklärung, warum dies die richtige Antwort ist"
    }]
    """
    prompt = f"""
    Erstelle {num_questions} Quizfragen zum Thema "{topic}" Schwierigkeitsgrad {difficulty}.

    Bitte gebe die Antwort auf JSON-Format in einer Liste mit eine Objekte für jede Frage:
    """
    prompt += format_prompt
    print("Fragen werden geladen...")
    response = openai.ChatCompletion.create(
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content": "Du bist Experte für die Erstellung von Lernquizzen."},
            {"role": "user", "content": prompt}
        ],
    )
    print()

    import json
    quiz_data = json.loads(response.choices[0].message.content)
    return quiz_data


def run_quiz(topic, num_questions=5):
    """
    Startet ein Quiz zu einem bestimmten Thema.

    Args:
        topic (str): Thema des Quizzes
        num_questions (int): How many questions to ask
    """
    print("=" * CONSOLE_WIDTH)
    print(f"🎯 QUIZ: {topic}")
    print("=" * CONSOLE_WIDTH)
    print()

    score = 0

    # Erst Fragen generieren
    quiz_questions = generate_quiz_questions(topic, num_questions)

    for i in range(1, num_questions + 1):
        print(f"Frage {i} von {num_questions}")
        print("-" * CONSOLE_WIDTH)

        # Frage nehmen
        quiz = quiz_questions[i - 1]

        # Frage ausgeben
        print(f"\n{quiz['question']}\n")

        # Wir listen die Antwortmöglichkeiten auf
        for option in quiz['options']:
            print(option)

        # Antwort des Benutzers eingeben
        user_answer = get_user_input("\nIhre Antwort (A/B/C/D): ").strip().upper()

        # Check user´s answer
        if user_answer == quiz['correct_answer']:
            print("✅  Correct!")
            score += 1
        else:
            print(f"❌  Falsch. Richtig ist: {quiz['correct_answer']}")

        # Explanation
        print(f"\n💡 {quiz['explanation']}")
        print("\n" + "=" * CONSOLE_WIDTH + "\n")

    # Result
    if score >= 85:
        print(f"Super! 🏆🏆🏆 Result: {score} von {num_questions} ({score / num_questions * 100:.0f}%)🏆🏆🏆")
        print("=" * CONSOLE_WIDTH)
    elif score < 85:
        print(f"Not bad! Result: {score} von {num_questions} ({score / num_questions * 100:.0f}%)")
        print("=" * CONSOLE_WIDTH)


def run_pink_python_quiz():
    run_quiz("Python Quiz", num_questions=3)
