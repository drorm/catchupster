from chatgpt  import OpenAIChat
from comments  import HackerNewsComments

openai_chat = OpenAIChat()

result = openai_chat.chat('5+3')
print("Result: ", result)
