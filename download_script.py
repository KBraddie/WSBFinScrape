import praw, re, io, datetime, sys
from requests import get
import yfinance as yf
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from os import path

###Create Splash Screen###

app = QApplication(sys.argv)
basepath = path.dirname(__file__)
WSBPath = path.abspath(path.join(basepath, "WallStreetBets.png"))

splash = QLabel()
layout = QVBoxLayout()
splash.setLayout(layout)
splash.setFixedSize(390, 200)
splash.setPixmap(QPixmap(WSBPath))

splash.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint |
                      Qt.AnchorHorizontalCenter | Qt.AnchorVerticalCenter |
                      Qt.WindowStaysOnTopHint)

loadingLabel = QLabel("Financial Scraper\nLoading...")

layout.addWidget(loadingLabel)
loadingLabel.setAlignment(Qt.AlignCenter |
                          Qt.AlignBottom)
labelstyle = "color: black; font-size: 9pt; font-weight: bold;"

loadingLabel.setStyleSheet(labelstyle)
splash.show()

###Splash Screen End###

nasdaq_traded_url = 'http://ftp.nasdaqtrader.com/dynamic/SymDir/nasdaqtraded' \
                    '.txt'
r_traded = get(nasdaq_traded_url, allow_redirects=True)
# open("nasdaq_traded_list.txt", "wb").write(r_traded.content)

nasdaq_listed_url = 'http://ftp.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt'
r_listed = get(nasdaq_listed_url, allow_redirects=True)
# open("nasdaq_traded_list.txt", "wb").write(r_listed.content)

print("Downloading Reddit data...\n")


# reddit = praw.Reddit(client_id='LOouFywEuMGZyw', #starts reddit instance
#                  client_secret='SKGdLoAzN3bXjTYeqoQdEHdwOl4BSQ',
#                  user_agent='WSBTickScrape')

reddit = praw.Reddit(
    client_id="o-_iA1WAMA0I_Q",
    client_secret="aSLs_NLBruh5JQ4hufl4O8tPiFWiQw",
    user_agent="WSBFinScrape",
    check_for_updates=False,
    comment_kind="t1",
    message_kind="t4",
    redditor_kind="t2",
    submission_kind="t3",
    subreddit_kind="t5",
    trophy_kind="t6",
    oauth_url="https://oauth.reddit.com",
    reddit_url="https://www.reddit.com",
    short_url="https://redd.it",
    ratelimit_seconds = 5,
    timeout = 16,
)

WSBsub = reddit.subreddit("wallstreetbets")

if getattr(sys, 'frozen', False):
    # path of files changes if run as exe or script
    application_path = path.dirname(sys.executable)
else:
    application_path = basepath

configPath = path.abspath(path.join(application_path,
                                    "WSBconfig.txt"))
try:
    configfile = open(configPath, "r")
    configfile.close()
except:
    print("no config file found, config file created")
    configfile = open(configPath, "w")
    configfile.write("#Posts to read: 300")
    configfile.close()

configRead = open(configPath, "r")
configlist = re.findall(r'\d+', configRead.read())
configval = configlist[0]
configRead.close()

# scrape_WSB = WSBsub.new(limit=None)
scrape_WSB = WSBsub.new(limit=int(configval)) #Reduce post download size for
# testing

WSB_data = ""

print("Analysiing WSB...\n")

for submission in scrape_WSB:
    WSB_data = WSB_data + "\n" + submission.title
    try:
        WSB_data += " [" + submission.link_flair_text + "] "
    except:
        pass
    WSB_data += submission.url


print("Complete!\n")

# new_tickers = re.findall(r'\b(?<=\$)[A-Z]{1,5}\b', WSB_data)
new_tickers_unsorted = re.findall(r'\b(?<=\$)[A-Z]{1,5}\b|\b\$?[A-Z]{3,5}\b',
                                  WSB_data)

print(new_tickers_unsorted)

new_tickers = []

for ticker_element in new_tickers_unsorted:
    if ticker_element == "YOLO":
        continue
    if "$" in "".join(ticker_element):
        new_tickers.append("".join(ticker_element).replace("$",""))
    else: new_tickers.append("".join(ticker_element))

dict_new_tickers ={}
data_save_tickers = []
data_black_list = []
print(new_tickers)

# yahooFin_str = ""

# Count ticker mentions
for i in new_tickers:
    if i in data_black_list:
        print("In black list, skipped:", i)
        continue
    if i in dict_new_tickers.keys(): #check if ticker already been added and counted
        continue
    if re.search(rf'\b(\|){i}(\|)\b', r_traded.text) == None:#check found
        # pattern
        # is in nasdaq traded list, if not skip.
        if re.search(rf'\b{i}(\|)\b', r_listed.text) == None:#check found
            # pattern
            # is in nasdaq listed list, if not skip.
            print(i," not found - removed")
            data_black_list.append(i)
            new_tickers.remove(i)
            continue #check against download list
    data_save_tickers.append(i)
    num_tick = new_tickers.count(i)#count how many occurance of ticker.
    dict_new_tickers.update({i:num_tick})#append ticker to dictionary along
    # with value of counted occurances.

sort_tickers = sorted(dict_new_tickers.items(), key=lambda x: x[1],
                     reverse=True)
string_list = []
for tickerI, valI in sort_tickers:
    string_list.append(tickerI)
sorted_string = " ".join(string_list)

print(sort_tickers)
tickerCurrent_Price = {}
tickerYesterdays_Price = {}



def get_ticker_prices(symbols):#gets current and yesterday price of ticker
    data = yf.download(tickers=symbols,period="2d",group_by='ticker',
                       auto_adjust=True,prepost=True,threads=True)
    return data

