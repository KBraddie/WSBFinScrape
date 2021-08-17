#! python3
import sys, re
from pandas import read_excel, Series
from os import path, execl
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QGridLayout,
                             QMenuBar, QPushButton, QVBoxLayout, QWidget,
                             QLabel,
                             QScrollArea, QSystemTrayIcon, QDialog, QSlider,
                             QMessageBox)
from functools import partial
from download_script import sort_tickers, \
    count_DD_posts, data_save_tickers, tickerPriceData, string_list

from TickerInfoGUI import TickerWindow

class OpenWindow: #opens ticker window with reddit posts
    def handleTickerbutton(self, data):
        try:
            self.tickerObject = TickerWindow()
            self.tickerObject.show()
            self.tickerObject.reddit_info(data)
        except: print("!ERROR: OpenWindow class failed.")

class MainWindow(QWidget): #Main application GUI

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.check_previous_data = 0
        self.previous_tickers = []
        self.basepath = path.dirname(__file__) #relative path

        if getattr(sys, 'frozen', False):
            # path of files changes if run as exe or script
            application_path = path.dirname(sys.executable)
        else:
            application_path = self.basepath

        try:
            historicPath = path.abspath(path.join(application_path,
                                                  "WSBhistoric_data.xlsx"))
            df = read_excel(historicPath)
            for tick in df[0]:
                self.previous_tickers.append(tick)
            self.check_previous_data = 1
            # print(self.previous_tickers)
        except: print("No previous data found")

        self.setWindowTitle("WSBFinScrape")
        self.setFixedSize(555, 620)
        self.setObjectName("myParentWidget")

        #create menu bar
        self.menubar = QMenuBar()
        self.menubar.setObjectName("menubar")
        supportMenu = self.menubar.addMenu("Support the Developer")
        supportMenu.addAction("Donate a Coffee", self.on_triggered_support)
        settingsMenu = self.menubar.addMenu("Settings")
        settingsMenu.addAction("Config", self.on_triggered_config)
        settingsMenu.addAction("Restart", self.restart)
        self.menubar.setStyleSheet("color: white;font-weight: bold;")
        self.menubar.setLayoutDirection(Qt.RightToLeft)


        # add window icon
        iconPath = path.abspath(path.join(self.basepath,"gorillaicon.jpg"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(iconPath), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.trayIcon = QSystemTrayIcon(QtGui.QIcon(iconPath), self)
        self.trayIcon.show()

        #add WSB logo
        WSBPath = path.abspath(path.join(self.basepath, "WallStreetBets.png"))
        self.WSBlabel = QLabel()
        self.WSBlabel.setAlignment(QtCore.Qt.AlignCenter |
                                   QtCore.Qt.AlignVCenter)
        self.WSBlabel.setText("")
        self.WSBlabel.setPixmap(QtGui.QPixmap(WSBPath))
        # self.label.setAlignment(Qt.AlignCenter)
        self.WSBlabel.setObjectName("label")

        # making scrollable area
        self.grid = QGridLayout()
        scrollwidget = QWidget()
        scrollwidget.setLayout(self.grid)
        scrollarea = QScrollArea()
        scrollarea.setWidgetResizable(True)
        scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollarea.setWidget(scrollwidget)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setObjectName("mainlayout")
        self.grid.setObjectName("gridlayout")

        self.mainLayout.addWidget(self.menubar)
        self.mainLayout.addWidget(self.WSBlabel)
        self.mainLayout.addWidget(scrollarea)

        self.setLayout(self.mainLayout)

        self.setStyleSheet("background-color: black;")

        labelstyle = "color: white; background-color: " \
                     "black; font-size: 8.2pt; font-weight: bold;"
        titleticker = QLabel("Ticker")
        titlePostCount = QLabel("#Mentions")
        titleStockPrice = QLabel("Current Price")
        titleDDcount = QLabel("#DD Posts")
        self.grid.addWidget(titlePostCount, 0, 1)
        self.grid.addWidget(titleStockPrice, 0, 2)
        self.grid.addWidget(titleticker, 0, 0)
        self.grid.addWidget(titleDDcount, 0, 3)
        titleticker.setStyleSheet(labelstyle)
        titleStockPrice.setStyleSheet(labelstyle)
        titlePostCount.setStyleSheet(labelstyle)
        titleDDcount.setStyleSheet(labelstyle)

        titlePostCount.setFixedSize(100, 30)
        titleticker.setFixedSize(160, 30)
        titleStockPrice.setFixedSize(100, 30)
        titleDDcount.setFixedSize(100, 30)

        titlePostCount.setAlignment(QtCore.Qt.AlignCenter |
                                    QtCore.Qt.AlignVCenter)
        titleStockPrice.setAlignment(QtCore.Qt.AlignCenter |
                                     QtCore.Qt.AlignVCenter)
        titleticker.setAlignment(QtCore.Qt.AlignCenter |
                                 QtCore.Qt.AlignVCenter)
        titleDDcount.setAlignment(QtCore.Qt.AlignCenter |
                                 QtCore.Qt.AlignVCenter)
        self.createTickButtons(mapping=sort_tickers)


    def createTickButtons(self, mapping):
        x = 0
        y = 0
        for key, value in mapping:
            # self.buttons.append(QPushButton(key))
            x += 1
            # y += 1
            button = QPushButton("$" + key)
            self.grid.addWidget(button, x, y)
            ticker_ob = OpenWindow()
            button.clicked.connect(partial(ticker_ob.handleTickerbutton,
                                           data=key))

            button.setFixedSize(160, 30)
            if self.check_previous_data == 1:
                if key not in self.previous_tickers:
                    button.setStyleSheet("QPushButton {border :2px solid "
                                         ";border-color: cyan; "
                                         "color: cyan; background-color: black;} "
                                         "QPushButton::pressed {background-color: "
                                         "grey;}")
                else:
                    button.setStyleSheet("QPushButton {border :2px solid "
                                     ";border-color: white; "
                                     "color: yellow; background-color: black;} "
                                     "QPushButton::pressed {background-color: "
                                     "grey;}")
            else: button.setStyleSheet("QPushButton {border :2px solid "
                                     ";border-color: white; "
                                     "color: yellow; background-color: black;} "
                                     "QPushButton::pressed {background-color: "
                                     "grey;}")

            button.setFont(QtGui.QFont('Times', 8))
            # button.set
            # self.buttons[-1].setFixedSize(40, 80)
            label = QLabel(str(value))
            self.grid.addWidget(label, x, 1)
            label.setStyleSheet("border :2px solid; color: yellow; "
                                "background-color: black;")
            label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

            try:
                label_DD_post = QLabel(str(count_DD_posts[key]))
                self.grid.addWidget(label_DD_post, x, 3)
                label_DD_post.setStyleSheet("border :2px solid; color: yellow; "
                                    "background-color: black;")
                label_DD_post.setAlignment(QtCore.Qt.AlignCenter |
                                      QtCore.Qt.AlignVCenter)
            except:
                label_DD_post = QLabel("0")
                self.grid.addWidget(label_DD_post, x, 3)
                label_DD_post.setStyleSheet("border :2px solid; color: yellow; "
                                            "background-color: black;")
                label_DD_post.setAlignment(QtCore.Qt.AlignCenter |
                                           QtCore.Qt.AlignVCenter)
        self.tickerPrice()
        self.dump_ticker_data()


    def tickerPrice(self):
        x = 0
        # today = datetime.date.today()
        for string_key in string_list:
            x += 1
            yest_container = float("{:.2f}".format(tickerPriceData[
                                                       string_key].iloc[0][
                                                       "Close"]))
            today_container = float("{:.2f}".format(tickerPriceData[
                                                        string_key].iloc[1][
                                                        "Close"]))
            price_label = QLabel("$ " + str(today_container))
            self.grid.addWidget(price_label, x, 2)
            price_label.setAlignment(
                QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

            if today_container > yest_container:#Higher
                price_label.setStyleSheet("color: rgb(0,204,0); "
                                       "background-color: "
                                       "black;font-weight: bold")
            elif today_container < yest_container:#Lower
                price_label.setStyleSheet("color: rgb(255, 0, 0"
                                          "); background-color: "
                                          "black;font-weight: bold")
            #USE A SINGLE LABEL AND JUST SET STYLE SHEET
            elif today_container == yest_container:#Neutral
                price_label.setStyleSheet("color: white; background-color: "
                                          "black;font-weight: bold")
            else:
                error_label = price_label
                error_label.setText("!ERROR")
                error_label.setStyleSheet("color: grey; background-color: "
                                          "black;font-weight: bold")

        created_label = QLabel("created by Nebulezz")

        created_label.setStyleSheet("color: red; font-size: 8.2pt; "
                                    "font-weight: bold; font: italic;")
        created_label.setAlignment(
            QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.mainLayout.addWidget(created_label)

    def dump_ticker_data(self):
        # create excel of tickers to check against in the future.
        ticker_dump = []
        for ticker in data_save_tickers:
            if ticker in ticker_dump:
                continue
            else:
                ticker_dump.append(ticker)
        historicDump = Series(ticker_dump)
        historicDump.to_excel('WSBhistoric_data.xlsx')


    def restart(self):#RESTARTS APPLICATION WITH INTERMEDIATE MESSAGEBOX
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Restart Application?")
        msgBox.setWindowTitle("Restart")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            execl(sys.executable, sys.executable, *sys.argv)

    @QtCore.pyqtSlot()
    def on_triggered_support(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://www.paypal.com/biz/fund?id=E34JBGHTN3DFJ"))

    @QtCore.pyqtSlot()
    def on_triggered_config(self):#TRIGGERED CONFIG MENU ACTION
        if getattr(sys, 'frozen', False):
            # path of files changes if run as exe or script
            application_path = path.dirname(sys.executable)
        else:
            application_path = self.basepath

        configPath = path.abspath(path.join(application_path,"WSBconfig.txt"))
        configRead = open(configPath, "r")
        configlist = re.findall(r'\d+', configRead.read())
        configval = configlist[0]

        def saveFile():#SAVES SELECTED NUMBER OF POSTS TO FILE
            configfile = open(configPath, "w")
            configfile.write("#Posts to read: " + str(sld.value()))
            print("Post count changed to: ", sld.value())
            configfile.close()

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Post Count Saved!")
            msgBox.setWindowTitle("Info")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()



        #CREATES DIALOG FOR CHANGING SETTINGS
        whoDialog = QDialog(self)
        whoDialog.setWindowTitle("Number of Posts to Read?")
        whoDialog.setFixedSize(350, 230)
        whoDialog.setContentsMargins(5, 0, 5, 5)
        whoDialog.setStyleSheet("color: white;")
        mainlayout = QGridLayout()  # mainlayout for diallog box
        whoDialog.setLayout(mainlayout)  # set mainlayout of dialog
        verticalLayoutWidget = QWidget()

        info_label = QLabel("WARNING! Increasing the post read amount "
                            "will increase app load time.")
        changes_label = QLabel("Restart app to see changes take affect.")
        saveButton = QPushButton("Save")
        saveButton.setStyleSheet("QPushButton {color: white; "
                                 "background-color: black; "
                                 "padding :5px; font-size: 9pt; border: 2px "
                                 "solid; border-color: white;}"
                                 "QPushButton::pressed {background-color: grey;}")
        number_label = QLabel(str(configval))
        number_label.setStyleSheet("color: white; background-color: black; "
                                 "padding :5px; font-size: 9pt;")
        number_label.setAlignment(
            QtCore.Qt.AlignCenter | QtCore.Qt.AlignHCenter)

        #CREATES A SLIDER FOR PICKING POST NUMBER
        sld = QSlider(Qt.Horizontal)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setMinimum(100)
        sld.setMaximum(1000)
        sld.setTickPosition(QSlider.TicksAbove)
        sld.setTickInterval(100)
        sld.setSingleStep(10)
        sld.setValue(int(configval))

        number_label.setWordWrap(True)
        info_label.setWordWrap(True)
        # changes_label.setWordWrap(True)
        mainlayout.addWidget(verticalLayoutWidget)
        mainlayout.addWidget(info_label, 0, 0, 2, 0)
        mainlayout.addWidget(number_label, 2, 2)
        mainlayout.addWidget(saveButton, 2, 3)
        mainlayout.addWidget(sld, 3, 0, 2, 0)
        mainlayout.addWidget(changes_label, 4, 0, 2, 0)

        def updateValue(value):
            number_label.setText(str(value))

        sld.valueChanged.connect(updateValue)#UPDATES LABEL WITH SLIDER VALUE
        saveButton.clicked.connect(saveFile)#CONNECTS TO SAVE FUNCTION
        whoDialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindowObj = MainWindow()
    mainWindowObj.show()
    app.exec_()