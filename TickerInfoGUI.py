from PyQt5.QtCore import QRect
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QGridLayout, QPushButton,
                             QVBoxLayout,
                             QWidget, QLabel, QScrollArea, QSizePolicy,
                             QSpacerItem, QDialog)
from download_script import Get_DD_Post, get_yesterdays_price, \
    get_current_price, Get_stock_info, URL_dict_duplicates_removed
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as \
    NavigationToolbar
from os import path
from functools import partial
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta, date
import sys


class TickerWindow(QWidget):

    def __init__(self, parent=None):
        # print("opened window")
        super(TickerWindow, self).__init__(parent)
        self.setMinimumSize(1500, 600)
        self.setObjectName("myParentWidget")
        # self.setAttribute(Qt.WA_DeleteOnClose)
        self.basepath = path.dirname(__file__)

        # create graph
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)  # add toolbar
        self.toolbar.setStyleSheet("background-color: white;")
        # self.figure.style.use('dark_background')
        # add icon
        WSBPath = path.abspath(path.join(self.basepath, "WallStreetBets.png"))
        iconPath = path.abspath(path.join(self.basepath, "gorillaicon.jpg"))

        icon = QIcon()
        icon.addPixmap(QPixmap(iconPath),
                       QIcon.Normal, QIcon.On)
        self.setWindowIcon(icon)

        self.WSB_Label = QLabel()
        self.WSB_Label.setGeometry(QRect(0, 0, 371, 121))
        font = QFont()
        # self.label.setAlignment(Qt.AlignTop)
        font.setFamily("Bauhaus 93")
        font.setPointSize(14)
        self.WSB_Label.setFont(font)
        self.WSB_Label.setText("")
        self.WSB_Label.setPixmap(QPixmap(WSBPath))
        self.WSB_Label.setAlignment(Qt.AlignCenter)
        self.WSB_Label.setObjectName("label")

        self.info_button_place = QPushButton("Place")
        self.info_button_place.setStyleSheet("border-color: white;")
        self.info_button_place.setFixedSize(100, 30)

        # making scrollable area
        self.grid = QGridLayout()
        scrollWidget = QWidget()
        # scrollWidget.setLayout(self.grid)
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidget(scrollWidget)

        self.mainLayout = QGridLayout()  # make main layout
        self.mainLayout.setObjectName("mainlayout")  # name main layout
        # self.grid.setObjectName("gridlayout")
        self.setLayout(self.mainLayout)  # set layout of main widget

        ####
        self.verticalLayout = QVBoxLayout()
        self.verticalLayoutWidget = QWidget()
        self.verticalLayoutWidget.setGeometry(QRect(10, 109, 401, 421))
        self.verticalLayoutWidget.setMinimumSize(600, 600)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutWidget.setLayout(self.verticalLayout)

        self.scrollArea2 = QScrollArea()
        self.scrollArea2.setWidgetResizable(True)
        self.scrollArea2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea2.setWidget(self.verticalLayoutWidget)

        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.gridLayout = QVBoxLayout()
        self.gridLayoutWidget = QWidget()
        self.gridLayoutWidget.setGeometry(QRect(601, 110, 391, 421))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayoutWidget.setLayout(self.gridLayout)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        ####

        self.price_place_label = QLabel("")
        self.price_place_label.setFixedHeight(60)
        self.mainLayout.addWidget(self.WSB_Label, 0, 0)
        self.mainLayout.addWidget(self.info_button_place, 0, 1,
                                  alignment=Qt.AlignRight)
        self.gridLayout.addWidget(self.price_place_label)
        self.mainLayout.addWidget(self.scrollArea2, 1, 0)

        self.mainLayout.addWidget(self.gridLayoutWidget, 1, 1)
        self.gridLayout.addWidget(self.canvas)  # add graph to layout
        self.gridLayout.addWidget(self.toolbar)  # add toolbar

        self.setStyleSheet("background-color: black;")

    def tickerWho(self, info):
        print(info)
        try:
            whoDialog = QDialog(self)
            whoDialog.setWindowTitle("Who is $" + info + "?")
            whoDialog.resize(640, 300)
            whoDialog.setContentsMargins(5, 0, 5, 5)
            whoDialog.setStyleSheet("color: white;")
            container = Get_stock_info(info)
            mainlayout = QVBoxLayout()  # mainlayout for diallog box
            whoDialog.setLayout(mainlayout)  # set mainlaout of dialog
            verticalLayoutWidget = QWidget()
            info_label = QLabel(container['longBusinessSummary'])
            info_label.setStyleSheet("color: white; background-color: black; "
                                     "padding :5px; font-size: 9pt;")
            info_label.setAlignment(
                Qt.AlignCenter | Qt.AlignHCenter)

            info_label.setWordWrap(True)
            mainlayout.addWidget(verticalLayoutWidget)
            mainlayout.addWidget(info_label)
            whoDialog.exec_()
        except:  # if no info found
            whoDialog = QDialog(self)
            whoDialog.setWindowTitle("Who is $" + info + "?")
            whoDialog.resize(640, 300)
            whoDialog.setContentsMargins(5, 0, 5, 5)
            whoDialog.setStyleSheet("color: white;")
            mainlayout = QVBoxLayout()  # mainlayout for diallog box
            whoDialog.setLayout(mainlayout)  # set mainlaout of dialog
            verticalLayoutWidget = QWidget()
            info_label = QLabel("Failed to load info!")
            info_label.setStyleSheet("color: white; background-color: black; "
                                     "padding :5px; font-size: 9pt;")
            info_label.setAlignment(
                Qt.AlignCenter | Qt.AlignHCenter)

            info_label.setWordWrap(True)
            mainlayout.addWidget(verticalLayoutWidget)
            mainlayout.addWidget(info_label)
            whoDialog.exec_()

        ###ADD REDDIT INFO###

    def reddit_info(self, ticker):
        self.setWindowTitle("WSBFinScrape: $" + ticker)
        # current price
        try:
            infoButton = self.info_button_place
            infoButton.setText("Who is "+ticker+"?")
            infoButton.clicked.connect(partial(self.tickerWho, info=ticker))
            infoButton.setStyleSheet("QPushButton {border :2px solid "
                                 ";border-color: white; "
                                 "color: blue; background-color: black;} "
                                 "QPushButton::pressed {background-color: "
                                 "grey;}")

            current = get_current_price(ticker)
            past = get_yesterdays_price(ticker)
            # print(current, past)
            if current > past:
                current_label =  self.price_place_label
                current_label.setText(ticker + " $" + str(current))
                current_label.setStyleSheet("color: rgb(0, 204, 0);"
                                             "background-color: black; font-size: "
                                             "14pt;")
                current_label.setAlignment(
                    Qt.AlignRight | Qt.AlignTop)

            elif current < past:
                current_label =  self.price_place_label
                current_label.setText(ticker + " $" + str(current))
                current_label.setStyleSheet("color: rgb(255, 0, 0);"
                                             "background-color: black; font-size: "
                                             "14pt;")
                current_label.setAlignment(
                    Qt.AlignRight | Qt.AlignTop)

            elif current == past:
                current_label =  self.price_place_label
                current_label.setText(ticker + " $" + str(current))
                current_label.setStyleSheet("color: gray;"
                                             "background-color: black; font-size: "
                                             "14pt;")
                current_label.setAlignment(
                    Qt.AlignRight | Qt.AlignTop)
            else: pass

        except:
            current_label = QLabel("!ERROR")
            current_label.setStyleSheet("color: rgb(0, 204, 0);"
                                        "background-color: black; font-size: "
                                        "14pt;")
            self.gridLayout.addWidget(current_label)
            current_label.setAlignment(
                Qt.AlignRight | Qt.AlignTop)

        ###

        today = date.today()
        self.figure.clear()

        try:
            # yf data
            data = yf.download(ticker, period="ytd") #create
            data['Adj Close'].plot()
            plt.xlabel("Date")
            plt.ylabel("Price at Close ($)")
            plt.title(ticker + " Price data from the past Year")

            plt.grid()
            self.canvas.draw()
            plt.style.use('dark_background')
        except:
            print("!ERROR: Year to Date grab failed\n Attempting Month to "
                  "date...")
            try:
                data = yf.download(ticker, start=today,
                                   end=(today - timedelta(weeks=4)))
                data['Adj Close'].plot()
                plt.xlabel("Date")
                plt.ylabel("Price at Close ($)")
                plt.title(ticker + " Price data Month to date")
                plt.style.use('dark_background')
                plt.grid()
                self.canvas.draw()
            except:
                print("Historic data grab failed")

        # print(ticker)
        repeat_url = []
        label_count = 0
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Fixed,
                                 QSizePolicy.Fixed)
        try:
            for item in URL_dict_duplicates_removed[ticker]:
                # print(i)
                # if item in repeat_url:
                #     continue
                label_count += 1
                # joined_url = "".join(i)
                list_make = Get_DD_Post(item)
                # print(list_make)
                title = "".join(list_make["Title"])
                author = "".join(list_make["Author"])
                score = "".join(str(list_make["Score"]))
                # created = "".join(str(list_make["Created"]))
                time_convert = ""
                for timeval in list_make["Created"]:
                    time_convert = datetime.utcfromtimestamp(
                        float(timeval)).strftime('%Y-%m-%d '
                                           '%H:%M:%S')
                url_holder = "".join(list_make["URL"])
                joined_subinfo = title + " --- u/" + author + "  " \
                                                              "Upvotes: "\
                                 + score + " --- Created: " + time_convert
                label_Title = QLabel(joined_subinfo)
                # label_Title = QLabel(joinedstr)
                label_Title.setStyleSheet("color: yellow; "
                                          "background-color: "
                                          "black;font-weight: "
                                          "bold; padding :5px;"
                                          "font-size: 9pt;")
                label_Title.setFixedHeight(60)
                label_Body = QLabel("".join(list_make["Body"]))
                label_Body.setStyleSheet("border :2px solid; "
                                         "border-color: white;"
                                         "color: white; "
                                         "background-color: "
                                         "black;padding :5px; "
                                         "font-size: 8.2pt;")
                label_Title.setWordWrap(True)
                label_Body.setWordWrap(True)
                label_Body.setAlignment(
                    Qt.AlignTop)
                urlLink = "<a href=\"" + str(
                    url_holder) + "\"color: red;\"" + "\">URL: " + str(
                    title) + "</a>"
                url_label = QLabel(str(urlLink))
                url_label.setStyleSheet("border :2px solid; "
                                        "border-color: white;"
                                        "color: yellow; "
                                        "background-color: "
                                        "black;padding :5px; "
                                        "font-size: 8.2pt;")
                url_label.setOpenExternalLinks(True)
                url_label.setMaximumHeight(100)
                # label.setText(urlLink)
                labelset = (Qt.LinksAccessibleByMouse |
                            Qt.TextSelectableByKeyboard |
                            Qt.TextSelectableByMouse)
                label_Title.setTextInteractionFlags(labelset)
                label_Body.setTextInteractionFlags(labelset)
                self.verticalLayout.addWidget(label_Title)
                self.verticalLayout.addWidget(label_Body)
                self.verticalLayout.addWidget(url_label)
                self.verticalLayout.addItem(spacerItem)
                # self.update()
                # repeat_url.append(item)

        except:
            pass
        # print(repeat_url)
        if label_count == 0:
            label_no_posts = QLabel("!ERROR: No Due Diligence posts found for "+
                                    "$"+ticker)
            label_no_posts.setStyleSheet("border :2px solid; "
                                     "border-color: white;"
                                     "color: rgb(255, 0, 0);"
                                     "background-color: black; font-size: "
                                         "8.2pt;")
            self.verticalLayout.addWidget(label_no_posts)
            label_no_posts.setAlignment(
                Qt.AlignCenter | Qt.AlignVCenter)
        else: pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tickerWindow = TickerWindow()
    tickerWindow.show()
    tickerWindow.setAttribute(Qt.WA_DeleteOnClose)
    app.exec_()


