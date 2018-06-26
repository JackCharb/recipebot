#!/usr/bin/env python3

import praw
import os.path
import string
import requests
import random
import binascii
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
    """ Create an instance of Reddit, and create an instance of the food
    subreddit. Load submission id's from replied.txt into replied[].
    """

    global reddit
    global replied
    global subreddit

    # Create an instance of Reddit.
    reddit = praw.Reddit('recipebot')

    # Open the appropriate subreddit.
    subreddit = reddit.subreddit("food")

    # If the file replied.txt exists then load it into
    # replied[].  If it does not exist, initialize
    # replied[] as an empty list.
    if os.path.isfile("replied.txt"):
        with open("replied.txt") as f:
            replied = f.read()
            replied = replied.split("\n")
            replied = list(filter(None, replied))
        f.close()


def find_posts():
    """Find a suitable reddit post and store it as target. Create a recipe
    search query by removing filler words from the target post's title and
    appending ' recipe -reddit -youtube -pinterest'
    """

    global subreddit
    global replied
    global target

    posts = []

    # Search the first 10 hot posts in the subreddit.
    for submission in subreddit.new(limit=10):
        is_image = ("imgur.com/" in submission.url or
                    "i.redd" in submission.url)
        is_simple = (submission.title.count(',') < 2)
        # Save the posts that contain images and haven't already been used.
        if submission.id not in replied and is_image:
            posts.append(submission)
    if len(posts) >= 3:
        # Randomly select one of the valid image posts.
        target = random.choice(posts)
    else:
        quit()
    query = target.title.lower()

    filler = open('filler.txt', 'r')
    for phrase in filler.readlines():
        phrase = phrase.strip('\n')
        if phrase in query:
            query = query.replace(phrase, ' ')
    query = query + " recipe -reddit -youtube -pinterest"
    print(query)
    return query


def find_recipe(query):
    """Use the query to perform a google search. Generate and return a
    valid URL for one of the search results.
    """

    search_URL = "https://www.google.com/search?q=" + query + "&num=5&hl=en"
    try:
        r = requests.get(search_URL)
    except:
        print("Could not reach Google.")
        quit()

    soup = BeautifulSoup(r.text, 'html.parser')
    for result in soup.find_all(class_='g'):
        link = result.find('a', href=True)
        if link is not None:
            link = str(link)
            if link.find("/url?q=") != -1:
                # Cut garbage before link.
                link = link.split('/url?q=', 1)[-1]
                # Cut garbage after link.
                link = link.split('&amp;sa=', 1)[0]
                # Fix ampersands.
                link = link.replace('&amp;', '&')

                valid = ['0', '1', '2', '3', '4', '5', '6', '7',
                         '8', '9', 'a', 'b', 'c', 'd', 'e', 'f',
                         'A', 'B', 'C', 'D', 'E', 'F']

                offset = 0
                # Fix hex encoded special characters.
                for i, char in enumerate(link):

                    if (char is '%' and (link[i + 1 - offset] in valid and
                                         link[i + 2 - offset] in valid)):
                        hex = link[i + 1 - offset] + link[i + 2 - offset]
                        ascii = binascii.unhexlify(hex)
                        link = link.replace("%" + hex, ascii.decode("utf-8"))
                        offset += 2
        try:
            link_res = requests.get(link)
            if (link_res.status_code == 200):
                return link
        except:
            print("Bad URL encontered. Trying next option")
    quit()


def post_recipe(link):
    """Post a comment containing the link as a response to the target post."""

    global target
    target.reply("If you like the look of this food, perhaps you may " +
                 "enjoy this recipe.\n\n" + link + "\n\n*I am a bot, and " +
                 "this action was performed automatically. Please contact " +
                 "my creator or the moderators of this subreddit if you " +
                 "have any questions or concerns.*")
    print("Recipe Posted.")


def finish():
    """The the id of target to replied.txt so that the same post will not
    be replied to when this script runs in the future.
    """

    global target
    with open("replied.txt", "a") as f:
            f.write(target.id + "\n")
    f.close()


if __name__ == '__main__':
    main()
