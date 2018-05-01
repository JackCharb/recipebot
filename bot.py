import praw
import re
import os

# TODO: Try to remove need for importing re and os.

# Create an instance of Reddit
reddit = praw.Reddit('bot1')

# If the file replied.txt exists then load it into
# the replied list. If it does not exist, initialize 
# replied as an empty list.
if not os.path.isfile("replied.txt"):
    replied = []
else:
    with open(replied.txt) as f:
        replied = f.read()
        replied = replied.split("\n")
        replied = list(filter(None, replied))

# Open the appropraite subreddit.
subreddit = reddit.subreddit("pythonforengineers")

# Search the first five hot posts in the subreddit. 
# If the title contains "i love python", reply to
# the post.
for submission in subreddit.hot(limit=5):
    if submission.id not in replied:
        if re.search("i love python", submission.title, re.IGNORECASE):
            submission.reply("Botty McBotface was here.")
            replied.append(submission.id)

# Store the list of replied posts into the replied.txt file
with open("replied.txt", "w") as f:
    for id in replied:
        f.write(id + "\n")
    