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


def reply_to_posts(reddit, subreddit_name, constraint, reply_text, posts_replied_to):
    subreddit = reddit.subreddit(subreddit_name)

    for submission in subreddit.hot(limit=10):
        print(f"Checking post: {submission.title}")
        # Only reply if constraint matches and post hasn't been replied to already
        if submission.id not in posts_replied_to and re.search(constraint, submission.title, re.IGNORECASE):
            print("Found a match!")
            submission.reply(reply_text)
            print("Bot replied to:", submission.title)
            posts_replied_to.append(submission.id)
            time.sleep(10)  # Sleep to avoid hitting API rate limits

    return posts_replied_to


def delete_replies(reddit, subreddit_name, posts_replied_to):
    subreddit = reddit.subreddit(subreddit_name)
    updated_posts_replied_to = posts_replied_to[:]  # Create a copy of the list

    for submission in subreddit.hot(limit=None):
        if submission.id in posts_replied_to:
            print("Checking post:", submission.title)
            reply_deleted = False  # Track if any reply was deleted for this submission

            for comment in submission.comments:
                if comment.author == reddit.user.me() and comment.parent_id.split("_")[-1] == submission.id:
                    print(f"Deleting comment: {comment.body}")
                    try:
                        comment.delete()
                        print("Reply deleted successfully!")
                        reply_deleted = True
                    except Exception as e:
                        print(f"Error occurred while deleting comment: {e}")

            if reply_deleted:
                # Remove submission ID from the list after successfully deleting its replies
                updated_posts_replied_to.remove(submission.id)

    # Save updated list back to the file
    save_replied_posts(updated_posts_replied_to)
    print("Updated posts_replied_to list saved.")
    return updated_posts_replied_to


def   main():
    # Authenticate the bot
    reddit = authenticate_reddit()

    # Load replied posts
    posts_replied_to = load_replied_posts()

    # Ask the user what they want to do
    action = input("What would you like to do? (1: Reply to posts, 2: Delete replies): ").strip()

    if action == "1":
        # Reply to posts
        subname = input("Enter subreddit name (case sensitive): ")
        constraint = input("Enter Post filter constraint: ")
        reply_text = input("Enter your reply: ")
        posts_replied_to = reply_to_posts(reddit, subname, constraint, reply_text, posts_replied_to)
        save_replied_posts(posts_replied_to)
    elif action == "2":
        # Delete replies
        subname = input("Enter subreddit name (case sensitive): ")
        posts_replied_to = delete_replies(reddit, subname, posts_replied_to)
    else:
        print("Invalid option. Please choose 1 or 2.")


if __name__ == "__main__":
    main()