import os
import random
import urllib
import json
import openai
import wikipedia
from wikipedia.exceptions import PageError, DisambiguationError
from dotenv import load_dotenv

# settings
from settings import MAX_ERRORS, PAGE_CONTENT_MIN_LENGTH, TOPICS

# API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key


# OpenAI API Functions

def gpt_nano_reading_exercise(wiki_article_title, wiki_article_content):
    topic = wiki_article_title
    article_text = wiki_article_content

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
    prompt = "The user will prompt you with the title of a Wikipedia article along with some text content from the article. I want you to select a short, readable snippet of about 100-200 words from the article. Create 3 questions about the text, each with 4 possible answers labeled A, B, C, and D. Please structure your response as JSON data that can be used directly in a program to run a reading comprehension quiz, like on the SAT. The output format should look like: " + prompt_format

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
                "content": "Topic: " + topic + "\n" + "Article Text:\n\n" + article_text
            }
        ],
    )

    data = json.loads(response.choices[0].message.content)

    topic = data["topic"]
    reading_text = data["reading_text"]
    questions = data["questions"]

    return topic, reading_text, questions


# Wikipedia API Functions

def get_category_members(category_name):
    url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&list=categorymembers&cmtitle=Category:{category_name}"
    headers = {'User-Agent': 'Mozilla/5.0'}

    request = urllib.request.Request(url, headers=headers)
    response_text = urllib.request.urlopen(request).read()
    data = json.loads(response_text)

    return [member['title'] for member in data['query']['categorymembers']]


def get_random_category_page():
    category = TOPICS[0]
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