import requests
import pandas as pd

subreddit = "legaladvice"
limit = 200
timeframe = "all"
listing = "top"

def get_reddit(subreddit, listing, limit, timeframe):
    try:
        base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}'
        request = requests.get(base_url, headers = {'User-agent': 'yourbot'})
    except:
        print('An Error Occured')
    return request.json()

r = get_reddit(subreddit, listing, limit, timeframe)

print(len(r))

with open("big_data.txt", "w") as f:
    f.write(str(r))

def get_post_titles(r):
    post_titles = []
    for post in r["data"]["children"]:
        x = post["data"]["title"]
        post_titles.append(x)
    return post_titles

def get_posts(r):
    posts = {}
    for post in r["data"]["children"]:
        t = post["data"]["title"]
        body = post["data"]["selftext"]
        posts[t] = body
    return posts

def get_post_data(r, keyword):
    d = {
        "title": [],
        "text": [],
        # "flairs": []
    }

    for post in r["data"]["children"]:
        post_d = post["data"]
        if keyword in post_d["selftext"]:
            d["title"].append(post_d["title"])
            d["text"].append(post_d["selftext"])
        # d["flairs"].append(post_d["link_flair_text"])

    return d


# print(get_post_titles(r))

# print(r["data"]["children"][0]["data"])

d = get_post_data(r, "divorce")
df = pd.DataFrame(data = d)

df.to_csv("test.csv")