import praw
import os.path
import re
import requests
import binascii
import string
import random
from bs4 import BeautifulSoup

reddit = None
subreddit = None
target = None
replied = []


def main():
    init()
    query = find_posts()
    link = find_recipe(query)

    post_recipe(link)
    finish()


def init():
    global reddit
    global replied
    global subreddit

    # Create an instance of Reddit
    reddit = praw.Reddit('recipebot')

    # If the file replied.txt exists then load it into
    # the replied list. If it does not exist, initialize
    # replied as an empty list.
    if os.path.isfile("replied.txt"):
        with open("replied.txt") as f:
            replied = f.read()
            replied = replied.split("\n")
            replied = list(filter(None, replied))
        f.close()

    # Open the appropriate subreddit.
    subreddit = reddit.subreddit("food")


def find_posts():
    global subreddit
    global replied
    global target

    posts = []

    # Search the first 10 hot posts in the subreddit.
    for submission in subreddit.hot(limit=10):
        # Save the posts that contain images and haven't already been used
        if submission.id not in replied and ("imgur.com/" in submission.url or "i.redd" in submission.url):
            posts.append(submission)
    if len(posts) >= 3:
        # Randomly select an image posts
        target = random.choice(posts)
    else:
        quit()
    query = target.title.lower()

    filler = open('filler.txt', 'r')
    for phrase in filler.readlines():
        phrase = phrase.strip('\n')
        if phrase in query:
            query = query.replace(phrase, ' ')
    query = query + " recipe -reddit"
    print(query)
    return query


def find_recipe(query):
    search_URL = "https://www.google.com/search?q=" + query + "&num=5&hl=en"
    r = requests.get(search_URL)

    soup = BeautifulSoup(r.text, 'html.parser')
    for result in soup.find_all(class_='g'):
        link = result.find('a', href=True)
        if link is not None:
            link = str(link)
            if link.find("/url?q=") != -1:
                # Cut garbage before link
                link = link.split('/url?q=', 1)[-1]
                # Cut garbage after link
                link = link.split('&amp;sa=', 1)[0]
                # Fix ampersands
                link = re.sub('&amp;', '&', link)

                valid = ['0', '1', '2', '3', '4', '5', '6', '7',
                         '8', '9', 'a', 'b', 'c', 'd', 'e', 'f',
                         'A', 'B', 'C', 'D', 'E', 'F']

                offset = 0
                for i, char in enumerate(link):
                    if char is '%' and link[i + 1 - offset] in valid and link[i + 2 - offset] in valid:
                        hex = link[i + 1 - offset] + link[i + 2 - offset]
                        ascii = binascii.unhexlify(hex)
                        link = re.sub("%" + hex, ascii.decode("utf-8"), link)
                        offset += 2
        link_res = requests.get(link)
        if (link_res.status_code == 200):
            return link
    quit()


def post_recipe(link):
    # global target
    target.reply("If you like the look of this food, perhaps you may " +
                 "enjoy this recipe.\n\n" + link + "\n\n*I am a bot, and " +
                 "this action was performed automatically. Please contact " +
                 "my creator or the moderators of this subreddit if you " +
                 "have any questions or concerns.*")


def finish():
    global target
    # Store the list of replied posts into the replied.txt file
    with open("replied.txt", "a") as f:
            f.write(target.id + "\n")
    f.close()

if __name__ == '__main__':
    main()
