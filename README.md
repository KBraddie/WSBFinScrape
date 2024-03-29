# WSBFinScrape

WSBFinScrape is a Reddit scraper for r/WallStreetBets, designed to keep you up-to-date on the subreddits current hottest stock, with related Due Diligence posts, historic stock data and stock infomation all in one easy to read place. All written in Python using PyQT5, yfinance and PRAW.

Breakdown:

* Counts the number of each ticker mentions in the last [100-1000] posts and produces a list sorted high to low.

* Finds related Due Diligence posts for each ticker in the list.

* Displays the Stock ticker, number of mentions, current price and number of Due Dligience posts found in an easy to read table format. All stock information is downloaded from Yahoo Finance.

* Each Ticker can be clicked to open a new window, displaying all related Due Diligence posts, URL links to the posts, Year-to-Date price data and a button to download the description of the stock.

* Tickers found are stored in memory and checked against when the App is next run. Any Tickers that haven't been previously found are highlighed in Cyan to highlight them as New.

## Images
![Loading Splash Screen](https://github.com/Nebulezz/WSBFinScrape/blob/master/Images/1%20-%20kBzXJ9f.png?raw=true)

![Main screen/Ticker list](https://github.com/Nebulezz/WSBFinScrape/blob/master/Images/2%20-%207eRJ7B5.png?raw=true)

![Ticker post and Stock analysis](https://github.com/Nebulezz/WSBFinScrape/blob/master/Images/3%20-%20WtJZpXe.png?raw=true)

![Post URL](https://github.com/Nebulezz/WSBFinScrape/blob/master/Images/4%20-%209JwJrAk.png?raw=true)

![Stock information pop-up](https://github.com/Nebulezz/WSBFinScrape/blob/master/Images/5%20-%20D1IkuE1.png?raw=true)

## Installation

1. Download all the files from github and place them in a single folder.
2. Install the 6 Python packages using the code below in cmd (Python needs to be installed and added to your system PATH). 
```bash
pip install openpyxl praw yfinance pandas PyQT5 matplotlib
```
3. Run the App by running the mainGUI.py file with Python.

Continue on to package the code as a single runnable application if desired.

4. Install pyinstaller using the code below in cmd
```bash
pip install pyinstaller
```
5. Navigate to the directory containing the files downloaded from github and type "cmd" in the file explorer adress bar, which should bring up cmd starting at that directory.
6. Copy and paste the below code into cmd and pyinstaller should begin packaging the code. This should take around 5 minutes, and once complete the .exe will be placed in the dist folder in your directory.
```bash
pyinstaller --onefile --name WSBFinScrape --clean --noconsole --add-data gorillaicon.jpg;. --add-data WallStreetBets.png;. --icon=gorillaicon_UrM_icon.ico mainGUI.py
```

Alternatively a pre packaged exe can be downloaded in "Releases".

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
