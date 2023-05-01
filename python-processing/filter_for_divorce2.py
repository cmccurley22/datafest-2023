# jun 1 2016
# jan 9 2022
from my_secrets import secret, id, user_agent

import praw
import pprint
import pandas as pd

reddit = praw.Reddit(
    client_id = id,
    client_secret = secret,
    user_agent = user_agent
)

subreddit = reddit.subreddit("legaladvice")

i = 0
d = {
    "title": [],
    "text": []
}

saving_replies = []

word_list = ["divorce", "custody", "separati", "seperati", "alimony", "child support", " ex ", "prenup"]

for submission in reddit.subreddit("legaladvice").top(limit = 500):
    if any([word in submission.selftext for word in word_list]):
        try:
            saving_replies.append("\n".join([comment.body for comment in submission.comments]))
        except:
            pass
        # d["title"].append(submission.title)
        # d["text"].append(submission.selftext)
    # print(submission.title)
    # pprint.pprint(vars(submission))

# df = pd.DataFrame(data = d)
# df.to_csv("new500comments.csv")
# print(df)

with open("top500comments", "w") as f:
    f.writelines(saving_replies)