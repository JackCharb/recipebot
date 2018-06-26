# recipebot

## A Reddit bot for posting recipes in /r/food.

The subreddit [/r/food](https://www.reddit.com/r/food/) is commonly used for sharing images of food that posters have cooked, eaten, or otherwise encountered out in the wild. Unfortunately, the pictures posted in /r/food rarely include any recipes to instruct viewers about how to recreate the foods that they see. This Python script views posts on /r/food and uses the title of the post to search for a similar recipe on Google. If a similar recipe is found, a link to it is posted as a comment reply to the original image post.

#### Notable Libraries Used

- Praw: Used for creating an instance of Reddit, accessing subreddits, reading posts, and posting replies.
- Requests: Used for submitting a Google search query and obtaining Google's response.
- Beautiful Soup: Used for parsing Google search results, accessing individual results and parsing the URL associated with each result.

#### See it in Action
The results of this script can be view through the post history of [/u/jlcharbonneau](https://www.reddit.com/user/jlcharbonneau) on Reddit.