tickerPriceData = get_ticker_prices(sorted_string)

def get_current_price(symbol):#gets current price of ticker
    try:
        ticker = yf.Ticker(symbol)
        todays_data = ticker.history(period='1d')
        data = todays_data['Close'][0]
        print(symbol, "data collected")
        return float("{:.2f}".format(data))
    except:
        print("Error retrieving", symbol)
        return 0

print("Getting current stock data \n")

# for key, value in sort_tickers:
#     try:
#         current_data = get_current_price(key)
#         tickerCurrent_Price.update({key : current_data})
#     except:
#         print("Error with:" + key)


print("Done! \n")

def get_yesterdays_price(symbol): #gets yesterdays price of ticker
    ticker = yf.Ticker(symbol)
    today = datetime.date.today()
    print("Collecting historic data for:", symbol)
    try:
        if datetime.datetime.today().weekday() == 5:
            yesterday = today - datetime.timedelta(days = 2)
            yesterdays_data = ticker.history(start=yesterday, end=today)
            data = yesterdays_data['Close'][0]
            return float("{:.2f}".format(data))
        elif datetime.datetime.today().weekday() == 6:
            yesterday = today - datetime.timedelta(days = 3)
            yesterdays_data = ticker.history(start=yesterday, end=today)
            data = yesterdays_data['Close'][0]
            return float("{:.2f}".format(data))
        elif datetime.datetime.today().weekday() == 0:
            yesterday = today - datetime.timedelta(days = 3)
            yesterdays_data = ticker.history(start=yesterday, end=today)
            data = yesterdays_data['Close'][0]
            return float("{:.2f}".format(data))
        else:
            yesterday = today - datetime.timedelta(days = 1)
            yesterdays_data = ticker.history(start=yesterday, end=today)
            data = yesterdays_data['Close'][0]
            # print(yesterday, today)
            return float("{:.2f}".format(data))
    except:
        print("Failed with: "+ symbol)
        return 0


print("Getting historic stock data \n")

# for key, value in sort_tickers:
#     yesterday_data = get_yesterdays_price(str(key))
#     tickerYesterdays_Price.update({key : yesterday_data})


print("Done! \n")


# print("todays " + str(tickerCurrent_Price))
# print("yesterdays " + str(tickerYesterdays_Price))

WSB_io = io.StringIO(WSB_data)#Makes string act like file for iterable lines.
URL_dict = {}


for i in WSB_io:
    for ticker in new_tickers:
        if len(ticker) < 2: #stops single character ticker causing pull of
            # all posts to ticker
            # print("In character control with:", ticker)
            if re.search(rf'\b(?<=\$){ticker}\b', i):
                if "[DD]" in i:
                    if ticker in URL_dict.keys():
                        URL_dict[ticker].append(re.findall(
                            'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|'
                            '(?:%[0-9a-fA-F][0-9a-fA-F]))+', i))
                        continue
                    else:
                        URL_dict.update({ticker: re.findall(
                            'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|'
                            '(?:%[0-9a-fA-F][0-9a-fA-F]))+', i)})
                        continue
                else:
                    continue
            else:
                continue
        # (r'\b(?<=\$)[A-Z]{1,5}\b'
        if ticker in i:
        # if re.search(rf'\b(?<=\$){ticker}\b', i):
            # (r'\b(?<=\$)[A-Z]{1,5}\b'
            if "[DD]" in i:
                if ticker in URL_dict.keys():
                    URL_dict[ticker].append(re.findall(
                        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|'
                        '(?:%[0-9a-fA-F][0-9a-fA-F]))+',i))
                else:URL_dict.update({ticker:re.findall(
                        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|'
                        '(?:%[0-9a-fA-F][0-9a-fA-F]))+',i)})
                # collects all URLs for tickers that have DD, pass to
                # Get_DD_Posts for GUI
        else:
            continue

# print(URL_dict)

#Prep URL_dict_diplicates_removed with URL_dict keys
URL_dict_duplicates_removed = {}
for keys in URL_dict.keys():
    URL_dict_duplicates_removed.update({keys:[]})
# print(URL_dict_duplicates_removed)

#Remove duplicates from URL_dict
for key_ticker, item in URL_dict.items():
        for subitem in item:
            listcheck = URL_dict_duplicates_removed[key_ticker]
            if "".join(subitem) in listcheck:
                continue
            else: URL_dict_duplicates_removed[key_ticker].append("".join(subitem))

#count how many DD posts of each ticker
count_DD_posts = {}
for keys_ticker, urls in URL_dict_duplicates_removed.items():
    count_DD_posts.update({keys_ticker : len(urls)})

print(count_DD_posts)

print(URL_dict_duplicates_removed)

def Get_DD_Post(url):  # Gets DD post title, body and flair
    post_url = url
    try:
        print("Downloading from reddit URL: ", url)
        post = reddit.submission(url=post_url)

        topics_dict = {"Title": [], "Body": [], "Flair": [], "Author": [],
                       "Score": [], "URL":[], "Created":[]}
        topics_dict["Title"].append(post.title)
        topics_dict["Body"].append(post.selftext)
        topics_dict["Flair"].append(post.link_flair_text)
        topics_dict["Author"].append(str(post.author))
        topics_dict["Score"].append(post.score)
        topics_dict["URL"].append(post.url)
        topics_dict["Created"].append(post.created_utc)

        print("Done")
        return topics_dict
    except:
        print("ERROR: Get_DD_Post fail - bad URL: " + str(url))

def Get_stock_info(ticker):
    infoContainer = yf.Ticker(ticker)
    return infoContainer.info

#close splash screen
splash.close()

