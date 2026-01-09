from flask import Flask, render_template, request
from bot import run_reply_bot, run_delete_bot

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        action = request.form.get("action")
        subreddit = request.form.get("subreddit")

        if action == "reply":
            keyword = request.form.get("keyword")
            reply_text = request.form.get("reply_text")
            result = run_reply_bot(subreddit, keyword, reply_text)

        elif action == "delete":
            result = run_delete_bot(subreddit)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
