import os

import requests
import praw

print(os.getcwd())

def do_bot_stuff():
    r = praw.Reddit('bot1')

    subreddit = r.subreddit("all")
    for submission in subreddit.hot(limit=5):
        print(submission)

if __name__ == '__main__':
    do_bot_stuff()