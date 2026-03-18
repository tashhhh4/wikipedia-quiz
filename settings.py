import os
import openai
from dotenv import load_dotenv

######## Console settings ########
CONSOLE_WIDTH = 43
MARGIN = 4
QUIT_SIGNALS = ['q', 'quit', 'stop', 'leave', 'exit', 'raus', 'clear']

# OpenAI API Key
def load_openai_api_key():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key