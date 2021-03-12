#! python3
import requests, praw, re, time, io, sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, \
    QLabel, QStyleFactory, QDialog, QGridLayout, QProgressBar,
import yfinance as yf
import matplotlib.pyplot as plt

nasdaq_traded_url = 'http://ftp.nasdaqtrader.com/dynamic/SymDir/nasdaqtraded' \
                    '.txt'
r_traded = requests.get(nasdaq_traded_url, allow_redirects=True)
# open("nasdaq_traded_list.txt", "wb").write(r_traded.content)

nasdaq_listed_url = 'http://ftp.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt'
r_listed = requests.get(nasdaq_listed_url, allow_redirects=True)
# open("nasdaq_traded_list.txt", "wb").write(r_listed.content)


reddit = praw.Reddit(client_id='LOouFywEuMGZyw', #starts reddit instance
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
        WSB_data += " [" + submission.link_flair_text + "] "
    except:
        pass
    WSB_data += submission.url
    # submission.title
    # parse_file.write(submission.title)
    # topics_dict["score"].append(submission.score)
    # topics_dict["id"].append(submission.id)
    # topics_dict["url"].append(submission.url)
    # topics_dict["comms_num"].append(submission.num_comments)
    # topics_dict["created"].append(submission.created)
    # topics_dict["body"].append(submission.selftext)


print("Complete!\n")
time.sleep(1)
new_tickers = re.findall(r'\b(?<=\$)[A-Z]{1,5}\b', WSB_data)


dict_new_tickers ={}
yahooFin_str = ""

for i in new_tickers:
    if i in dict_new_tickers: #check if ticker already been added and counted
        continue
    if re.search(rf'(\|){i}(\|)', r_traded.text) == None:#check found pattern
        # is in nasdaq traded list, if not skip.
        if re.search(rf'{i}(\|)', r_listed.text) == None:#check found pattern
            # is in nasdaq listed list, if not skip.
            continue #check against download list
    num_tick = new_tickers.count(i)#count how many occurance of ticker.
    dict_new_tickers.update({i:num_tick})#append ticker to dictionary along
    # with value of counted occurances.
    yahooFin_str += i + " "

yahooFin_tickers = yf.Tickers(yahooFin_str)

sort_tickers = sorted(dict_new_tickers.items(), key=lambda x: x[1],
                     reverse=True)

print(sort_tickers)


WSB_io = io.StringIO(WSB_data)#Makes string act like file for iterable lines.
URL_dict = {} #

#Find what tickers have Due Diligience, build further to add URL links to DD
# for each ticker in GUI
for i in WSB_io:
    for ticker in new_tickers:
        if re.search(rf'{ticker}', i):
            if re.search((r'\bDD\b'), i):
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
print(URL_dict)

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

#TURN INTO DEFINITION - PASS TICKER UPON BUTTON PRESS.
data = yf.download(list(dict.fromkeys(new_tickers)), period="ytd") #create
# list from dict as it removes duplicates
# data['Adj Close'].plot()
# plt.xlabel("Date")
# plt.ylabel("Adjusted")
# plt.title("Ticker Price data")
# plt.style.use('dark_background')
# plt.grid()
# plt.show()

class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.originalPalette = QApplication.palette()

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createBottomLeftTabWidget()
        self.createBottomRightGroupBox()
        self.createProgressBar()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0)
        mainLayout.addWidget(self.bottomRightGroupBox, 2, 1)
        mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)

        timer = QTimer(self)
        timer.timeout.connect(self.advanceProgressBar)
        timer.start(1000)

if __name__ == '__main__':
    gallery = WidgetGallery()
    gallery.show()
    # sys.exit(WidgetGallery.app.exec())