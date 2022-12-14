import requests
import settings

# Fetch the top stories from the Hacker News API
response = requests.get(f'{settings.HACKER_NEWS_API}/topstories.json')
top_story_ids = response.json()

# Keep track of how many threads have been displayed so far
thread_count = 0

# Print the title and first comment of each top story
for story_id in top_story_ids:
    # Stop when 10 threads have been displayed
    if thread_count >= settings.MAXIMUM_THREADS:
        break

    # Fetch the details of the story from the API
    story_response = requests.get(f'{settings.HACKER_NEWS_API}/item/{story_id}.json')
    story = story_response.json()

    # Check if the story has MINIMUM_SCORE points or more
    if story['score'] < settings.MINIMUM_SCORE:
        continue

    print (' ====================')
    # Print the title of the story
    print (thread_count+1, story['title'])
    print ('------------')

    # Fetch the details of the first comment for the story from the API
    comment_response = requests.get(f'{settings.HACKER_NEWS_API}/item/{story["kids"][0]}.json')
    comment = comment_response.json()

    # Print the text of the first comment
    if 'text' in comment and comment['text']:
        print(comment['text'])

    # Increment the thread count
    thread_count += 1
