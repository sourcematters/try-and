import logging
import threading
import time

import requests
import praw

logging.basicConfig(level=logging.INFO)

def do_bot_stuff():
    while True:
        comments = 0
        rate_limit_seconds = 60
        previous_comment_ids = []
        reddit = praw.Reddit('bot')

        # Grab all the Recent Comments in every subreddit. 
        # This will return 100 of the newest comments on Reddit
        for result in reddit.subreddit('all').comments():

            # The comment
            body = result.body.lower()

            # Get the Comment ID
            comment_id = result.id  
            
            # Check if we already replied to this comment
            if comment_id not in previous_comment_ids:
                # Search for phrase
                if body.find(' try and ') != -1:
                    previous_comment_ids.append(comment_id)

                    try:
                        # Reply to the comment
                        result.reply('try to* 😇')

                        logging.info(f"Replied to post: {result.link_permalink}")
                    except praw.exceptions.RedditAPIException as api_exc:
                        rate_limit_seconds *= 10  # Add 10 minutes to retry
                        logging.exception(f"Backing off retry frequency due to rate limit: [{rate_limit_seconds} seconds]")
                    except Exception as e:
                        logging.exception(e)
            comments += 1

        logging.info(f"Completed analyzing [{comments}] comments")
        time.sleep(rate_limit_seconds)

if __name__ == '__main__':
    thread = threading.Thread(name='ReplyThread', target=do_bot_stuff)
    thread.daemon = True
    thread.start()

    # Make main thread wait until bot thread "finishes"
    thread.join()