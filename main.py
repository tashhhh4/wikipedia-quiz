import requests
import bs4
import openai
import wikipedia
import os
from dotenv import load_dotenv



load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


""" import wiki api """
# res = requests.get('https://en.wikipedia.org/w/api.php')
# print(res.json())

# wikiclient.getarticle()
# http://api.wikipedia.org/articles/235235




def number_of_players(num):
    num = int(input("Enter number of players: "))


def print_menu():
    print("\n** Welcome to the Pink Python Quiz **")
    print("1. Python-History")
    print("2. Python-Math")
    print("3. Python-Puzzles")
    print("0. Exit")


def greetin_user():
    print("\n --- Welcome Ninja to the Pink Python Quiz ---")
    user_name = input("Whats your Name: ")
    print(f"Okay Ninja {user_name}, let start the quiz!")

# Schreib eine Funktion, der OpenAI rufen und eine Frage mit antworten generiert.
# Als Return soll die Funktion etwas wie:
# {
#     "question": "What is the question?",
#     "answers": [("text", True), ("text2", False), (etc), (etc)]
# }
def create_question():
    # experimentieren mit den Prompts
    pass


# z.B. hier kannst du suchen "Wie rufe ich OpenAI mit Python" und versuchen
# was du findest hier.
def fetch_openAI(prompt):
    #res = requests.respons(openaiurl, key, etc)
    client = openai.OpenAI()

    response = client.responses.create(
        model="gpt-5-nano",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Analyze the letter and provide a summary of the key points.",
                    },
                    #{
                    #    "type": "input_file",
                    #    "file_url": "https://www.berkshirehathaway.com/letters/2024ltr.pdf",
                    #},
                ],
            },
        ]
    )
    print("client", client)
    print("the response", response.output_text)



def create_questions():
    create_question()


def user_name(user):
    pass


def main():
    user = "Bobby"
    # print(f"Hellow {user}! Welcome to our Lern-Quiz")
    # print_menu()

    fetch_openAI("hello")


if __name__ == "__main__":
    main()