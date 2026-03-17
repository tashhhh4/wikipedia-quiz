from main2 import random_wikipedia_articles

# test functions
articles = random_wikipedia_articles(10)
for i in range(len(articles)):
    print(f"{i}. {articles[i]["title"]} (content={len(articles[i]["content"])} chars)")