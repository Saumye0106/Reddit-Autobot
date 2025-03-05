# Reddit Automation Bot

## Video Demo
[Watch the video demo here](https://your-video-url-here)

## Project Description
This project is a Reddit automation bot built using Python and the `praw` library. The bot allows users to interact with Reddit by automating specific tasks related to posts and comments. The key functionalities of the bot include:

1. **Replying to Posts**:
   - The bot scans through the latest posts in a specified subreddit.
   - It checks posts that match a user-defined constraint (case-insensitive keyword or regular expression).
   - If a match is found, the bot replies with a user-specified message and keeps track of replied posts in a file to avoid duplication.

2. **Deleting Replies**:
   - The bot can delete its own comments/replies for specific posts in a subreddit.
   - It checks the history of replies and removes them to maintain a clean comment history.

3. **File Storage**:
   - The bot uses a file `posts_replied_to.txt` to keep track of replied post IDs, ensuring no duplicate interactions with previously replied posts.

## How to Set Up
1. Clone this repository and navigate to the project directory.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up a Reddit application:
   - Visit [Reddit Apps](https://www.reddit.com/prefs/apps).
   - Create a script app and obtain the credentials (`client_id`, `client_secret`, `username`, `password`, `user_agent`).
   - Add these credentials to your `praw.ini` file with the section name `[autobot]`.

## How to Run
1. Start the bot by running the main file:
   ```bash
   python main.py
   ```
2. Follow the prompts:
   - Select whether to reply to posts or delete replies.
   - Provide the subreddit name, constraints, and reply content (if replying to posts).

## Testing
The project includes a comprehensive test suite (`test_main.py`) to ensure reliability.
Run the tests with:
```bash
pytest test_main.py
```

## Tools and Technologies Used
- **Python**: Core programming language.
- **PRAW**: Python Reddit API Wrapper for interacting with Reddit.
- **Unittest and Pytest**: For testing functionalities.

## Features to Consider for Future Enhancements
- Adding functionality to reply to comments.
- Logging system for better debugging and history tracking.
- Improved rate control for APIs using advanced tools.

---
This bot is a simple and effective way to automate interactions on Reddit while respecting the platform's guidelines.