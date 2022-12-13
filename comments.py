import requests
import html

class HackerNewsComments:
    # Set the base URL for the Hacker News API
    HACKER_NEWS_API_URL = 'https://hacker-news.firebaseio.com/v0'

    def __init__(self, thread_id):
        self.thread_id = thread_id

    def fetch_comments(self, indent=0):
        # Fetch the details of the thread from the API
        thread_response = requests.get(f'{HACKER_NEWS_API_URL}/item/{self.thread_id}.json')
        thread = thread_response.json()

        # Print the text of the thread
        if 'text' in thread and thread['text']:
            print("\t" * indent, html.unescape(thread['text']))

        # Check if the thread has any comments
        if 'kids' in thread and thread['kids']:
            # Fetch the comments for the thread
            for comment_id in thread['kids']:
                self.fetch_comments(comment_id, indent+1)

# Fetch the comments for the thread with id 33961106
# and print them in a hierarchical manner
hn_comments = HackerNewsComments(33961106)
hn_comments.fetch_comments()
