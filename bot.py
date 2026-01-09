import praw
import re
import os
import time


def authenticate_reddit():
    reddit = praw.Reddit("autobot")
    print(f"Authenticated as: {reddit.user.me()}")
    return reddit


def load_replied_posts(file_path="posts_replied_to.txt"):
    if not os.path.isfile(file_path):
        return []

    with open(file_path, "r") as f:
        posts_replied_to = f.read().split("\n")
        return list(filter(None, posts_replied_to))  # Remove empty strings


def save_replied_posts(posts_replied_to, file_path="posts_replied_to.txt"):
    with open(file_path, "w") as f:
        for post_id in set(posts_replied_to):  # Remove duplicates (if any)
            f.write(post_id + "\n")

def run_reply_bot(subreddit_name, constraint, reply_text):
    reddit = authenticate_reddit()
    posts_replied_to = load_replied_posts()

    subreddit = reddit.subreddit(subreddit_name)

    reply_count = 0

    for submission in subreddit.hot(limit=10):
        if submission.id not in posts_replied_to and re.search(constraint, submission.title, re.IGNORECASE):
            submission.reply(reply_text)
            posts_replied_to.append(submission.id)
            reply_count += 1
            time.sleep(10)

    save_replied_posts(posts_replied_to)

    return f"Replied to {reply_count} posts successfully."


def run_delete_bot(subreddit_name):
    reddit = authenticate_reddit()
    posts_replied_to = load_replied_posts()

    subreddit = reddit.subreddit(subreddit_name)
    updated_posts = posts_replied_to[:]

    delete_count = 0

    for submission in subreddit.hot(limit=None):
        if submission.id in posts_replied_to:
            for comment in submission.comments:
                if comment.author == reddit.user.me() and comment.parent_id.split("_")[-1] == submission.id:
                    try:
                        comment.delete()
                        updated_posts.remove(submission.id)
                        delete_count += 1
                    except:
                        pass

    save_replied_posts(updated_posts)

    return f"Deleted replies from {delete_count} posts."