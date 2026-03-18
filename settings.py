######## Program settings #########
# If 10 exceptions occur while retrieving random articles, give up.
MAX_ERRORS = 10
# Skip articles that are too short for quiz generation.
PAGE_CONTENT_MIN_LENGTH = 1000
# The quiz is in English.
LANG = "EN"
# Wikipedia Page Categories the excerpts can come from.
TOPICS = ["Python_(programming_language)"]
# Length of the practice test.
NUM_EXERCISES = 1

######## Console settings ########
CONSOLE_WIDTH = 43
MARGIN = 4
QUIT_SIGNALS = ['q', 'quit', 'stop', 'leave', 'exit', 'raus', 'clear']