from main2 import random_wikipedia_articles, get_category_members, print_with_margins

print("running tests.py")

# test functions
#articles = random_wikipedia_articles(2)
#for i in range(len(articles)):
#    print(f"{i}. {articles[i]["title"]} (content={len(articles[i]["content"])} chars)")

#titles = get_category_members("Python_(programming_language)")
#for t in titles:
#    print(t)

print("Normal printed console output.")
print()

text = """Here is some text printed from the print_with_margins(text)
function. It prints the text with extra space to the right
and left so that it sticks out from the other text above and
below it in the console."""

print_with_margins(text)