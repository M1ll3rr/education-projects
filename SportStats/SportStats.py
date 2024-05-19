import os
import sys
from bs4 import BeautifulSoup as bs
import asyncio
import aiohttp
import httplib2
import json
from datetime import datetime
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import pandas as pd
import lxml
# чтобы иконка приложения отображалась на панели задач
import ctypes
myappid = 'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(1100, 750)
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        MainWindow.setFont(font)
        MainWindow.setWindowTitle("Спорт статистика")
        MainWindow.setWindowFilePath("")
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setDockNestingEnabled(False)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.sport_name = QtWidgets.QComboBox(self.centralwidget)
        self.sport_name.setGeometry(QtCore.QRect(192, 90, 165, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.sport_name.setFont(font)
        self.sport_name.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.sport_name.setToolTip("")
        self.sport_name.setInputMethodHints(QtCore.Qt.ImhNone)
        self.sport_name.setCurrentText("")
        self.sport_name.setObjectName("sport_name")
        self.champ_name = QtWidgets.QComboBox(self.centralwidget)
        self.champ_name.setGeometry(QtCore.QRect(625, 90, 400, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.champ_name.setFont(font)
        self.champ_name.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.champ_name.setToolTip("")
        self.champ_name.setInputMethodHints(QtCore.Qt.ImhNone)
        self.champ_name.setCurrentText("")
        self.champ_name.setObjectName("champ_name")
        self.sport_label = QtWidgets.QLabel(self.centralwidget)
        self.sport_label.setGeometry(QtCore.QRect(210, 30, 130, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.sport_label.setFont(font)
        self.sport_label.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
        self.sport_label.setToolTip("")
        self.sport_label.setText("Вид спорта")
        self.sport_label.setTextFormat(QtCore.Qt.AutoText)
        self.sport_label.setAlignment(QtCore.Qt.AlignCenter)
        self.sport_label.setObjectName("sport_label")
        self.champ_label = QtWidgets.QLabel(self.centralwidget)
        self.champ_label.setGeometry(QtCore.QRect(785, 30, 80, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.champ_label.setFont(font)
        self.champ_label.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
        self.champ_label.setToolTip("")
        self.champ_label.setText("Турнир")
        self.champ_label.setTextFormat(QtCore.Qt.AutoText)
        self.champ_label.setAlignment(QtCore.Qt.AlignCenter)
        self.champ_label.setObjectName("champ_label")
        self.begin_label = QtWidgets.QLabel(self.centralwidget)
        self.begin_label.setGeometry(QtCore.QRect(180, 170, 190, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.begin_label.setFont(font)
        self.begin_label.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
        self.begin_label.setToolTip("")
        self.begin_label.setText("Начало выборки")
        self.begin_label.setTextFormat(QtCore.Qt.AutoText)
        self.begin_label.setAlignment(QtCore.Qt.AlignCenter)
        self.begin_label.setObjectName("begin_label")
        self.end_label = QtWidgets.QLabel(self.centralwidget)
        self.end_label.setGeometry(QtCore.QRect(735, 170, 180, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.end_label.setFont(font)
        self.end_label.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
        self.end_label.setToolTip("")
        self.end_label.setText("Конец выборки")
        self.end_label.setTextFormat(QtCore.Qt.AutoText)
        self.end_label.setAlignment(QtCore.Qt.AlignCenter)
        self.end_label.setObjectName("end_label")
        self.parse_button = QtWidgets.QPushButton(self.centralwidget)
        self.parse_button.setGeometry(QtCore.QRect(435, 650, 230, 40))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(14)
        font.setKerning(True)
        self.parse_button.setFont(font)
        self.parse_button.setToolTip("")
        self.parse_button.setText("Получить данные")
        self.parse_button.setShortcut("")
        self.parse_button.setCheckable(False)
        self.parse_button.setChecked(False)
        self.parse_button.setAutoRepeat(False)
        self.parse_button.setObjectName("parse_button")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(260, 660, 150, 20))
        self.progressBar.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.team1_lable = QtWidgets.QLabel(self.centralwidget)
        self.team1_lable.setGeometry(QtCore.QRect(180, 320, 190, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.team1_lable.setFont(font)
        self.team1_lable.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
        self.team1_lable.setToolTip("")
        self.team1_lable.setText("Выбор команд")
        self.team1_lable.setTextFormat(QtCore.Qt.AutoText)
        self.team1_lable.setAlignment(QtCore.Qt.AlignCenter)
        self.team1_lable.setObjectName("team1_lable")
        self.team2_label = QtWidgets.QLabel(self.centralwidget)
        self.team2_label.setGeometry(QtCore.QRect(150, 550, 250, 71))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.team2_label.setFont(font)
        self.team2_label.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
        self.team2_label.setToolTip("")
        self.team2_label.setText("2-я команда для сравнения (необязательно)")
        self.team2_label.setTextFormat(QtCore.Qt.AutoText)
        self.team2_label.setScaledContents(False)
        self.team2_label.setAlignment(QtCore.Qt.AlignCenter)
        self.team2_label.setWordWrap(True)
        self.team2_label.setObjectName("team2_label")
        self.team1_name = QtWidgets.QComboBox(self.centralwidget)
        self.team1_name.setGeometry(QtCore.QRect(135, 380, 280, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.team1_name.setFont(font)
        self.team1_name.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.team1_name.setToolTip("")
        self.team1_name.setInputMethodHints(QtCore.Qt.ImhNone)
        self.team1_name.setCurrentText("")
        self.team1_name.setObjectName("team1_name")
        self.team2_name = QtWidgets.QComboBox(self.centralwidget)
        self.team2_name.setGeometry(QtCore.QRect(135, 500, 280, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.team2_name.setFont(font)
        self.team2_name.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.team2_name.setToolTip("")
        self.team2_name.setInputMethodHints(QtCore.Qt.ImhNone)
        self.team2_name.setCurrentText("")
        self.team2_name.setObjectName("team2_name")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(605, 320, 440, 261))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox.setFont(font)
        self.groupBox.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.groupBox.setToolTip("")
        self.groupBox.setTitle("Параметры статистики")
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName("groupBox")
        self.stat_check1 = QtWidgets.QCheckBox(self.groupBox)
        self.stat_check1.setGeometry(QtCore.QRect(20, 54, 190, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(False)
        self.stat_check1.setFont(font)
        self.stat_check1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.stat_check1.setToolTip("")
        self.stat_check1.setText("")
        self.stat_check1.setShortcut("")
        self.stat_check1.setTristate(False)
        self.stat_check1.setObjectName("stat_check1")
        self.stat_check2 = QtWidgets.QCheckBox(self.groupBox)
        self.stat_check2.setGeometry(QtCore.QRect(20, 131, 190, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.stat_check2.setFont(font)
        self.stat_check2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.stat_check2.setToolTip("")
        self.stat_check2.setText("")
        self.stat_check2.setObjectName("stat_check2")
        self.stat_check3 = QtWidgets.QCheckBox(self.groupBox)
        self.stat_check3.setGeometry(QtCore.QRect(20, 208, 190, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.stat_check3.setFont(font)
        self.stat_check3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.stat_check3.setToolTip("")
        self.stat_check3.setText("")
        self.stat_check3.setObjectName("stat_check3")
        self.stat_check4 = QtWidgets.QCheckBox(self.groupBox)
        self.stat_check4.setGeometry(QtCore.QRect(240, 54, 190, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(False)
        self.stat_check4.setFont(font)
        self.stat_check4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.stat_check4.setToolTip("")
        self.stat_check4.setText("")
        self.stat_check4.setShortcut("")
        self.stat_check4.setTristate(False)
        self.stat_check4.setObjectName("stat_check4")
        self.stat_check5 = QtWidgets.QCheckBox(self.groupBox)
        self.stat_check5.setGeometry(QtCore.QRect(240, 131, 190, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(False)
        self.stat_check5.setFont(font)
        self.stat_check5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.stat_check5.setToolTip("")
        self.stat_check5.setText("")
        self.stat_check5.setShortcut("")
        self.stat_check5.setTristate(False)
        self.stat_check5.setObjectName("stat_check5")
        self.stat_check6 = QtWidgets.QCheckBox(self.groupBox)
        self.stat_check6.setGeometry(QtCore.QRect(240, 208, 190, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(False)
        self.stat_check6.setFont(font)
        self.stat_check6.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.stat_check6.setToolTip("")
        self.stat_check6.setText("")
        self.stat_check6.setShortcut("")
        self.stat_check6.setTristate(False)
        self.stat_check6.setObjectName("stat_check6")
        self.graph_button = QtWidgets.QPushButton(self.centralwidget)
        self.graph_button.setGeometry(QtCore.QRect(760, 650, 241, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.graph_button.setFont(font)
        self.graph_button.setText("Показать статистику")
        self.graph_button.setObjectName("graph_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1100, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.sport_name.setCurrentIndex(-1)
        self.team1_name.setCurrentIndex(-1)
        self.team2_name.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        pass


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    sport_list = ["Футбол", "Хоккей", "Баскетбол", "Волейбол", "Гандбол", "Теннис"]

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Спорт статистика")
        self.setWindowIcon(QtGui.QIcon('imgs/balle-sport.png'))

        self.sport_name.addItems(self.sport_list)
        self.sport_name.setItemIcon(0, QtGui.QIcon('imgs/football.png'))
        self.sport_name.setItemIcon(1, QtGui.QIcon('imgs/hockey.png'))
        self.sport_name.setItemIcon(2, QtGui.QIcon('imgs/basketball.png'))
        self.sport_name.setItemIcon(3, QtGui.QIcon('imgs/volleyball.png'))
        self.sport_name.setItemIcon(4, QtGui.QIcon('imgs/handball.png'))
        self.sport_name.setItemIcon(5, QtGui.QIcon('imgs/tennis.png'))
        self.sport_name.setCurrentIndex(-1)

        self.date_begin = QtWidgets.QDateEdit(self)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setFamily("Nirmala UI")
        self.date_begin.setFont(font)
        self.date_begin.setCalendarPopup(True)
        self.date_begin.setGeometry(QtCore.QRect(202, 230, 142, 40))

        self.date_end = QtWidgets.QDateEdit(self)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setFamily("Nirmala UI")
        self.date_end.setFont(font)
        self.date_end.setCalendarPopup(True)
        self.date_end.setGeometry(QtCore.QRect(752, 230, 142, 40))

        font = QtGui.QFont()
        font.setPointSize(10)
        self.stat_check_all = QtWidgets.QCheckBox(self)
        self.stat_check_all.setFont(font)
        self.stat_check_all.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.stat_check_all.setToolTip("")
        self.stat_check_all.setText("Выбрать все")
        self.stat_check_all.setObjectName("stat_check_all")
        self.stat_check_all.setGeometry(QtCore.QRect(765, 600, 120, 20))

        self.date_begin.setDate(QtCore.QDate.currentDate())
        self.date_begin.setMaximumDate(QtCore.QDate(datetime.now().year, datetime.now().month, datetime.now().day - 1))
        self.date_begin.setMinimumDate(QtCore.QDate(datetime.now().year - 10, datetime.now().month, datetime.now().day))
        self.date_end.setDate(QtCore.QDate.currentDate())
        self.date_end.setMaximumDate(QtCore.QDate(datetime.now().year, datetime.now().month, datetime.now().day - 1))
        self.date_end.setMinimumDate(QtCore.QDate(datetime.now().year - 10, datetime.now().month, datetime.now().day))

        self.champ_name.setHidden(True)
        self.groupBox.setHidden(True)
        self.progressBar.setHidden(True)
        self.team1_name.setHidden(True)
        self.team2_name.setHidden(True)
        self.team2_label.setHidden(True)
        self.graph_button.setHidden(True)
        self.stat_check_all.setHidden(True)

        self.graph_window = pg.GraphicsLayoutWidget(title="График")
        #self.graph_window.setBackground('w')
        self.graph_window.resize(1600, 950)
        self.graph_window.ci.setBorder()
        self.graph_window.setWindowTitle('График полученной статистики')
        self.graph_window.setWindowIcon(QtGui.QIcon('imgs/balle-sport.png'))
        self.sport = ''
        self.champ = ''
        self.team1 = ''
        self.team2 = ''

        self.addFunctions()

    def addFunctions(self):
        self.sport_name.currentTextChanged.connect(lambda: self.sport_update())
        self.sport_name.currentTextChanged.connect(lambda: self.take_champs())
        self.sport_name.currentTextChanged.connect(lambda: self.graph_button.setHidden(True))
        self.sport_name.currentTextChanged.connect(lambda: self.team1_name.clear())
        self.sport_name.currentTextChanged.connect(lambda: self.show_team2(True))
        self.sport_name.currentTextChanged.connect(lambda: self.show_statistic_param())

        self.champ_name.currentTextChanged.connect(lambda: self.champ_update())
        self.champ_name.currentTextChanged.connect(lambda: self.graph_button.setHidden(True))
        self.champ_name.currentTextChanged.connect(lambda: self.team1_name.clear())
        self.champ_name.currentTextChanged.connect(lambda: self.show_team2(True))

        self.date_begin.dateChanged.connect(lambda: self.graph_button.setHidden(True))
        self.date_end.dateChanged.connect(lambda: self.graph_button.setHidden(True))

        self.team1_name.currentTextChanged.connect(lambda: self.team1_update())
        self.team1_name.currentTextChanged.connect(lambda: self.show_team2(False))
        self.team2_name.currentTextChanged.connect(lambda: self.team2_update())

        self.stat_check_all.clicked.connect(lambda: self.stat_select_all())

        self.parse_button.clicked.connect(lambda: self.parse_data())

        self.graph_button.clicked.connect(lambda: self.build_graph())

    def take_champs(self):
        self.champ_name.clear()
        with open("data.json", "r") as file:
            data = json.load(file)
        self.champ_name.addItems(data[self.sport_name.currentText()].keys())
        self.champ_name.setHidden(False)

    def take_teams(self, data):
        team_list = []
        date_list = self.get_date()
        self.team1_name.clear()
        self.team2_name.clear()

        for key in data[self.sport_name.currentText()][self.champ_name.currentText()]:
            if key in date_list:
                for team in data[self.sport_name.currentText()][self.champ_name.currentText()][key]:
                    team_list.append(team)
        team_list = sorted(list(set(team_list)))
        if len(team_list) == 0:
            self.showDialog("За выбранный период нет соревнований")
        else:
            if 'id_list' in team_list:
                team_list.remove('id_list')
            self.team1_name.addItems(team_list)
            self.team2_name.addItems(team_list)

            for i in range(len(team_list)):
                self.team1_name.setItemIcon(i, QtGui.QIcon(f'imgs/team_logo/{team_list[i]}.png'))
                self.team2_name.setItemIcon(i, QtGui.QIcon(f'imgs/team_logo/{team_list[i]}.png'))
            self.team1_name.setHidden(False)

            self.team2_name.insertItem(0, "Не выбрано")
            self.team2_name.setCurrentIndex(0)
            if self.champ == "КХЛ":
                self.stat_check5.setText("Силовые приемы")
                self.stat_check5.setHidden(False)
            else:
                if self.stat_check5.text() == "Силовые приемы":
                    self.stat_check5.setChecked(False)
                    self.stat_check5.setHidden(True)



    def show_team2(self, value):
        self.graph_button.setHidden(value)
        self.team2_name.setHidden(value)
        self.team2_label.setHidden(value)

    def parse_data(self):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        self.progressBar.setHidden(False)
        date_list = self.get_date()
        with open('data.json', 'r', encoding="utf-8") as file:
            data = json.load(file)
        self.progressBar.setValue(0)

        self.total_parse = 0
        self.count_parse = 0
        try:
            asyncio.run(self.gather_matches(data, date_list))
        except:
            self.showDialog("Плохое соединение, попробуйте снова")
        try:
            asyncio.run(self.gather_stat_data(data))
        except:
            self.showDialog("Плохое соединение, попробуйте снова")
        self.progressBar.setValue(100)
        self.progressBar.setHidden(True)

        data[self.sport] = dict(sorted(data[self.sport].items()))
        data[self.sport][self.champ] = dict(sorted(data[self.sport][self.champ].items()))

        with open("data.json", "w") as file:
            json.dump(data, file)

        self.take_teams(data)

    def get_date(self):
        self.date_end.date()
        start_date = datetime(self.date_begin.date().year(), self.date_begin.date().month(),
                              self.date_begin.date().day())
        end_date = datetime(self.date_end.date().year(), self.date_end.date().month(), self.date_end.date().day())
        res = pd.date_range(
            min(start_date, end_date),
            max(start_date, end_date)
        ).strftime('%d-%m-%Y').tolist()
        return res

    def show_statistic_param(self):

        self.stat_check1.setChecked(False)
        self.stat_check2.setChecked(False)
        self.stat_check3.setChecked(False)
        self.stat_check4.setChecked(False)
        self.stat_check5.setChecked(False)
        self.stat_check6.setChecked(False)
        self.stat_check_all.setChecked(False)

        if self.sport == "Футбол":
            self.stat_check1.setText("Владение мячом")
            self.stat_check2.setText("Всего ударов")
            self.stat_check3.setText("Ударов в створ")
            self.stat_check4.setText("Угловые")
            self.stat_check5.setText("Офсайды")
            self.stat_check6.setText("Нарушения")
            self.stat_check5.setHidden(False)
            self.stat_check6.setHidden(False)
            self.groupBox.setHidden(False)
            self.stat_check_all.setHidden(False)

        elif self.sport == "Хоккей":
            self.stat_check1.setText("Броски в створ")
            self.stat_check2.setText("Голы в большинстве")
            self.stat_check3.setText("Штрафное время")
            self.stat_check4.setText("Голы по периодам")
            self.stat_check5.setHidden(True)
            self.stat_check6.setHidden(True)
            self.groupBox.setHidden(False)
            self.stat_check_all.setHidden(False)

        else:
            self.groupBox.setHidden(True)
            self.stat_check_all.setHidden(True)


    def get_base_stat(self, data, date_list, team_key):
        titles = []
        give = []  # забито
        get = []  # пропущено
        odds_win = []
        odds_draw = []
        for date in date_list:
            if date in data[self.sport][self.champ]:
                if team_key in data[self.sport][self.champ][date]:
                    title = date + '\n' + data[self.sport][self.champ][date][team_key]["Cоперник"] + '\n' \
                             + data[self.sport][self.champ][date][team_key]["Статус"]
                    if "Исход" in data[self.sport][self.champ][date][team_key]:
                        title += ' ' + 'в' + ' ' + data[self.sport][self.champ][date][team_key]["Исход"]
                        if data[self.sport][self.champ][date][team_key]["Исход"] == 'П':
                            title += ' (' + str(data[self.sport][self.champ][date][team_key]["П забито"]) \
                                     + ':' + str(data[self.sport][self.champ][date][team_key]["П пропущено"]) + ')'
                    sum_score = data[self.sport][self.champ][date][team_key]["Забито"] + data[self.sport][self.champ][date][team_key]["Пропущено"]
                    if sum_score % 2 == 0:
                        title += f'\nВсего {sum_score} (чёт)'
                    else:
                        title += f'\nВсего {sum_score} (нечёт)'
                    titles.append(title)
                    give.append(data[self.sport][self.champ][date][team_key]["Забито"])
                    get.append(-data[self.sport][self.champ][date][team_key]["Пропущено"])
                    if "К победы" in data[self.sport][self.champ][date][team_key]:
                        odds_win.append(data[self.sport][self.champ][date][team_key]["К победы"])
                    else:
                        odds_win.append(0)
                    if "К ничьи" in data[self.sport][self.champ][date][team_key]:
                        odds_draw.append(data[self.sport][self.champ][date][team_key]["К ничьи"])
                    else:
                        odds_draw.append(0)

        return give, get, odds_win, odds_draw, titles

    def get_stat(self, data, date_list, team_key, stat_key):
        # date_arr = []
        stat_arr = []
        titles = []

        for date in date_list:
            if date in data[self.sport][self.champ]:
                if team_key in data[self.sport][self.champ][date]:
                    if stat_key in data[self.sport][self.champ][date][team_key]["Статистика"]:
                        titles.append(data[self.sport][self.champ][date][team_key]["Cоперник"] + '\n' + date)
                        stat_arr.append(data[self.sport][self.champ][date][team_key]["Статистика"][stat_key])
                    elif stat_key in data[self.sport][self.champ][date][team_key]:
                        titles.append(data[self.sport][self.champ][date][team_key]["Cоперник"] + '\n' + date)
                        stat_arr.append(data[self.sport][self.champ][date][team_key][stat_key])
        return np.arange(len(stat_arr)), np.array(stat_arr), titles

    def build_graph(self):
        if self.team1_name.currentText() == self.team2_name.currentText():
            self.showDialog("Выберите две разные команды или одну")
            return
        with open("data.json", "r") as file:
            data = json.load(file)

        date_list = np.array(self.get_date())
        params = self.stat_params()
        self.graph_window.clear()
        pg.setConfigOptions(antialias=True)

        give, get, odds_win, odds_draw, titles = self.get_base_stat(data, date_list, self.team1)
        x = np.arange(len(give))

        p0 = self.graph_window.addPlot(col=1, colspan=2)
        p0.setTitle(f'Игры {self.team1} с {date_list[0]} по {date_list[-1]}', **{'color': '#FFF', 'size': '14pt'})
        p0.addLegend()
        p0.showGrid(y=True)
        p0.showAxis('bottom', False)

        bar_give = pg.BarGraphItem(x=x, width=0.2, stepMode="center", height=give, pen='w', brush=(0,255,0), name='Забито')
        p0.addItem(bar_give)
        bar_get = pg.BarGraphItem(x=x, width=0.2, stepMode="center", height=get, pen='w', brush=(248,0,0), name='Пропущено')
        p0.addItem(bar_get)

        ow = p0.plot(x=x, y=odds_win, pen=pg.mkPen((31,174,233),width=3), symbolBrush=(31,174,233), name='К на победу', symbol='o')
        od = p0.plot(x=x, y=odds_draw, pen=pg.mkPen((234,230,202),width=3), symbolBrush=(234,230,202), name='К на ничью', symbol='o')

        for i in range(len(give)):
            if titles[i].find("Победа") > 0:
                fill = (0, 255, 0, 90)
            elif titles[i].find("Поражение") > 0:
                fill = (248,0,0,90)
            else:
                fill = (234,230,202,90)
            text = pg.TextItem(text=f'{titles[i]}', anchor=(0.5, -0.2), angle=0, border='w', fill=fill)
            text.setColor((0,0,0))

            p0.addItem(text)
            text.setPos(i, get[i])

        if self.team2 == "Не выбрано":
            self.graph_window.resize(1600, 980)
        else:
            if len(params) > 1:
                self.graph_window.resize(2000, 980)

            give, get, odds_win, odds_draw, titles = self.get_base_stat(data, date_list, self.team2)
            x = np.arange(len(give))

            p0_2 = self.graph_window.addPlot(col=3, colspan=2)
            p0_2.setTitle(f'Игры {self.team2} с {date_list[0]} по {date_list[-1]}', **{'color': '#FFF', 'size': '14pt'})
            p0_2.addLegend()
            p0_2.showGrid(y=True)
            p0_2.showAxis('bottom', False)

            bar_give = pg.BarGraphItem(x=x, width=0.2, stepMode="center", height=give, pen='w', brush=(0, 255, 0),
                                       name='Забито')
            p0_2.addItem(bar_give)
            bar_get = pg.BarGraphItem(x=x, width=0.2, stepMode="center", height=get, pen='w', brush=(248, 0, 0),
                                      name='Пропущено')
            p0_2.addItem(bar_get)

            ow_2 = p0_2.plot(x=x, y=odds_win, pen=pg.mkPen((31, 174, 233), width=3), symbolBrush=(31, 174, 233),
                         name='К на победу', symbol='o')
            od_2 = p0_2.plot(x=x, y=odds_draw, pen=pg.mkPen((234, 230, 202), width=3), symbolBrush=(234, 230, 202),
                         name='К на ничью', symbol='o')

            for i in range(len(give)):
                if titles[i].find("Победа") > 0:
                    fill = (0, 255, 0, 90)
                elif titles[i].find("Поражение") > 0:
                    fill = (248, 0, 0, 90)
                else:
                    fill = (234, 230, 202, 90)
                text = pg.TextItem(text=f'{titles[i]}', anchor=(0.5, -0.2), angle=0, border='w', fill=fill)
                #text.setColor((0, 0, 0))

                p0_2.addItem(text)
                text.setPos(i, get[i])


        self.graph_window.nextRow()
        sum_stat = 0
        try:
            stat_name = params[0]
            x, y, tl = self.get_stat(data, date_list, self.team1, stat_name)
            sum_stat += sum(y)
            if len(y) != 0:
                p1 = self.graph_window.addPlot(col=1)
                p1.setTitle(stat_name, **{'color': '#000', 'size': '14pt'})
                p1.showGrid(y=True)
                p1.showAxis('bottom', False)
                bg1 = pg.BarGraphItem(x=x,width=0.3, stepMode="center", height=y, pen='w', brush=(127, 255, 212, 150))
                p1.addItem(bg1)
                for i in range(len(y)):
                    text = pg.TextItem(text=f'{tl[i]}', anchor=(0.5, -0.2), angle=0, border='w', fill=(127, 255, 212, 90))
                    text.setColor((0, 0, 0))
                    p1.addItem(text)
                    text.setPos(i, 0)
            if self.team2 != "Не выбрано":
                x, y, tl = self.get_stat(data, date_list, self.team2, stat_name)
                if len(y) != 0:
                    p1_2 = self.graph_window.addPlot(col=3)
                    p1_2.setTitle(stat_name, **{'color': '#FFF', 'size': '14pt'})
                    p1_2.showGrid(y=True)
                    p1_2.showAxis('bottom', False)
                    bg1_2 = pg.BarGraphItem(x=x, width=0.3, stepMode="center", height=y, pen='w',
                                          brush=(127, 255, 212, 150))
                    p1_2.addItem(bg1_2)
                    for i in range(len(y)):
                        text = pg.TextItem(text=f'{tl[i]}', anchor=(0.5, -0.2), angle=0, border='w',
                                           fill=(127, 255, 212, 90))
                        #text.setColor((0, 0, 0))
                        p1_2.addItem(text)
                        text.setPos(i, 0)
        except:
            pass
        try:
            stat_name = params[1]
            x, y, tl = self.get_stat(data, date_list, self.team1, stat_name)
            sum_stat += sum(y)
            if len(y) != 0:
                p2 = self.graph_window.addPlot(col=2)
                p2.setTitle(stat_name, **{'color': '#FFF', 'size': '14pt'})
                p2.showGrid(y=True)
                p2.showAxis('bottom', False)
                bg2 = pg.BarGraphItem(x=x, width=0.3, stepMode="center", height=y, pen='w', brush=(241, 156, 187, 150))
                p2.addItem(bg2)
                for i in range(len(y)):
                    text = pg.TextItem(text=f'{tl[i]}', anchor=(0.5, -0.2), angle=0, border='w', fill=(241, 156, 187, 90))
                    text.setColor((0,0,0))
                    p2.addItem(text)
                    text.setPos(i, 0)
            if self.team2 != "Не выбрано":
                x, y, tl = self.get_stat(data, date_list, self.team2, stat_name)
                if len(y) != 0:
                    p2_2 = self.graph_window.addPlot(col=4)
                    p2_2.setTitle(stat_name, **{'color': '#FFF', 'size': '14pt'})
                    p2_2.showGrid(y=True)
                    p2_2.showAxis('bottom', False)
                    bg2_2 = pg.BarGraphItem(x=x, width=0.3, stepMode="center", height=y, pen='w',
                                            brush=(241, 156, 187, 150))
                    p2_2.addItem(bg2_2)
                    for i in range(len(y)):
                        text = pg.TextItem(text=f'{tl[i]}', anchor=(0.5, -0.2), angle=0, border='w',
                                           fill=(241, 156, 187, 90))
                        #text.setColor((0, 0, 0))
                        p2_2.addItem(text)
                        text.setPos(i, 0)
            self.graph_window.nextRow()
        except:
            pass
        try:
            stat_name = params[2]
            if len(params) == 3:
                if self.stat_check4.isChecked() and self.stat_check4.text() == "Голы по периодам":
                    cs = 1
                else:
                    cs = 2
            else:
                cs = 1
            x, y, tl = self.get_stat(data, date_list, self.team1, stat_name)
            sum_stat += sum(y)
            if len(y) != 0:
                p3 = self.graph_window.addPlot(col=1, colspan=cs)
                p3.setTitle(stat_name, **{'color': '#FFF', 'size': '14pt'})
                p3.showGrid(y=True)
                p3.showAxis('bottom', False)
                bg3 = pg.BarGraphItem(x=x, width=0.3, stepMode="center", height=y, pen='w', brush=(255, 184, 65, 150))
                p3.addItem(bg3)
                for i in range(len(y)):
                    text = pg.TextItem(text=f'{tl[i]}', anchor=(0.5, -0.2), angle=0, border='w', fill=(255, 184, 65, 90))
                    #text.setColor((0,0,0))
                    p3.addItem(text)
                    text.setPos(i, 0)
            if self.team2 != "Не выбрано":
                x, y, tl = self.get_stat(data, date_list, self.team2, stat_name)
                if len(y) != 0:
                    p3_2 = self.graph_window.addPlot(col=3, colspan=cs)
                    p3_2.setTitle(stat_name, **{'color': '#FFF', 'size': '14pt'})
                    p3_2.showGrid(y=True)
                    p3_2.showAxis('bottom', False)
                    bg3_2 = pg.BarGraphItem(x=x, width=0.3, stepMode="center", height=y, pen='w',
                                            brush=(255, 184, 65, 150))
                    p3_2.addItem(bg3_2)
                    for i in range(len(y)):
                        text = pg.TextItem(text=f'{tl[i]}', anchor=(0.5, -0.2), angle=0, border='w',
                                           fill=(255, 184, 65, 90))
                        #text.setColor((0, 0, 0))
                        p3_2.addItem(text)
                        text.setPos(i, 0)
        except:
            pass
        try:
            stat_name = params[3]
            x, y, tl = self.get_stat(data, date_list, self.team1, stat_name)
            sum_stat += sum(y)
            if len(y) != 0:
                p4 = self.graph_window.addPlot(col=2)
                p4.setTitle(stat_name, **{'color': '#FFF', 'size': '14pt'})
                p4.showGrid(y=True)
                p4.showAxis('bottom', False)
                bg4 = pg.BarGraphItem(x=x, width=0.3, stepMode="center", height=y, pen='w', brush=(100, 149, 237, 150))
                p4.addItem(bg4)
                for i in range(len(y)):
                    text = pg.TextItem(text=f'{tl[i]}',
                                       anchor=(0.5, -0.2), angle=0, border='w', fill=(100, 149, 237, 90))
                    #text.setColor((0, 0, 0))
                    p4.addItem(text)
                    text.setPos(i, 0)
            if self.team2 != "Не выбрано":
                x, y, tl = self.get_stat(data, date_list, self.team2, stat_name)
                if len(y) != 0:
                    p4_2 = self.graph_window.addPlot(col=4)
                    p4_2.setTitle(stat_name, **{'color': '#FFF', 'size': '14pt'})
                    p4_2.showGrid(y=True)
                    p4_2.showAxis('bottom', False)
                    bg4_2 = pg.BarGraphItem(x=x, width=0.3, stepMode="center", height=y, pen='w',
                                            brush=(100, 149, 237, 150))
                    p4_2.addItem(bg4_2)
                    for i in range(len(y)):
                        text = pg.TextItem(text=f'{tl[i]}', anchor=(0.5, -0.2), angle=0, border='w',
                                           fill=(100, 149, 237, 90))
                        #text.setColor((0, 0, 0))
                        p4_2.addItem(text)
                        text.setPos(i, 0)

            self.graph_window.nextRow()
        except:
            pass
        try:
            stat_name = params[4]
            if len(params) == 5:
                cs = 2
            else:
                cs = 1
            x, y, tl = self.get_stat(data, date_list, self.team1, stat_name)
            sum_stat += sum(y)
            if len(y) != 0:
                p5 = self.graph_window.addPlot(col=1, colspan=cs)
                p5.setTitle(stat_name, **{'color': '#FFF', 'size': '14pt'})
                p5.showGrid(y=True)
                bg5 = pg.BarGraphItem(x=x, width=0.3, stepMode="center", height=y, pen='w', brush=(223,	115, 255, 150))
                p5.addItem(bg5)
                for i in range(len(y)):
                    text = pg.TextItem(text=f'{tl[i]}', anchor=(0.5, -0.2), angle=0, border='w', fill=(223,	115, 255,90))
                    #text.setColor((0, 0, 0))
                    p5.addItem(text)
                    text.setPos(i, 0)
            if self.team2 != "Не выбрано":
                x, y, tl = self.get_stat(data, date_list, self.team2, stat_name)
                if len(y) != 0:
                    p5_2 = self.graph_window.addPlot(col=3, colspan=cs)
                    p5_2.setTitle(stat_name, **{'color': '#FFF', 'size': '14pt'})
                    p5_2.showGrid(y=True)
                    p5_2.showAxis('bottom', False)
                    bg5_2 = pg.BarGraphItem(x=x, width=0.3, stepMode="center", height=y, pen='w',
                                            brush=(223,	115, 255, 150))
                    p5_2.addItem(bg5_2)
                    for i in range(len(y)):
                        text = pg.TextItem(text=f'{tl[i]}', anchor=(0.5, -0.2), angle=0, border='w',
                                           fill=(223, 115, 255,90))
                        #text.setColor((0, 0, 0))
                        p5_2.addItem(text)
                        text.setPos(i, 0)
        except:
            pass
        try:
            stat_name = params[5]
            x, y, tl = self.get_stat(data, date_list, self.team1, stat_name)
            sum_stat += sum(y)
            if len(y) != 0:
                p6 = self.graph_window.addPlot(col=2)
                p6.setTitle(stat_name, **{'color': '#FFF', 'size': '14pt'})
                p6.showGrid(y=True)
                bg6 = pg.BarGraphItem(x=x, width=0.3, stepMode="center", height=y, pen='w', brush=(52, 201, 36, 150))
                p6.addItem(bg6)
                for i in range(len(y)):
                    text = pg.TextItem(text=f'{tl[i]}', anchor=(0.5, -0.2), angle=0, border='w', fill=(52, 201, 36, 90))
                    #text.setColor((0,0,0))
                    p6.addItem(text)
                    text.setPos(i, 0)
            if self.team2 != "Не выбрано":
                x, y, tl = self.get_stat(data, date_list, self.team2, stat_name)
                if len(y) != 0:
                    p6_2 = self.graph_window.addPlot(col=4)
                    p6_2.setTitle(stat_name, **{'color': '#FFF', 'size': '14pt'})
                    p6_2.showGrid(y=True)
                    p6_2.showAxis('bottom', False)
                    bg6_2 = pg.BarGraphItem(x=x, width=0.3, stepMode="center", height=y, pen='w',
                                            brush=(52, 201, 36, 150))
                    p6_2.addItem(bg6_2)
                    for i in range(len(y)):
                        text = pg.TextItem(text=f'{tl[i]}', anchor=(0.5, -0.2), angle=0, border='w',
                                           fill=(52, 201, 36, 90))
                        #text.setColor((0, 0, 0))
                        p6_2.addItem(text)
                        text.setPos(i, 0)
        except:
            pass


        if self.stat_check4.isChecked() and self.stat_check4.text() == "Голы по периодам":
            if (len(params)+1) % 2 == 0:  # 2 либо 4
                cl = 2
            else: #1 либо 3
                cl = 1
            x, y, tl = self.get_stat(data, date_list, self.team1, "1 период")
            if len(y) != 0:
                pp1 = self.graph_window.addPlot(col=cl)
                pp1.setTitle("Голы в 1 период", **{'color': '#FFF', 'size': '14pt'})
                pp1.showGrid(y=True)
                bgp1 = pg.BarGraphItem(x=x, width=0.3, stepMode="center", height=y, pen='w', brush=(52, 201, 36, 150))
                pp1.addItem(bgp1)
                for i in range(len(y)):
                    text = pg.TextItem(text=f'{tl[i]}', anchor=(0.5, -0.2), angle=0, border='w', fill=(52, 201, 36, 90))
                    #text.setColor((0,0,0))
                    pp1.addItem(text)
                    text.setPos(i, 0)
            if self.team2 != "Не выбрано":
                x, y, tl = self.get_stat(data, date_list, self.team2, "1 период")
                if len(y) != 0:
                    pp1_2 = self.graph_window.addPlot(col=cl+2)
                    pp1_2.setTitle("Голы в 1 период", **{'color': '#FFF', 'size': '14pt'})
                    pp1_2.showGrid(y=True)
                    pp1_2.showAxis('bottom', False)
                    bgp1_2 = pg.BarGraphItem(x=x, width=0.3, stepMode="center", height=y, pen='w',
                                             brush=(52, 201, 36, 150))
                    pp1_2.addItem(bgp1_2)
                    for i in range(len(y)):
                        text = pg.TextItem(text=f'{tl[i]}', anchor=(0.5, -0.2), angle=0, border='w',
                                           fill=(52, 201, 36, 90))
                        #text.setColor((0, 0, 0))
                        pp1_2.addItem(text)
                        text.setPos(i, 0)

            if (len(params)+1) % 2 == 0: #2 либо 4
                self.graph_window.nextRow()
                cl = 1
            else:
                cl = 2

            x, y, tl = self.get_stat(data, date_list, self.team1, "2 период")
            if len(y) != 0:
                pp2 = self.graph_window.addPlot(col=cl)
                pp2.setTitle("Голы во 2 период", **{'color': '#FFF', 'size': '14pt'})
                pp2.showGrid(y=True)
                bgp2 = pg.BarGraphItem(x=x, width=0.3, stepMode="center", height=y, pen='w', brush=(223, 115, 255, 150))
                pp2.addItem(bgp2)
                for i in range(len(y)):
                    text = pg.TextItem(text=f'{tl[i]}', anchor=(0.5, -0.2), angle=0, border='w', fill=(223,	115, 255, 90))
                    #text.setColor((0,0,0))
                    pp2.addItem(text)
                    text.setPos(i, 0)

            if self.team2 != "Не выбрано":
                x, y, tl = self.get_stat(data, date_list, self.team2, "2 период")
                if len(y) != 0:
                    pp2_2 = self.graph_window.addPlot(col=cl+2)
                    pp2_2.setTitle("Голы во 2 период", **{'color': '#FFF', 'size': '14pt'})
                    pp2_2.showGrid(y=True)
                    pp2_2.showAxis('bottom', False)
                    bgp2_2 = pg.BarGraphItem(x=x, width=0.3, stepMode="center", height=y, pen='w',
                                             brush=(52, 201, 36, 150))
                    pp2_2.addItem(bgp2_2)
                    for i in range(len(y)):
                        text = pg.TextItem(text=f'{tl[i]}', anchor=(0.5, -0.2), angle=0, border='w',
                                           fill=(52, 201, 36, 90))
                        #text.setColor((0, 0, 0))
                        pp2_2.addItem(text)
                        text.setPos(i, 0)

            if (len(params)+1) % 2 == 0:  # 2 либо 4
                cl = 2
                cs = 1
            else:
                self.graph_window.nextRow()
                cl = 1
                cs = 2

            x, y, tl = self.get_stat(data, date_list, self.team1, "3 период")
            if len(y) != 0:
                pp3 = self.graph_window.addPlot(col=cl, colspan=cs)
                pp3.setTitle("Голы в 3 период", **{'color': '#FFF', 'size': '14pt'})
                pp3.showGrid(y=True)
                bgp3 = pg.BarGraphItem(x=x, width=0.3, stepMode="center", height=y, pen='w', brush=(100, 149, 237, 150))
                pp3.addItem(bgp3)
                for i in range(len(y)):
                    text = pg.TextItem(text=f'{tl[i]}', anchor=(0.5, -0.2), angle=0, border='w', fill=(100, 149, 237, 90))
                    #text.setColor((0,0,0))
                    pp3.addItem(text)
                    text.setPos(i, 0)
            if self.team2 != "Не выбрано":
                x, y, tl = self.get_stat(data, date_list, self.team2, "3 период")
                if len(y) != 0:
                    pp3_2 = self.graph_window.addPlot(col=cl+2,colspan=cs)
                    pp3_2.setTitle("Голы в 3 период", **{'color': '#FFF', 'size': '14pt'})
                    pp3_2.showGrid(y=True)
                    pp3_2.showAxis('bottom', False)
                    bgp3_2 = pg.BarGraphItem(x=x, width=0.3, stepMode="center", height=y, pen='w',
                                            brush=(52, 201, 36, 150))
                    pp3_2.addItem(bgp3_2)
                    for i in range(len(y)):
                        text = pg.TextItem(text=f'{tl[i]}', anchor=(0.5, -0.2), angle=0, border='w',
                                           fill=(52, 201, 36, 90))
                        #text.setColor((0, 0, 0))
                        pp3_2.addItem(text)
                        text.setPos(i, 0)

        if sum_stat == 0:
            try:
                self.graph_window.removeItem(p1)
            except:
                pass
            try:
                self.graph_window.removeItem(p1_2)
            except:
                pass
            try:
                self.graph_window.removeItem(p2)
            except:
                pass
            try:
                self.graph_window.removeItem(p2_2)
            except:
                pass
            try:
                self.graph_window.removeItem(p3)
            except:
                pass
            try:
                self.graph_window.removeItem(p3_2)
            except:
                pass
            try:
                self.graph_window.removeItem(p4)
            except:
                pass
            try:
                self.graph_window.removeItem(p4_2)
            except:
                pass
            try:
                self.graph_window.removeItem(p5)
            except:
                pass
            try:
                self.graph_window.removeItem(p5_2)
            except:
                pass
            try:
                self.graph_window.removeItem(p6)
            except:
                pass
            try:
                self.graph_window.removeItem(p6_2)
            except:
                pass
        self.graph_window.show()
        pg.exec()

    async def parse_matches(self, session, data, date):  # тут идем по страницам с датами, забираем id для ссылки на статистику

        url = data[self.sport][self.champ]['URL'] + '/' + date + '/'
        async with session.get(url=url) as response:
            self.count_parse += 100 / self.total_parse
            if 1 <= self.count_parse < 2:
                self.progressBar.setValue(self.progressBar.value() + 1)
                self.count_parse -= 1
            elif self.count_parse >= 2:
                self.progressBar.setValue(self.progressBar.value() + int(self.count_parse - self.count_parse % 1))
                self.count_parse %= 1
            if response.status == 200:
                response_text = await response.text()
                soup = bs(response_text, "lxml")
                if len(soup.findAll(class_="se-matchcenter-sports-no-events-block__text")) != 0:
                    data[self.sport][self.champ]["noData"].append(date)
                    # noData нужна чтобы не парсить сайты где нет инфы
                else:
                    data[self.sport][self.champ][date] = {}

                    matches = soup.findAll(
                        class_="se-matchcenter-matches__match se-matchcenter-matches__match--status-not-started")
                    if len(matches) == 0:
                        matches = soup.findAll(
                            class_="se-matchcenter-matches__match se-matchcenter-matches__match--status-fin")  # волейбол/хоккей/гандбол, но может и футбол

                    if self.sport == 'Футбол' or self.sport == 'Хоккей':  # для других видов спорта отдельных url со статистикой нет
                        data[self.sport][self.champ][date]['id_list'] = []
                    # проход по всем сыгранным матчам любого вида спорта
                    for match in matches:
                        link = match.get('href')
                        if link:
                            # ссылка есть - парсим в другой функции статистику
                            ID = link[-7:-1]
                            data[self.sport][self.champ][date]['id_list'].append(ID)
                        else:
                            # ссылки нет - парсим текущий сайт
                            if self.sport == "Волейбол":
                                teams_name = match.findAll(class_="se-matchcenter-volleyball-matches__team")
                            elif self.sport == "Теннис":
                                teams_name = match.findAll(class_="se-matchcenter-tennis-matches__player")
                            elif self.sport == "Хоккей":
                                teams_name = match.findAll(class_="sp-matchcenter-board-team-details__team")
                            else:
                                teams_name = match.findAll(class_="se-matchcenter-matches__match-team__name")

                            team_home_name = teams_name[0].text.strip()
                            team_guest_name = teams_name[1].text.strip()
                            if self.sport == "Теннис":
                                team_home_name = teams_name[0].text.replace('\n', '').replace(
                                    '                            ', '').strip()
                                team_guest_name = teams_name[1].text.replace('\n', '').replace(
                                    '                            ', '').strip()

                            data[self.sport][self.champ][date][team_home_name] = {}
                            data[self.sport][self.champ][date][team_guest_name] = {}

                            data[self.sport][self.champ][date][team_home_name]['Cоперник'] = team_guest_name
                            data[self.sport][self.champ][date][team_guest_name]['Cоперник'] = team_home_name

                            if self.sport != "Теннис":
                                data[self.sport][self.champ][date][team_home_name]['Локация'] = 'Дома'
                                data[self.sport][self.champ][date][team_guest_name]['Локация'] = 'Гости'

                            if self.sport == "Волейбол" or self.sport == "Теннис":
                                if self.sport == "Волейбол":
                                    score = match.findAll(class_="se-matchcenter-volleyball-matches__result")
                                    score_list_team_home = score[0].text.strip().split('\n')
                                    score_list_team_guest = score[1].text.strip().split('\n')
                                else:
                                    score = match.findAll(class_="se-matchcenter-tennis-matches__score")
                                    score_list_team_home = score[0].text.strip().split(' ')
                                    score_list_team_guest = score[1].text.strip().split(' ')
                                score_team_home = 0
                                score_team_guest = 0
                                team_home_win_count = 0
                                team_guest_win_count = 0
                                for i in range(len(score_list_team_home)):
                                    if not (score_list_team_home[i].isdigit() and score_list_team_guest[i].isdigit()):
                                        del data[self.sport][self.champ][date][team_home_name]
                                        del data[self.sport][self.champ][date][team_guest_name]
                                        return
                                    set_score_team_home = int(score_list_team_home[i])
                                    set_score_team_guest = int(score_list_team_guest[i])
                                    data[self.sport][self.champ][date][team_home_name][
                                        f'{i + 1} сет'] = set_score_team_home
                                    data[self.sport][self.champ][date][team_guest_name][
                                        f'{i + 1} сет'] = set_score_team_guest
                                    score_team_home += set_score_team_home
                                    score_team_guest += set_score_team_guest
                                    if set_score_team_home > set_score_team_guest:
                                        team_home_win_count += 1
                                    else:
                                        team_guest_win_count += 1

                                data[self.sport][self.champ][date][team_home_name]['Забито'] = score_team_home
                                data[self.sport][self.champ][date][team_home_name]['Пропущено'] = score_team_guest
                                data[self.sport][self.champ][date][team_guest_name]['Забито'] = score_team_guest
                                data[self.sport][self.champ][date][team_guest_name]['Пропущено'] = score_team_home

                                if team_home_win_count > team_guest_win_count:
                                    data[self.sport][self.champ][date][team_home_name]['Статус'] = 'Победа'
                                    data[self.sport][self.champ][date][team_guest_name]['Статус'] = 'Поражение'
                                else:
                                    data[self.sport][self.champ][date][team_home_name]['Статус'] = 'Поражение'
                                    data[self.sport][self.champ][date][team_guest_name]['Статус'] = 'Победа'

                                data[self.sport][self.champ][date][team_home_name]['Забито'] = score_team_home
                                data[self.sport][self.champ][date][team_guest_name]['Забито'] = score_team_guest
                                data[self.sport][self.champ][date][team_home_name]['Пропущено'] = score_team_guest
                                data[self.sport][self.champ][date][team_guest_name]['Пропущено'] = score_team_home

                            else:  # футбол, хоккей, баскетбол, гандбол
                                score = match.find(class_="se-matchcenter-matches__match-score__column") \
                                    .text.strip().replace(' ', '').split('\n')

                                if not (score[0].isdigit() and score[1].isdigit()):
                                    del data[self.sport][self.champ][date][team_home_name]
                                    del data[self.sport][self.champ][date][team_guest_name]
                                    return
                                data[self.sport][self.champ][date][team_home_name]["Забито"] = int(score[0])
                                data[self.sport][self.champ][date][team_home_name]["Пропущено"] = int(score[1])
                                data[self.sport][self.champ][date][team_guest_name]["Забито"] = int(score[1])
                                data[self.sport][self.champ][date][team_guest_name]["Пропущено"] = int(score[0])

                                if int(score[0]) > int(score[1]):
                                    data[self.sport][self.champ][date][team_home_name]['Статус'] = 'Победа'
                                    data[self.sport][self.champ][date][team_guest_name]['Статус'] = 'Поражение'
                                elif int(score[0]) < int(score[1]):
                                    data[self.sport][self.champ][date][team_home_name]['Статус'] = 'Поражение'
                                    data[self.sport][self.champ][date][team_guest_name]['Статус'] = 'Победа'
                                else:
                                    data[self.sport][self.champ][date][team_home_name]['Статус'] = 'Ничья'
                                    data[self.sport][self.champ][date][team_guest_name]['Статус'] = 'Ничья'

                                if len(score) > 2:
                                    data[self.sport][self.champ][date][team_home_name]['Исход'] = score[2]
                                    data[self.sport][self.champ][date][team_guest_name]['Исход'] = score[2]
                                else:
                                    data[self.sport][self.champ][date][team_home_name]['Исход'] = 'ОВ'
                                    data[self.sport][self.champ][date][team_guest_name]['Исход'] = 'ОВ'

                            bets = match.findAll(class_="se-bets__bet")
                            for bet in bets:
                                bet_name, bet_value = bet.text.split(' ')
                                if bet_name == 'П1':
                                    data[self.sport][self.champ][date][team_home_name]['К победы'] = float(bet_value)
                                elif bet_name == 'П2':
                                    data[self.sport][self.champ][date][team_guest_name]['К победы'] = float(bet_value)
                                elif bet_name == 'X':
                                    data[self.sport][self.champ][date][team_home_name]['К ничьи'] = float(bet_value)
                                    data[self.sport][self.champ][date][team_guest_name]['К ничьи'] = float(bet_value)

    async def gather_matches(self, data, date_list):  # запускает парсер url со статистикой и возвращает их
        async with aiohttp.ClientSession() as session:
            tasks = []
            for date in date_list:
                if date in data[self.sport][self.champ].keys() or date in data[self.sport][self.champ]["noData"]:
                    # дата учтена
                    continue
                task = asyncio.create_task(self.parse_matches(session, data, date))
                tasks.append(task)
            self.total_parse = len(tasks)
            await asyncio.gather(*tasks)

    async def parse_stat_data(self, session, url, data, date):
        # ТОЛЬКО ДЛЯ ФУТБОЛА И ХОККЕЯ

        async with session.get(url=url) as response:  # тут обрабатываем запрос на страничку html либо json
            self.count_parse += 100 / self.total_parse
            if 1 <= self.count_parse < 2:
                self.progressBar.setValue(self.progressBar.value() + 1)
                self.count_parse -= 1
            elif self.count_parse >= 2:
                self.progressBar.setValue(self.progressBar.value() + int(self.count_parse - self.count_parse % 1))
                self.count_parse %= 1
            if response.status == 200:
                response_text = await response.text()
                stat_soup = bs(response_text, "lxml")

                if self.sport == 'Футбол':  # парсим json
                    stat_data = eval(stat_soup.text)  # формат словаря

                    team_home_name = stat_data["homeCommand"]["name"]
                    team_guest_name = stat_data["guestCommand"]["name"]

                    data[self.sport][self.champ][date][team_home_name] = {}
                    data[self.sport][self.champ][date][team_guest_name] = {}
                    data[self.sport][self.champ][date][team_home_name]['Cоперник'] = team_guest_name
                    data[self.sport][self.champ][date][team_guest_name]['Cоперник'] = team_home_name
                    data[self.sport][self.champ][date][team_home_name]['Локация'] = 'Дома'
                    data[self.sport][self.champ][date][team_guest_name]['Локация'] = 'Гости'

                    if not os.path.exists(f'imgs/team_logo/{team_home_name}.png'):
                        if stat_data["homeCommand"]["icon80x80"][0] == 'h':
                            img_link = stat_data["homeCommand"]["icon80x80"]
                        else:
                            img_link = 'https:' + stat_data["homeCommand"]["icon80x80"]
                        h = httplib2.Http('.cache')
                        response, content = h.request(img_link)
                        out = open(f'imgs/team_logo/{team_home_name}.png', 'wb')
                        out.write(content)
                        out.close()

                    if not os.path.exists(f'imgs/team_logo/{team_guest_name}.png'):
                        if stat_data["guestCommand"]["icon80x80"][0] == 'h':
                            img_link = stat_data["guestCommand"]["icon80x80"]
                        else:
                            img_link = 'https:' + stat_data["guestCommand"]["icon80x80"]
                        h = httplib2.Http('.cache')
                        response, content = h.request(img_link)
                        out = open(f'imgs/team_logo/{team_guest_name}.png', 'wb')
                        out.write(content)
                        out.close()
                    if not (stat_data["homeScore"].isdigit() and stat_data["guestScore"].isdigit()):
                        del data[self.sport][self.champ][date][team_home_name]
                        del data[self.sport][self.champ][date][team_guest_name]
                        return
                    data[self.sport][self.champ][date][team_home_name]['Забито'] = int(stat_data["homeScore"])
                    data[self.sport][self.champ][date][team_guest_name]['Забито'] = int(stat_data["guestScore"])
                    data[self.sport][self.champ][date][team_home_name]['Пропущено'] = int(stat_data["guestScore"])
                    data[self.sport][self.champ][date][team_guest_name]['Пропущено'] = int(stat_data["homeScore"])

                    if stat_data["result"] == "1":
                        data[self.sport][self.champ][date][team_home_name]['Статус'] = 'Победа'
                        data[self.sport][self.champ][date][team_guest_name]['Статус'] = 'Поражение'
                    elif stat_data["result"] == "-1":
                        data[self.sport][self.champ][date][team_home_name]['Статус'] = 'Поражение'
                        data[self.sport][self.champ][date][team_guest_name]['Статус'] = 'Победа'
                    else:
                        data[self.sport][self.champ][date][team_home_name]['Статус'] = 'Ничья'
                        data[self.sport][self.champ][date][team_guest_name]['Статус'] = 'Ничья'

                    if stat_data["isOvertimePlayed"] == "1":
                        if stat_data["isPenaltyPlayed"] == "1":
                            data[self.sport][self.champ][date][team_home_name]['Исход'] = 'П'
                            data[self.sport][self.champ][date][team_guest_name]['Исход'] = 'П'
                            data[self.sport][self.champ][date][team_home_name]['П забито'] = int(
                                stat_data["homePenaltyScore"])
                            data[self.sport][self.champ][date][team_guest_name]['П забито'] = int(
                                stat_data["guestPenaltyScore"])
                            data[self.sport][self.champ][date][team_home_name]['П пропущено'] = int(
                                stat_data["guestPenaltyScore"])
                            data[self.sport][self.champ][date][team_guest_name]['П пропущено'] = int(
                                stat_data["homePenaltyScore"])
                        else:
                            data[self.sport][self.champ][date][team_home_name]['Исход'] = 'ДВ'
                            data[self.sport][self.champ][date][team_guest_name]['Исход'] = 'ДВ'
                    else:
                        data[self.sport][self.champ][date][team_home_name]['Исход'] = 'ОВ'
                        data[self.sport][self.champ][date][team_guest_name]['Исход'] = 'ОВ'

                    data[self.sport][self.champ][date][team_home_name]["Статистика"] = {}
                    data[self.sport][self.champ][date][team_guest_name]["Статистика"] = {}

                    data[self.sport][self.champ][date][team_home_name]["Статистика"]["Владение мячом"] = int(
                        stat_data["homeCommand"]["statistic"]["homePosession"])
                    data[self.sport][self.champ][date][team_guest_name]["Статистика"]["Владение мячом"] = int(
                        stat_data["guestCommand"]["statistic"]["guestPosession"])
                    data[self.sport][self.champ][date][team_home_name]["Статистика"]["Всего ударов"] = int(
                        stat_data["homeCommand"]["statistic"]["homeShotwides"])
                    data[self.sport][self.champ][date][team_guest_name]["Статистика"]["Всего ударов"] = int(
                        stat_data["guestCommand"]["statistic"]["guestShotwides"])
                    data[self.sport][self.champ][date][team_home_name]["Статистика"]["Ударов в створ"] = int(
                        stat_data["homeCommand"]["statistic"]["homeShotgates"])
                    data[self.sport][self.champ][date][team_guest_name]["Статистика"]["Ударов в створ"] = int(
                        stat_data["guestCommand"]["statistic"]["guestShotgates"])
                    data[self.sport][self.champ][date][team_home_name]["Статистика"]["Угловые"] = int(
                        stat_data["homeCommand"]["statistic"]["homeCorners"])
                    data[self.sport][self.champ][date][team_guest_name]["Статистика"]["Угловые"] = int(
                        stat_data["guestCommand"]["statistic"]["guestCorners"])
                    data[self.sport][self.champ][date][team_home_name]["Статистика"]["Офсайды"] = int(
                        stat_data["homeCommand"]["statistic"]["homeOffsides"])
                    data[self.sport][self.champ][date][team_guest_name]["Статистика"]["Офсайды"] = int(
                        stat_data["guestCommand"]["statistic"]["guestOffsides"])
                    data[self.sport][self.champ][date][team_home_name]["Статистика"]["Нарушения"] = int(
                        stat_data["homeCommand"]["statistic"]["homeFouls"])
                    data[self.sport][self.champ][date][team_guest_name]["Статистика"]["Нарушения"] = int(
                        stat_data["guestCommand"]["statistic"]["guestFouls"])

                    if "bookies" in stat_data:
                        data[self.sport][self.champ][date][team_home_name]['К победы'] = float(
                            stat_data["bookies"]["odds1"])
                        data[self.sport][self.champ][date][team_guest_name]['К победы'] = float(
                            stat_data["bookies"]["odds2"])
                        data[self.sport][self.champ][date][team_home_name]['К ничьи'] = float(
                            stat_data["bookies"]["oddsX"])
                        data[self.sport][self.champ][date][team_guest_name]['К ничьи'] = float(
                            stat_data["bookies"]["oddsX"])


                elif self.sport == 'Хоккей':  # парсим html
                    team_home = stat_soup.find(class_="sp-matchcenter-board__left")
                    team_guest = stat_soup.find(class_="sp-matchcenter-board__right")
                    team_home_name = team_home.find(class_="sp-matchcenter-board-team-details__team").text.strip()
                    team_guest_name = team_guest.find(class_="sp-matchcenter-board-team-details__team").text.strip()

                    data[self.sport][self.champ][date][team_home_name] = {}
                    data[self.sport][self.champ][date][team_guest_name] = {}
                    data[self.sport][self.champ][date][team_home_name]['Cоперник'] = team_guest_name
                    data[self.sport][self.champ][date][team_guest_name]['Cоперник'] = team_home_name
                    data[self.sport][self.champ][date][team_home_name]['Локация'] = 'Дома'
                    data[self.sport][self.champ][date][team_guest_name]['Локация'] = 'Гости'

                    if not os.path.exists(f'imgs/team_logo/{team_home_name}.png'):
                        if team_home.img.get('src')[0] == 'h':
                            img_link = team_home.img.get('src')
                        else:
                            img_link = 'https:' + team_home.img.get('src')
                        h = httplib2.Http('.cache')
                        response, content = h.request(img_link)
                        out = open(f'imgs/team_logo/{team_home_name}.png', 'wb')
                        out.write(content)
                        out.close()

                    if not os.path.exists(f'imgs/team_logo/{team_guest_name}.png'):
                        if team_guest.img.get('src')[0] == 'h':
                            img_link = team_guest.img.get('src')
                        else:
                            img_link = 'https:' + team_guest.img.get('src')
                        h = httplib2.Http('.cache')
                        response, content = h.request(img_link)
                        out = open(f'imgs/team_logo/{team_guest_name}.png', 'wb')
                        out.write(content)
                        out.close()

                    score = stat_soup.find(class_="sp-MatchScore__score")
                    if score:
                        score = score.text.strip().split(':')
                    else:
                        return
                    if not (score[0].isdigit() and score[1].isdigit()):
                        del data[self.sport][self.champ][date][team_home_name]
                        del data[self.sport][self.champ][date][team_guest_name]
                        return
                    data[self.sport][self.champ][date][team_home_name]['Забито'] = int(score[0])
                    data[self.sport][self.champ][date][team_guest_name]['Забито'] = int(score[1])
                    data[self.sport][self.champ][date][team_home_name]['Пропущено'] = int(score[1])
                    data[self.sport][self.champ][date][team_guest_name]['Пропущено'] = int(score[0])

                    if int(score[0]) > int(score[1]):
                        data[self.sport][self.champ][date][team_home_name]['Статус'] = 'Победа'
                        data[self.sport][self.champ][date][team_guest_name]['Статус'] = 'Поражение'
                    elif int(score[0]) < int(score[1]):
                        data[self.sport][self.champ][date][team_home_name]['Статус'] = 'Поражение'
                        data[self.sport][self.champ][date][team_guest_name]['Статус'] = 'Победа'
                    else:
                        data[self.sport][self.champ][date][team_home_name]['Статус'] = 'Ничья'
                        data[self.sport][self.champ][date][team_guest_name]['Статус'] = 'Ничья'

                    result = stat_soup.find(class_="sp-MatchScore-scoreType sp-MatchScore-scoreType--right")
                    if result:
                        data[self.sport][self.champ][date][team_home_name]['Исход'] = result.text.strip()
                        data[self.sport][self.champ][date][team_guest_name]['Исход'] = result.text.strip()
                    else:
                        data[self.sport][self.champ][date][team_home_name]['Исход'] = 'ОВ'
                        data[self.sport][self.champ][date][team_guest_name]['Исход'] = 'ОВ'

                    periods = stat_soup.findAll(class_="sp-MatchCenterScoreByPeriods-periodScore")
                    for i in range(len(periods)):
                        per_score = periods[i].text.strip()
                        if i <= 2:  # периоды от 1 до 3
                            data[self.sport][self.champ][date][team_home_name][f'{i + 1} период'] = int(per_score[0])
                            data[self.sport][self.champ][date][team_guest_name][f'{i + 1} период'] = int(per_score[1])
                        elif i == 3:
                            data[self.sport][self.champ][date][team_home_name]['ОТ период'] = int(per_score[0])
                            data[self.sport][self.champ][date][team_guest_name]['ОТ период'] = int(per_score[1])
                        elif i == 4:
                            data[self.sport][self.champ][date][team_home_name]['В период'] = int(per_score[0])
                            data[self.sport][self.champ][date][team_guest_name]['В период'] = int(per_score[1])

                    statistic = stat_soup.find(class_="sp-MatchStats")
                    if statistic:
                        data[self.sport][self.champ][date][team_home_name]["Статистика"] = {}
                        data[self.sport][self.champ][date][team_guest_name]["Статистика"] = {}
                        statistic = statistic.findAll(
                            class_="sp-MatchStats__param")  # тут вся статистика за матч если есть
                        for elem in statistic:
                            elem_name = elem.find(class_="sp-MatchStats__param-title").text
                            value = elem.findAll(class_="sp-ProgressLineBar__value")
                            data[self.sport][self.champ][date][team_home_name]["Статистика"][elem_name] = int(
                                value[0].text)
                            data[self.sport][self.champ][date][team_guest_name]["Статистика"][elem_name] = int(
                                value[1].text)

                    bets = stat_soup.findAll(class_="sp-Betcity-bet")
                    for bet in bets:
                        bet_name = bet.find(class_="sp-Betcity-bet-title").text.strip()
                        bet_value = bet.find(class_="sp-Betcity-bet-value").text.strip()
                        if bet_name == 'П1':
                            data[self.sport][self.champ][date][team_home_name]['К победы'] = float(bet_value)
                        elif bet_name == 'П2':
                            data[self.sport][self.champ][date][team_guest_name]['К победы'] = float(bet_value)
                        elif bet_name == 'X':
                            data[self.sport][self.champ][date][team_home_name]['К ничьи'] = float(bet_value)
                            data[self.sport][self.champ][date][team_guest_name]['К ничьи'] = float(bet_value)



    async def gather_stat_data(self, data):  # запускает задачи на парсинг статистики если выбран футбол или хоккей

        url_list = []
        date_list = []
        if self.sport == 'Футбол' or self.sport == 'Хоккей':
            for key in data[self.sport][self.champ]:
                if key != 'URL' and key != 'noData':
                    if len(data[self.sport][self.champ][key].keys()) - 1 == len(
                            data[self.sport][self.champ][key]['id_list']) * 2:
                        # все матчи этой даты записаны
                        continue
                    for ID in data[self.sport][self.champ][key]['id_list']:
                        date_list.append(key)
                        if self.sport == 'Футбол':
                            url_list.append(
                                f'https://www.sport-express.ru/services/match/football/{ID}/online/se/?json=1')
                        elif self.sport == 'Хоккей':
                            url_list.append(f'https://www.sport-express.ru/hockey/L/matchcenter/{ID}/protocol/')
        async with aiohttp.ClientSession() as session:
            tasks = []
            for i in range(len(url_list)):
                task = asyncio.create_task(self.parse_stat_data(session, url_list[i], data, date_list[i]))
                tasks.append(task)
            self.total_parse = len(tasks)
            self.progressBar.setValue(0)
            await asyncio.gather(*tasks)

    def stat_params(self):
        arr = []
        if self.stat_check1.isChecked():
            arr.append(self.stat_check1.text())
        if self.stat_check2.isChecked():
            arr.append(self.stat_check2.text())
        if self.stat_check3.isChecked():
            arr.append(self.stat_check3.text())
        if self.stat_check4.isChecked():
            if self.stat_check4.text() != "Голы по периодам":
                arr.append(self.stat_check4.text())
        if self.stat_check5.isChecked():
            if self.sport != "Хоккей" or self.champ == "КХЛ":
                arr.append(self.stat_check5.text())
        if self.stat_check6.isChecked():
            if self.sport != "Хоккей":
                arr.append(self.stat_check6.text())
        return arr

    def showDialog(self, message):
        error = QtWidgets.QMessageBox()
        error.setWindowTitle("Предупреждение")
        error.setWindowIcon(QtGui.QIcon('imgs\warning.png'))
        error.setText(message)
        error.setIcon(QtWidgets.QMessageBox.Warning)
        error.setStandardButtons(QtWidgets.QMessageBox.Ok)
        error.exec_()

    def stat_select_all(self):
        if self.stat_check_all.isChecked():
            self.stat_check1.setChecked(True)
            self.stat_check2.setChecked(True)
            self.stat_check3.setChecked(True)
            self.stat_check4.setChecked(True)
            self.stat_check5.setChecked(True)
            self.stat_check6.setChecked(True)
        else:
            self.stat_check1.setChecked(False)
            self.stat_check2.setChecked(False)
            self.stat_check3.setChecked(False)
            self.stat_check4.setChecked(False)
            self.stat_check5.setChecked(False)
            self.stat_check6.setChecked(False)

    def sport_update(self):
        self.sport = self.sport_name.currentText()

    def champ_update(self):
        self.champ = self.champ_name.currentText()

    def team1_update(self):
        self.team1 = self.team1_name.currentText()

    def team2_update(self):
        self.team2 = self.team2_name.currentText()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
