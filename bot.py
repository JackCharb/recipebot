import praw
import pdb
import re
import os



reddit = praw.Reddit('bot1')

if not os.path.isfile("replied.txt"):
    replied = []
else:
    with open(replied.txt) as f:
        replied = f.read()
        replied = replied.split("\n")
        replied = list(filter(None, replied))

subreddit = reddit.subreddit("pythonforengineers")

for submission in subreddit.hot(limit=5):
    if submission.id not in replied:
        if re.search("i love python", submission.title, re.IGNORECASE):
            submission.reply("Botty McBotface was here.")
            replied.append(submission.id)

with open("replied.txt", "w") as f:
    for id in replied:
        f.write(id + "\n")
    