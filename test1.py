import praw

reddit = praw.Reddit(client_id='LOouFywEuMGZyw',
                     client_secret='SKGdLoAzN3bXjTYeqoQdEHdwOl4BSQ',
                     user_agent='WSBTickScrape')

def Get_DD_Post(url):  # Gets DD post title, body and flair
    post_url = url
    try:
        post = reddit.submission(url=post_url)

        topics_dict = {"Title": [], "Body": [], "Flair": []}

        topics_dict["Title"].append(post.title)
        topics_dict["Body"].append(post.selftext)
        topics_dict["Flair"].append(post.link_flair_text)
        print(topics_dict["Flair"])
    except:
        print("ERROR: Get_DD_Post fail - bad URL: " + str(url))

Get_DD_Post("https://www.")