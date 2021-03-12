#! python3
import requests
import praw
import re
import time
import io

nasdaq_traded_url = 'http://ftp.nasdaqtrader.com/dynamic/SymDir/nasdaqtraded' \
                    '.txt'
r_traded = requests.get(nasdaq_traded_url, allow_redirects=True)
# open("nasdaq_traded_list.txt", "wb").write(r_traded.content)

nasdaq_listed_url = 'http://ftp.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt'
r_listed = requests.get(nasdaq_listed_url, allow_redirects=True)
# open("nasdaq_traded_list.txt", "wb").write(r_listed.content)


reddit = praw.Reddit(client_id='LOouFywEuMGZyw',
                     client_secret='SKGdLoAzN3bXjTYeqoQdEHdwOl4BSQ',
                     user_agent='WSBTickScrape')

WSBsub = reddit.subreddit("wallstreetbets")

scrape_WSB = WSBsub.new(limit=None)

# topics_dict = { "title":[], \
#                 # "score":[], \
#                 # "id":[], "url":[], \
#                 # "comms_num": [], \
#                 # "created": [], \
#                 "body":[]}

# parse_file = open("Download.txt", "w", encoding="utf-8")
WSB_data = ""

print("Analysiing WSB...")

for submission in scrape_WSB:
    WSB_data = WSB_data + "\n" + submission.title
    try:
        WSB_data = WSB_data + " [" + submission.link_flair_text + "]"
    except:
        pass

print(WSB_data)

s = io.StringIO(WSB_data)
for line in s:
    print(line)