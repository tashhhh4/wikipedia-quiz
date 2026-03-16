import requests
import bs4
import openai
import wikipedia
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


""" import wiki api """
# res = requests.get('')
# print(res.json())


def get_question(thema):
    pass


def greeting(user):
    pass


def number_of_players(num):
    pass


def user_name(user):
    pass


def main():
    user = "Bobby"
    print(f"Hellow {user}! Welcome to our Lern-Quiz")


if __name__ == "__main__":
    main()