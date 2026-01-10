import unittest
from unittest.mock import patch, mock_open, MagicMock
import cli  # Replace 'cli' with the actual name of your Python file if it's different.


class TestProject(unittest.TestCase):

    @patch("cli.praw.Reddit")
    def test_authenticate_reddit(self, mock_reddit):
        # Mock Reddit instance and user
        mock_user_me = MagicMock()
        mock_user_me.return_value = "test_user"
        mock_reddit.return_value.user.me = mock_user_me

        result = cli.authenticate_reddit()
        mock_reddit.assert_called_once_with("autobot")
        self.assertEqual(result.user.me(), "test_user")

    @patch("builtins.open", new_callable=mock_open, read_data="post1\npost2\n")
    @patch("os.path.isfile", return_value=True)
    def test_load_replied_posts(self, mock_isfile, mock_file):
        result = cli.load_replied_posts("posts_replied_to.txt")
        self.assertEqual(result, ["post1", "post2"])
        mock_file.assert_called_once_with("posts_replied_to.txt", "r")
        mock_isfile.assert_called_once_with("posts_replied_to.txt")

    @patch("builtins.open", new_callable=mock_open)
    def test_save_replied_posts(self, mock_file):
        posts_replied_to = ["post1", "post2", "post2"]  # Duplicates should be removed
        cli.save_replied_posts(posts_replied_to, "posts_replied_to.txt")

        mock_file.assert_called_once_with("posts_replied_to.txt", "w")
        mock_file().write.assert_any_call("post1\n")
        mock_file().write.assert_any_call("post2\n")
        self.assertEqual(mock_file().write.call_count, 2)  # Ensure each line is called once

    @patch("cli.praw.Reddit")
    def test_reply_to_posts(self, mock_reddit):
        # Setup mock subreddit and submission
        mock_reddit_instance = mock_reddit.return_value
        mock_subreddit = MagicMock()
        mock_submission = MagicMock()
        mock_submission.title = "Test post with matching constraint"
        mock_submission.id = "post1"
        mock_submission.reply.return_value = None

        mock_subreddit.hot.return_value = [mock_submission]
        mock_reddit_instance.subreddit.return_value = mock_subreddit

        # Test the function
        posts_replied_to = []
        returned_posts = cli.reply_to_posts(
            mock_reddit_instance, "testsubreddit", "matching", "Test reply", posts_replied_to
        )

        mock_reddit_instance.subreddit.assert_called_once_with("testsubreddit")
        mock_submission.reply.assert_called_once_with("Test reply")
        self.assertIn("post1", returned_posts)

    @patch("cli.praw.Reddit")
    def test_delete_replies(self, mock_reddit):
        # Setup mock Reddit instance
        mock_reddit_instance = mock_reddit.return_value
        mock_reddit_instance.user.me.return_value = "mr_white-009"  # Mock the method to return bot username

        # Setup mock subreddit and submission
        mock_subreddit = MagicMock()
        mock_submission = MagicMock()
        mock_submission.id = "post1"  # Matching ID in posts_replied_to

        # Setup mock comments
        mock_comment = MagicMock()
        mock_comment.author = "mr_white-009"  # Must match mock_reddit_instance.user.me()
        mock_comment.parent_id = "t3_post1"  # Must match format "t3_" + submission.id
        mock_comment.body = "Test comment"

        # Ensure delete is called
        mock_comment.delete.return_value = None

        # Attach mock comments to mock submission
        mock_submission.comments = [mock_comment]
        mock_subreddit.hot.return_value = [mock_submission]
        mock_reddit_instance.subreddit.return_value = mock_subreddit

        # Test the function
        posts_replied_to = ["post1"]
        updated_posts = cli.delete_replies(mock_reddit_instance, "testsubreddit", posts_replied_to)

        # Assertions
        mock_reddit_instance.subreddit.assert_called_once_with("testsubreddit")
        mock_comment.delete.assert_called_once()  # Ensure delete was called
        self.assertNotIn("post1", updated_posts)  # Ensure post1 was removed from the list


    @patch("cli.load_replied_posts", return_value=["post1", "post2"])
    @patch("cli.save_replied_posts")
    @patch("cli.reply_to_posts", return_value=["post1", "post3"])
    @patch("cli.delete_replies", return_value=["post3"])
    def test_cli_reply_workflow(self, mock_delete, mock_reply, mock_save, mock_load):
        # Mock user input
        with patch("builtins.input", side_effect=["1", "testsubreddit", "constraint", "Test reply"]):
            with patch("cli.authenticate_reddit") as mock_auth:
                mock_auth.return_value = MagicMock()
                cli.main()

        mock_auth.assert_called_once()
        mock_load.assert_called_once()
        mock_reply.assert_called_once_with(
            mock_auth.return_value, "testsubreddit", "constraint", "Test reply", ["post1", "post2"]
        )
        mock_save.assert_called_once_with(["post1", "post3"])

    @patch("cli.load_replied_posts", return_value=["post1", "post2"])
    @patch("cli.save_replied_posts")
    @patch("cli.reply_to_posts", return_value=["post1", "post3"])
    @patch("cli.delete_replies", return_value=["post3"])
    def test_cli_delete_workflow(self, mock_delete, mock_reply, mock_save, mock_load):
        # Mock user input
        with patch("builtins.input", side_effect=["2", "testsubreddit"]):
            with patch("cli.authenticate_reddit") as mock_auth:
                mock_auth.return_value = MagicMock()
                cli.main()

        mock_auth.assert_called_once()
        mock_load.assert_called_once()
        mock_delete.assert_called_once_with(
            mock_auth.return_value, "testsubreddit", ["post1", "post2"]
        )
        mock_save.assert_not_called()  # Save is only called when modifying reply data


if __name__ == "__main__":
    unittest.main()
