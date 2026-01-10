import praw

reddit = praw.Reddit("autobot")
print("Logged in as:", reddit.user.me())
