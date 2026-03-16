import os
from dotenv import load_dotenv
import openai

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key


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
def run_quiz(topic, num_questions=5):
    """
    Startet ein Quiz zu einem bestimmten Thema.

    Args:
        topic (str): Thema des Quizzes
        num_questions (int): How many questions to ask
    """
    print("=" * 50)
    print(f"🎯 QUIZ: {topic}")
    print("=" * 50)
    print()

    score = 0

    for i in range(1, num_questions + 1):
        print(f"Frage {i} von {num_questions}")
        print("-" * 50)

        # Frage generieren
        quiz = generate_quiz_question(topic)

        # Frage ausgeben
        print(f"\n{quiz['question']}\n")

        # Wir listen die Antwortmöglichkeiten auf
        for option in quiz['options']:
            print(option)

        # Antwort des Benutzers eingeben
        user_answer = input("\nIhre Antwort (A/B/C/D): ").strip().upper()

        # Check user´s answer
        if user_answer == quiz['correct_answer']:
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Falsch. Richtig ist: {quiz['correct_answer']}")

        # Explanation
        print(f"\n💡 {quiz['explanation']}")
        print("\n" + "=" * 50 + "\n")

    # Result
    print(f"🏆 Result: {score} von {num_questions} ({score / num_questions * 100:.0f}%)")
    print("=" * 50)


if __name__ == "__main__":
    run_quiz("Python Quiz", num_questions=3)