import math
from tkinter import *
from tkinter import ttk
import fileinput
from tkinter.filedialog import *
from tkinter.messagebox import showinfo
import csv
import json
from matplotlib import pyplot as plt
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os


URL1 = 'https://www.gismeteo.ru/diary/11441/2022/4/'
URL2 ='https://www.gismeteo.ru/diary/11441/2022/5/'

data_list = []
lines = []
file_name = ''

class MainWindow():
    def __init__(self, color="8e1b8e"):
        self.root = Tk()
        self.root.title('Название')
        self.root.geometry('700x570')
        #self.root.config(bg='seashell')
        self.root.config(bg='#FFFAF0')


    def run(self):
        self.show_widgets()
        self.root.mainloop()

    def show_widgets(self):


        menu_bar = Menu(self.root)
        menu_bar.add_command(label="Открыть файл", command=self.open_file)
        self.root.configure(menu=menu_bar)

        self.lable1 = Label(self.root, text="Прибор", bg="#FFFAF0", font="Roboto 12").place(y=25, relx=0.25, anchor=CENTER) #x=110

        self.lable2 = Label(self.root, text="Данные для обработки", bg="#FFFAF0", font="Roboto 12")

        self.lable3 = Label(self.root, text="по оси X", bg="#FFFAF0", font="Roboto 10")

        self.lable4 = Label(self.root, text="по оси Y", bg="#FFFAF0", font="Roboto 10")

        self.lable5 = Label(self.root, text="Данные", bg="#FFFAF0", font="Roboto 12")

        self.lable6 = Label(self.root, text="Начало интервала", bg="#FFFAF0", font="Roboto 12")

        self.lable7 = Label(self.root, text="Конец инервала", bg="#FFFAF0", font="Roboto 12")

        self.lable8 = Label(self.root, text="График", bg="#FFFAF0", font="Roboto 12")

        self.lable9 = Label(self.root, text="по оси", bg="#FFFAF0", font="Roboto 10")

        self.lable10 = Label(self.root, text="по оси", bg="#FFFAF0", font="Roboto 10")

        self.button1 = Button(text="Построить график", bg='#32CD32', font="Roboto 12", relief=RAISED)
        self.button1.config(command=self.build_graph)

        self.button2 = Button(text="Построить график ЭТ", bg='#32CD32', font="Roboto 12", relief=RAISED)
        self.button2.config(command=self.buildET_graph)



        self.choice1 = IntVar(value=0)
        self.rad1 = Radiobutton(self.root, text="Как есть", variable=self.choice1, value=0, bg="#FFFAF0", font="Roboto 11")
        self.rad2 = Radiobutton(self.root, text="Осреднять за час", variable=self.choice1, value=1, bg="#FFFAF0", font="Roboto 11")
        self.rad3 = Radiobutton(self.root, text="Осреднять за каждые 3 часа", variable=self.choice1, value=2, bg="#FFFAF0", font="Roboto 11")
        self.rad4 = Radiobutton(self.root, text="Осреднять за сутки", variable=self.choice1, value=3, bg="#FFFAF0", font="Roboto 11")
        self.rad5 = Radiobutton(self.root, text="Мин. и макс. за сутки", variable=self.choice1, value=4, bg="#FFFAF0", font="Roboto 11")

        self.choice2 = IntVar(value=0)
        self.rad6 = Radiobutton(self.root, text="Линейный", variable=self.choice2, value=0, bg="#FFFAF0", font="Roboto 11")
        self.rad7 = Radiobutton(self.root, text="Столбчатый", variable=self.choice2, value=1, bg="#FFFAF0", font="Roboto 11")
        self.rad8 = Radiobutton(self.root, text="Точечный", variable=self.choice2, value=2, bg="#FFFAF0", font="Roboto 11")

        self.choice3 = BooleanVar(value=False)
        self.check1 = Checkbutton(self.root, text="Добавить данные", variable=self.choice3, bg="#FFFAF0", font="Roboto 11")
        self.check1.config(command=self.show_data)

        self.choice4 = BooleanVar(value=False)
        self.check2 = Checkbutton(self.root, text="Добавить данные c Gismeteo", variable=self.choice4, bg="#FFFAF0", font="Roboto 11")
        self.check2.config(command=self.show_gis)

        varD1 = IntVar(value=datetime.now().day-1)
        varM1 = IntVar(value=datetime.now().month)
        varH1 = IntVar(value=9)
        self.spinboxD1 = Spinbox(self.root, width=3, font="Roboto 10", from_=1, to=31, relief=SUNKEN, textvariable=varD1)
        self.spinboxM1 = Spinbox(self.root, width=3, font="Roboto 10", from_=1, to=13, relief=SUNKEN, textvariable=varM1)
        self.spinboxY1 = Spinbox(self.root, width=5, font="Roboto 10", from_=2022, to=2023, state='disabled', relief=SUNKEN)
        self.spinboxH1 = Spinbox(self.root, width=3, font="Roboto 10", from_=0, to=23, relief=SUNKEN, textvariable=varH1)
        self.lableS1 = Label(self.root, text=":", bg="#FFFAF0", font="Roboto 12", width=0)
        self.spinboxMin1 = Spinbox(self.root, width=3, font="Roboto 10", from_=0, to=59, relief=SUNKEN)

        varD2 = IntVar(value=datetime.now().day-1)
        varM2 = IntVar(value=datetime.now().month)
        varH2 = IntVar(value=17)
        varMin2 = IntVar(value=0)
        self.spinboxD2 = Spinbox(self.root, width=3, font="Roboto 10", from_=1, to=31, relief=SUNKEN, textvariable=varD2)
        self.spinboxM2 = Spinbox(self.root, width=3, font="Roboto 10", from_=1, to=13, relief=SUNKEN, textvariable=varM2)
        self.spinboxY2 = Spinbox(self.root, width=5, font="Roboto 10", from_=2022, to=2023, state='disabled', relief=SUNKEN)
        self.spinboxH2 = Spinbox(self.root, width=3, font="Roboto 10", from_=0, to=23, relief=SUNKEN, textvariable=varH2)
        self.lableS2 = Label(self.root, text=":", bg="#FFFAF0", font="Roboto 12", width=0)
        self.spinboxMin2 = Spinbox(self.root, width=3, font="Roboto 10", from_=0, to=59, relief=SUNKEN, textvariable=varMin2)

        self.cb_ET1 = ttk.Combobox(self.root, state="readonly", font="Roboto 11", width=1)
        self.cb_ET1['values'] = ('t', 'h')

        self.cb_ET2 = ttk.Combobox(self.root, state="readonly", font="Roboto 11", width=1)
        self.cb_ET2['values'] = ('t', 'h')

        self.current_device = StringVar(value="Не выбрано")
        self.cb_device = ttk.Combobox(self.root, textvariable=self.current_device, state="readonly", width=25, font="Roboto 11")

        self.current_dataX = StringVar(value="Не выбрано")
        self.cb_dataX = ttk.Combobox(self.root, textvariable=self.current_dataX, state="readonly", width=25, font="Roboto 11")
        self.cb_dataX.bind("<<ComboboxSelected>>", self.show_cb_dataY)

        self.current_dataY = StringVar(value="Не выбрано")
        self.cb_dataY = ttk.Combobox(self.root, textvariable=self.current_dataY, state="readonly", width=25, font="Roboto 11")
        self.cb_dataY.bind("<<ComboboxSelected>>", self.show_other)

        self.current_datadop = StringVar(value="Не выбрано")
        self.cb_datadop = ttk.Combobox(self.root, textvariable=self.current_datadop, state="readonly", width=25, font="Roboto 11")

        self.current_datagis = StringVar(value="Не выбрано")
        self.cb_datagis = ttk.Combobox(self.root, textvariable=self.current_datagis, state="readonly", width=20, font="Roboto 11")
        self.cb_datagis['values'] = ('temp', 'pressure', 'temp ,pressure')

        self.cb_gisxy = ttk.Combobox(self.root, state="readonly", font="Roboto 11", width=2)
        self.cb_gisxy['values'] = ('X', 'Y')


        self.cb_xory = ttk.Combobox(self.root, state="readonly", font="Roboto 10", width=2)
        self.cb_xory['values'] = ('X', 'Y')

        self.cb_device['values'] = \
            ('РОСА К-2 (01)', 'Роса-К-1 (01)', 'Тест Студии (schHome)', 'Сервер СЕВ (01)',
            'Сервер СЕВ (02)', 'Сервер СЕВ (03)', 'Тест воздуха (01)', 'Hydra-L (01)',
            'Hydra-L (02)', 'Hydra-L (03)', 'Hydra-L (04)', 'Hydra-L (05)', 'Hydra-L (06)',
            'Hydra-L (07)', 'Hydra-L (08)', 'Hydra-L1 (01)', 'Hydra-L1 (02)',
             'Опорный барометр (01)', 'Опорный барометр (02)', 'Сервер dokuwiki (01)',
            'Сервер dbrobo (01)', 'Сервер webrobo (01)', 'Паскаль (00)', 'Паскаль (01)', 'Паскаль (02)',
             'Паскаль (03)', 'Паскаль (04)', 'Паскаль (05)', 'Паскаль (06)', 'Паскаль (07)',
             'Паскаль (08)', 'Паскаль (09)', 'Паскаль (10)', 'Паскаль (11)', 'Паскаль (12)',
             'Паскаль (13)', 'Паскаль (14)', 'Паскаль (15)', 'Паскаль (16)', 'Паскаль (17)',
             'Паскаль (18)', 'Паскаль (19)', 'Паскаль (20)')
        self.cb_device.place(y=65, relx=0.25, anchor=CENTER)
        self.cb_device.bind("<<ComboboxSelected>>", self.show_cb_dataX)



    def open_file(self, flag=0):
        try:
            #тут нужно поставить в комбобоксах не выбрано



            x = []
            y = []

            if flag == 0:
                self.current_dataX = StringVar(value="Не выбрано")
                self.current_dataY = StringVar(value="Не выбрано")
                self.cb_dataX.configure(textvariable=self.current_dataX)
                self.cb_dataY.configure(textvariable=self.current_dataY)
                global file_name
                file_name = askopenfilename(filetypes=[("JSON file", "*.json"), ("CSV file", "*.csv")])

            if file_name[-3:] == "csv":
                file = open(file_name, "r", encoding='cp1251')
            else:
                file = open(file_name, "r", encoding='utf-8')

            global data_list
            global lines
            if file_name[-3:] == "csv":
                firstline = file.readline()
                #в зависимости от выбранного файла настраиваем 1-й комбобокс
                self.current_device = firstline.split(';')[1]  #название прибора
                self.cb_device.config(textvariable=firstline.split(';')[1])
                self.cb_device.set(firstline.split(';')[1])
                self.cb_device.config(state='disabled')

                data_list = file.readline().split(';')[0:-1]
                self.show_cb_dataX(self) #передали список даты

                lines = csv.reader(file, delimiter=';')
            else:
                self.cb_device.config(state='readonly')
                lines = json.load(file)

        except FileNotFoundError:
            showinfo("Error", "File not loaded")


    def show_cb_dataX(self, event):
        if file_name[-3:] == "csv":
            self.cb_device.config(state='disabled') #выкл комбобох
        else:
            global data_list
            data_list = []
            data_list.append('Date')
            self.current_dataX.set('Не выбрано')
            self.current_dataY.set('Не выбрано')
            self.current_datadop.set('Не выбрано')

            for unit in lines:
                if unit['uName'] + ' ' + '(' + unit['serial'] + ')' == self.cb_device.get():
                    for name in unit['data']:
                        if unit['uName'].find('Сервер') == -1:
                            #if name.find('system') == -1:
                            data_list.append(name)
                        else:
                            data_list.append(name)
                    break
        self.cb_dataX['values'] = data_list

        self.lable2.place(y=105, relx=0.25, anchor=CENTER) #x=55
        self.lable3.place(x=295, y=133)
        self.cb_dataX.place(y=145, relx=0.25, anchor=CENTER) #x=30


    def show_cb_dataY(self, event):
        self.cb_dataY['values'] = data_list
        self.lable4.place(x=295, y=173)
        self.cb_dataY.place(y=185, relx=0.25, anchor=CENTER) #x=30



    def show_other(self, event):
        self.button1.place(y=520, relx=0.3, anchor=CENTER) #x-290
        self.button2.place(y=520, relx=0.7, anchor=CENTER)

        self.check1.place(y=330, relx=0.25, anchor=CENTER)
        self.check2.place(y=330, relx=0.75, anchor=CENTER)

        self.lable5.place(y=25, relx=0.75, anchor=CENTER) #x=455
        self.rad1.place(y=65, relx=0.58, anchor=W) #x=380 у всех
        self.rad2.place(y=95, relx=0.58, anchor=W)
        self.rad3.place(y=125, relx=0.58, anchor=W)
        self.rad4.place(y=155, relx=0.58, anchor=W)
        self.rad5.place(y=185, relx=0.58, anchor=W)

        self.lable8.place(y=430, relx=0.5, anchor=CENTER)
        self.rad6.place(y=470, relx=0.25, anchor=CENTER)
        self.rad7.place(y=470, relx=0.5, anchor=CENTER)
        self.rad8.place(y=470, relx=0.75, anchor=CENTER)

        self.lable6.place(y=240, relx=0.25, anchor=CENTER) #x=70
        self.lable7.place(y=240, relx=0.75, anchor=CENTER) #x=435

        self.spinboxD1.place(x=65,y=275)
        self.spinboxM1.place(x=103, y=275)
        self.spinboxY1.place(x=141, y=275)
        self.spinboxH1.place(x=207, y=275)
        self.lableS1.place(x=242, y=272)
        self.spinboxMin1.place(x=252, y=275)

        self.spinboxD2.place(x=415, y=275)
        self.spinboxM2.place(x=453, y=275)
        self.spinboxY2.place(x=491, y=275)
        self.spinboxH2.place(x=557, y=275)
        self.lableS2.place(x=592, y=272)
        self.spinboxMin2.place(x=602, y=275)

        self.cb_ET1.place(x=25, y=134)
        self.cb_ET2.place(x=25, y=174)

    def show_data(self):
        if self.choice3.get() == True:
            self.cb_datadop['values'] = data_list[1:]
            #self.cb_datadop.configure(textvariable='')
            self.cb_datadop.place(y=375, relx=0.25, anchor=CENTER)
            self.lable9.place(x=295, y=363)
            self.cb_xory.place(x=345, y=365)
        else:
            self.cb_datadop.place_forget()
            self.lable9.place_forget()
            self.cb_xory.place_forget()

    def show_gis(self):
        if self.choice4.get() == True:
            self.cb_datagis.place(y=375, relx=0.72, anchor=CENTER)
            self.lable10.place(x=600, y=363)
            self.cb_gisxy.place(x=650, y=365)
        else:
            self.cb_datagis.place_forget()
            self.lable10.place_forget()
            self.cb_gisxy.place_forget()


    def select_data(self):
        D1 = int(self.spinboxD1.get())
        D2 = int(self.spinboxD2.get())
        M1 = int(self.spinboxM1.get())
        M2 = int(self.spinboxM2.get())
        H1 = int(self.spinboxH1.get())
        H2 = int(self.spinboxH2.get())
        Min1 = int(self.spinboxMin1.get())
        Min2 = int(self.spinboxMin2.get())

        x_arr = []
        y_arr = []
        xmin_arr = []
        xmax_arr = []
        ymin_arr = []
        ymax_arr = []

        flag = 0
        flagMid = 0
        wait_day = 0
        wait_hour = 0
        wait_min = 0
        middleX = []
        middleY = []

        x = self.cb_dataX.current()
        y = self.cb_dataY.current()

        x_value = self.cb_dataX.get()
        y_value = self.cb_dataY.get()

        if file_name[-3:] == "csv":

            for row in lines:
                cur_day = int(row[0][0:row[0].find(' ')].split('-')[2])
                cur_mounth = int(row[0][0:row[0].find(' ')].split('-')[1])
                cur_min = int(row[0][row[0].find(' ') + 1:].split(':')[1])
                cur_hour = int(row[0][row[0].find(' ') + 1:].split(':')[0])
                if (cur_mounth == M1 and cur_day > D1) or (cur_mounth > M1) \
                        or (cur_mounth == M1 and cur_day == D1 and cur_hour > H1) \
                        or (cur_mounth == M1 and cur_day == D1 and cur_hour == H1 and cur_min >= Min1):
                    flag = 1
                if (cur_mounth == M2 and cur_day > D2) or (cur_mounth > M2) \
                        or (cur_mounth == M2 and cur_day == D2 and cur_hour > H2) \
                        or (cur_mounth == M2 and cur_day == D2 and cur_hour == H2 and cur_min >= Min2):
                    flag = 0

                if flag == 1:

                    if self.choice1.get() == 0:  # как есть
                        if x == 0:
                            x_arr.append(row[x])
                            y_arr.append(float(row[y]))
                        elif y == 0:
                            x_arr.append(float(row[x]))
                            y_arr.append(row[y])
                        else:
                            x_arr.append(float(row[x]))
                            y_arr.append(float(row[y]))


                    elif self.choice1.get() == 1:  # час################################################

                        if flagMid == 0:
                            flagMid = 1
                            wait_hour = (cur_hour + 1) % 24
                            wait_min = cur_hour
                            if x == 0:
                                middleY.append(float(row[y]))
                            elif y == 0:
                                middleX.append(float(row[x]))
                            else:
                                middleX.append(float(row[x]))
                                middleY.append(float(row[y]))

                        elif flagMid == 1:
                            if cur_hour != wait_hour or (cur_hour == wait_hour and cur_min < wait_min):
                                if x == 0:
                                    middleY.append(float(row[y]))
                                elif y == 0:
                                    middleX.append(float(row[x]))
                                else:
                                    middleX.append(float(row[x]))
                                    middleY.append(float(row[y]))

                            else:  # прошел час
                                if x == 0:
                                    x_arr.append(row[x][0:-6])
                                    y_arr.append(sum(middleY) / len(middleY))
                                elif y == 0:
                                    x_arr.append(sum(middleX) / len(middleX))
                                    y_arr.append(row[y][0:-6])
                                else:
                                    x_arr.append(sum(middleX) / len(middleX))
                                    y_arr.append(sum(middleY) / len(middleY))
                                middleX = []
                                middleY = []

                                wait_hour = (cur_hour + 1) % 24
                                wait_min = cur_min
                                if x == 0:
                                    middleY.append(float(row[y]))
                                elif y == 0:
                                    middleX.append(float(row[x]))
                                else:
                                    middleX.append(float(row[x]))
                                    middleY.append(float(row[y]))


                    elif self.choice1.get() == 2:  # 3 часа ################################################
                        # если не хватило часов можно закинуть как есть
                        if flagMid == 0:
                            flagMid = 1
                            wait_hour = (cur_hour + 3) % 24
                            wait_min = cur_hour
                            if x == 0:
                                middleY.append(float(row[y]))
                            elif y == 0:
                                middleX.append(float(row[x]))
                            else:
                                middleX.append(float(row[x]))
                                middleY.append(float(row[y]))

                        elif flagMid == 1:
                            if cur_hour != wait_hour or (cur_hour == wait_hour and cur_min < wait_min):
                                if x == 0:
                                    middleY.append(float(row[y]))
                                elif y == 0:
                                    middleX.append(float(row[x]))
                                else:
                                    middleX.append(float(row[x]))
                                    middleY.append(float(row[y]))

                            else:  # прошло 3 часа
                                if x == 0:
                                    x_arr.append(row[x][0:-6])
                                    y_arr.append(sum(middleY) / len(middleY))
                                elif y == 0:
                                    x_arr.append(sum(middleX) / len(middleX))
                                    y_arr.append(row[y][0:-6])
                                else:
                                    x_arr.append(sum(middleX) / len(middleX))
                                    y_arr.append(sum(middleY) / len(middleY))
                                middleX = []
                                middleY = []

                                wait_hour = (cur_hour + 3) % 24
                                wait_min = cur_min
                                if x == 0:
                                    middleY.append(float(row[y]))
                                elif y == 0:
                                    middleX.append(float(row[x]))
                                else:
                                    middleX.append(float(row[x]))
                                    middleY.append(float(row[y]))

                    elif self.choice1.get() == 3:  # сутки #################################################

                        if flagMid == 0:
                            flagMid = 1

                            wait_day = cur_day + 1
                            wait_hour = cur_hour
                            if x == 0:
                                middleY.append(float(row[y]))
                            elif y == 0:
                                middleX.append(float(row[x]))
                            else:
                                middleX.append(float(row[x]))
                                middleY.append(float(row[y]))
                            last_data = row[x][:10]

                        elif flagMid == 1:
                            if (wait_day - cur_day) == 1 or ((wait_day - cur_day) != 1 and cur_hour < wait_hour):
                                if x == 0:
                                    middleY.append(float(row[y]))
                                elif y == 0:
                                    middleX.append(float(row[x]))
                                else:
                                    middleX.append(float(row[x]))
                                    middleY.append(float(row[y]))

                            else:  # прошли сутки
                                if x == 0:
                                    x_arr.append(last_data)
                                    y_arr.append(sum(middleY) / len(middleY))
                                elif y == 0:
                                    x_arr.append(sum(middleX) / len(middleX))
                                    y_arr.append(last_data)
                                else:
                                    x_arr.append(sum(middleX) / len(middleX))
                                    y_arr.append(sum(middleY) / len(middleY))
                                middleX = []
                                middleY = []


                                wait_day = cur_day + 1
                                wait_hour = cur_hour
                                if x == 0:
                                    last_data = row[x][:10]
                                    middleY.append(float(row[y]))
                                elif y == 0:
                                    middleX.append(float(row[x]))
                                    last_data = row[y][:10]
                                else:
                                    middleX.append(float(row[x]))
                                    middleY.append(float(row[y]))

                    #все хуня давай по новой, нужно два графика
                    elif self.choice1.get() == 4:  # мин и макс за сутки
                        if flagMid == 0:
                            flagMid = 1
                            wait_day = cur_day + 1
                            wait_hour = cur_hour
                            if x == 0:
                                middleY.append(float(row[y]))
                            elif y == 0:
                                middleX.append(float(row[x]))
                            else:
                                middleX.append(float(row[x]))
                                middleY.append(float(row[y]))

                        elif flagMid == 1:
                            if (wait_day - cur_day) == 1 or ((wait_day - cur_day) != 1 and cur_hour < wait_hour):
                                if x == 0:
                                    middleY.append(float(row[y]))
                                elif y == 0:
                                    middleX.append(float(row[x]))
                                else:
                                    middleX.append(float(row[x]))
                                    middleY.append(float(row[y]))

                            else:  # прошли сутки
                                if x == 0:
                                    xmin_arr.append(row[x][:10])
                                    xmax_arr.append(row[x][:10])
                                    middleY.sort()
                                    ymin_arr.append(middleY[0]) #добавили мин
                                    ymax_arr.append(middleY[-1]) #добавили макс
                                elif y == 0:
                                    middleX.sort()
                                    xmin_arr.append(middleX[0])
                                    xmax_arr.append(middleX[-1])
                                    ymin_arr.append(row[y][:10])
                                    ymax_arr.append(row[y][:10])
                                else:
                                    middleX.sort()
                                    middleY.sort()
                                    xmin_arr.append(middleX[0])
                                    xmax_arr.append(middleX[-1])
                                    ymin_arr.append(middleY[0])
                                    ymax_arr.append(middleY[-1])

                                middleX = []
                                middleY = []

                                wait_day = cur_day + 1
                                wait_hour = cur_hour
                                if x == 0:
                                    middleY.append(float(row[y]))
                                elif y == 0:
                                    middleX.append(float(row[x]))
                                else:
                                    middleX.append(float(row[x]))
                                    middleY.append(float(row[y]))



            if (len(middleX) > 0 or len(middleY) > 0) and (self.choice1.get() == 1 or self.choice1.get() == 2):
                if x == 0:
                    x_arr.append(row[x][0:-6])
                    y_arr.append(sum(middleY) / len(middleY))
                elif y == 0:
                    x_arr.append(sum(middleX) / len(middleX))
                    y_arr.append(row[y][0:-6])
                else:
                    x_arr.append(sum(middleX) / len(middleX))
                    y_arr.append(sum(middleY) / len(middleY))
                middleX = []
                middleY = []
            elif (len(middleX) > 0 or len(middleY) > 0) and self.choice1.get() == 3:
                if x == 0:
                    x_arr.append(last_data)
                    y_arr.append(sum(middleY) / len(middleY))
                elif y == 0:
                    x_arr.append(sum(middleX) / len(middleX))
                    y_arr.append(last_data)
                else:
                    x_arr.append(sum(middleX) / len(middleX))
                    y_arr.append(sum(middleY) / len(middleY))
                middleX = []
                middleY = []

            elif (len(middleX) > 2 or len(middleY) > 2) and self.choice1.get() == 4:
                if x == 0:
                    xmin_arr.append(row[x][:10])
                    xmax_arr.append(row[x][:10])
                    middleY.sort()
                    ymin_arr.append(middleY[0])  # добавили мин
                    ymax_arr.append(middleY[-1])  # добавили макс
                elif y == 0:
                    middleX.sort()
                    xmin_arr.append(middleX[0])
                    xmax_arr.append(middleX[-1])
                    ymin_arr.append(row[y][:10])
                    ymax_arr.append(row[y][:10])
                else:
                    middleX.sort()
                    middleY.sort()
                    xmin_arr.append(middleX[0])
                    xmax_arr.append(middleX[-1])
                    ymin_arr.append(middleY[0])
                    ymax_arr.append(middleY[-1])

                middleX = []
                middleY = []

            else:
                pass



        else:
            for unit in lines:
                if unit['uName'] + ' ' + '(' + unit['serial'] + ')' == self.cb_device.get() :
                    cur_day = int(unit['Date'][0:unit['Date'].find(' ')].split('-')[2])
                    cur_mounth = int(unit['Date'][0:unit['Date'].find(' ')].split('-')[1])
                    cur_min = int(unit['Date'][unit['Date'].find(' ') + 1:].split(':')[1])
                    cur_hour = int(unit['Date'][unit['Date'].find(' ') + 1:].split(':')[0])
                    if (cur_mounth == M1 and cur_day > D1) or (cur_mounth > M1) \
                            or (cur_mounth == M1 and cur_day == D1 and cur_hour > H1) \
                            or (cur_mounth == M1 and cur_day == D1 and cur_hour == H1 and cur_min >= Min1):
                        flag = 1
                    if (cur_mounth == M2 and cur_day > D2) or (cur_mounth > M2) \
                            or (cur_mounth == M2 and cur_day == D2 and cur_hour > H2) \
                            or (cur_mounth == M2 and cur_day == D2 and cur_hour == H2 and cur_min >= Min2):
                        flag = 0

                    if flag == 1:

                        if self.choice1.get() == 0:  # как есть
                            if x == 0:
                                x_arr.append(unit[x_value])
                                y_arr.append(float(unit['data'][y_value]))
                            elif y == 0:
                                x_arr.append(float(unit['data'][x_value]))
                                y_arr.append(unit[y_value])
                            else:
                                x_arr.append(float(unit['data'][x_value]))
                                y_arr.append(float(unit['data'][y_value]))

                        elif self.choice1.get() == 1:  # час################################################
                            if flagMid == 0:
                                flagMid = 1
                                wait_hour = (cur_hour + 1) % 24
                                wait_min = cur_hour
                                if x == 0:
                                    middleY.append(float(unit['data'][y_value]))
                                elif y == 0:
                                    middleX.append(float(unit['data'][x_value]))
                                else:
                                    middleX.append(float(unit['data'][x_value]))
                                    middleY.append(float(unit['data'][y_value]))

                            elif flagMid == 1:
                                if cur_hour != wait_hour or (cur_hour == wait_hour and cur_min < wait_min):
                                    if x == 0:
                                        middleY.append(float(unit['data'][y_value]))
                                    elif y == 0:
                                        middleX.append(float(unit['data'][x_value]))
                                    else:
                                        middleX.append(float(unit['data'][x_value]))
                                        middleY.append(float(unit['data'][y_value]))

                                else:  # прошел час
                                    if x == 0:
                                        x_arr.append(unit[x_value][0:-6])
                                        y_arr.append(sum(middleY) / len(middleY))
                                    elif y == 0:
                                        x_arr.append(sum(middleX) / len(middleX))
                                        y_arr.append(unit[y_value][0:-6])
                                    else:
                                        x_arr.append(sum(middleX) / len(middleX))
                                        y_arr.append(sum(middleY) / len(middleY))
                                    middleX = []
                                    middleY = []

                                    wait_hour = (cur_hour + 1) % 24
                                    wait_min = cur_min
                                    if x == 0:
                                        middleY.append(float(unit['data'][y_value]))
                                    elif y == 0:
                                        middleX.append(float(unit['data'][x_value]))
                                    else:
                                        middleX.append(float(unit['data'][x_value]))
                                        middleY.append(float(unit['data'][y_value]))

                        elif self.choice1.get() == 2:  # 3 часа ################################################
                            # если не хватило часов можно закинуть как есть
                            if flagMid == 0:
                                flagMid = 1
                                wait_hour = (cur_hour + 3) % 24
                                wait_min = cur_hour
                                if x == 0:
                                    middleY.append(float(unit['data'][y_value]))
                                elif y == 0:
                                    middleX.append(float(unit['data'][x_value]))
                                else:
                                    middleX.append(float(unit['data'][x_value]))
                                    middleY.append(float(unit['data'][y_value]))

                            elif flagMid == 1:
                                if cur_hour != wait_hour or (cur_hour == wait_hour and cur_min < wait_min):
                                    if x == 0:
                                        middleY.append(float(unit['data'][y_value]))
                                    elif y == 0:
                                        middleX.append(float(unit['data'][x_value]))
                                    else:
                                        middleX.append(float(unit['data'][x_value]))
                                        middleY.append(float(unit['data'][y_value]))

                                else:  # прошло 3 часа
                                    if x == 0:
                                        x_arr.append(unit[x_value][0:-6])
                                        y_arr.append(sum(middleY) / len(middleY))
                                    elif y == 0:
                                        x_arr.append(sum(middleX) / len(middleX))
                                        y_arr.append(unit[y_value][0:-6])
                                    else:
                                        x_arr.append(sum(middleX) / len(middleX))
                                        y_arr.append(sum(middleY) / len(middleY))
                                    middleX = []
                                    middleY = []

                                    wait_hour = (cur_hour + 3) % 24
                                    wait_min = cur_min
                                    if x == 0:
                                        middleY.append(float(unit['data'][y_value]))
                                    elif y == 0:
                                        middleX.append(float(unit['data'][x_value]))
                                    else:
                                        middleX.append(float(unit['data'][x_value]))
                                        middleY.append(float(unit['data'][y_value]))

                        elif self.choice1.get() == 3:  # сутки #################################################
                            if flagMid == 0:
                                flagMid = 1

                                wait_day = cur_day + 1
                                wait_hour = cur_hour
                                if x == 0:
                                    middleY.append(float(unit['data'][y_value]))
                                elif y == 0:
                                    middleX.append(float(unit['data'][x_value]))
                                else:
                                    middleX.append(float(unit['data'][x_value]))
                                    middleY.append(float(unit['data'][y_value]))

                            elif flagMid == 1:
                                if (wait_day - cur_day) == 1 or ((wait_day - cur_day) != 1 and cur_hour < wait_hour):
                                    if x == 0:
                                        middleY.append(float(unit['data'][y_value]))
                                    elif y == 0:
                                        middleX.append(float(unit['data'][x_value]))
                                    else:
                                        middleX.append(float(unit['data'][x_value]))
                                        middleY.append(float(unit['data'][y_value]))

                                else:  # прошли сутки
                                    if x == 0:
                                        x_arr.append(unit[x_value][:10])
                                        y_arr.append(sum(middleY) / len(middleY))
                                    elif y == 0:
                                        x_arr.append(sum(middleX) / len(middleX))
                                        y_arr.append(unit[y_value][:10])
                                    else:
                                        x_arr.append(sum(middleX) / len(middleX))
                                        y_arr.append(sum(middleY) / len(middleY))
                                    middleX = []
                                    middleY = []

                                    wait_day = cur_day + 1
                                    wait_hour = cur_hour
                                    if x == 0:
                                        middleY.append(float(unit['data'][y_value]))
                                    elif y == 0:
                                        middleX.append(float(unit['data'][x_value]))
                                    else:
                                        middleX.append(float(unit['data'][x_value]))
                                        middleY.append(float(unit['data'][y_value]))

                        elif self.choice1.get() == 4:  # мин и макс за сутки
                            if flagMid == 0:
                                flagMid = 1
                                wait_day = cur_day + 1
                                wait_hour = cur_hour
                                if x == 0:
                                    middleY.append(float(unit['data'][y_value]))
                                elif y == 0:
                                    middleX.append(float(unit['data'][x_value]))
                                else:
                                    middleX.append(float(unit['data'][x_value]))
                                    middleY.append(float(unit['data'][y_value]))

                            elif flagMid == 1:
                                if (wait_day - cur_day) == 1 or ((wait_day - cur_day) != 1 and cur_hour < wait_hour):
                                    if x == 0:
                                        middleY.append(float(unit['data'][y_value]))
                                    elif y == 0:
                                        middleX.append(float(unit['data'][x_value]))
                                    else:
                                        middleX.append(float(unit['data'][x_value]))
                                        middleY.append(float(unit['data'][y_value]))

                                else:  # прошли сутки
                                    if x == 0:
                                        xmin_arr.append(unit[x_value][:10])
                                        xmax_arr.append(unit[x_value][:10])
                                        middleY.sort()
                                        ymin_arr.append(middleY[0])  # добавили мин
                                        ymax_arr.append(middleY[-1])  # добавили макс
                                    elif y == 0:
                                        middleX.sort()
                                        xmin_arr.append(middleX[0])
                                        xmax_arr.append(middleX[-1])
                                        ymin_arr.append(unit[y_value][:10])
                                        ymax_arr.append(unit[y_value][:10])
                                    else:
                                        middleX.sort()
                                        middleY.sort()
                                        xmin_arr.append(middleX[0])
                                        xmax_arr.append(middleX[-1])
                                        ymin_arr.append(middleY[0])
                                        ymax_arr.append(middleY[-1])

                                    middleX = []
                                    middleY = []

                                    wait_day = cur_day + 1
                                    wait_hour = cur_hour
                                    if x == 0:
                                        middleY.append(float(unit['data'][y_value]))
                                    elif y == 0:
                                        middleX.append(float(unit['data'][x_value]))
                                    else:
                                        middleX.append(float(unit['data'][x_value]))
                                        middleY.append(float(unit['data'][y_value]))

            if (len(middleX) > 0 or len(middleY) > 0) and (
                    self.choice1.get() == 1 or self.choice1.get() == 2):
                if x == 0:
                    x_arr.append(unit[x_value][0:-6])
                    y_arr.append(sum(middleY) / len(middleY))
                elif y == 0:
                    x_arr.append(sum(middleX) / len(middleX))
                    y_arr.append(unit[y_value][0:-6])
                else:
                    x_arr.append(sum(middleX) / len(middleX))
                    y_arr.append(sum(middleY) / len(middleY))
                middleX = []
                middleY = []

            elif (len(middleX) > 0 or len(middleY) > 0) and self.choice1.get() == 3:
                if x == 0:
                    x_arr.append(unit[x_value][:10])
                    y_arr.append(sum(middleY) / len(middleY))
                elif y == 0:
                    x_arr.append(sum(middleX) / len(middleX))
                    y_arr.append(unit[y_value][:10])
                else:
                    x_arr.append(sum(middleX) / len(middleX))
                    y_arr.append(sum(middleY) / len(middleY))
                middleX = []
                middleY = []

            elif (len(middleX) > 2 or len(middleY) > 2) and self.choice1.get() == 4:
                if x == 0:
                    xmin_arr.append(unit[x_value][:10])
                    xmax_arr.append(unit[x_value][:10])
                    middleY.sort()
                    ymin_arr.append(middleY[0])  # добавили мин
                    ymax_arr.append(middleY[-1])  # добавили макс
                elif y == 0:
                    middleX.sort()
                    xmin_arr.append(middleX[0])
                    xmax_arr.append(middleX[-1])
                    ymin_arr.append(unit[y_value][:10])
                    ymax_arr.append(unit[y_value][:10])
                else:
                    middleX.sort()
                    middleY.sort()
                    xmin_arr.append(middleX[0])
                    xmax_arr.append(middleX[-1])
                    ymin_arr.append(middleY[0])
                    ymax_arr.append(middleY[-1])

                middleX = []
                middleY = []

            else:
                pass

        if len(xmin_arr) > 0:
            return xmin_arr, ymin_arr, xmax_arr, ymax_arr
        else:
            return x_arr, y_arr

    def check_param(self):
        D1 = int(self.spinboxD1.get())
        D2 = int(self.spinboxD2.get())
        M1 = int(self.spinboxM1.get())
        M2 = int(self.spinboxM2.get())
        H1 = int(self.spinboxH1.get())
        H2 = int(self.spinboxH2.get())
        Min1 = int(self.spinboxMin1.get())
        Min2 = int(self.spinboxMin2.get())
        if (D1 < 22 and M1 == 4) or ((D2 > 23 or (D2 == 23 and (H2 > 0))) and M2 == 5):
            showinfo(title="Внимание!",
                     message="Начало интервала не ранее 22.04.22\nКонец интервала не позднее 23.05.22 00:00")
            return -1
        if (D1 > 30 and M1 == 4) or (D2 > 30 and M2 == 4):
            showinfo(title="Внимание!", message="В апреле всего 30 дней!")
            return -1
        if M1 > M2 or (M1 == M2 and D1 > D2) or (M1 == M2 and D1 == D2 and H1 > H2) or (
                M1 == M2 and D1 == D2 and H1 == H2 and Min1 > Min2):
            showinfo(title="Внимание!", message="Конечная дата должна быть позже начальной")
            return -1
        if self.cb_dataX.current() == -1 or self.cb_dataY.current() == -1:
            showinfo(title="Внимание!", message="Выберите данные для обработки")
            return -1
        if self.cb_dataX.current() == self.cb_dataY.current():
            showinfo(title="Внимание!", message="Выберите разные данные для обработки")
            return -1
        if self.choice3.get() == True and self.cb_xory.current() == -1:
            showinfo(title="Внимание!", message="Выберите ось для доп данных или уберите галочку")
            return -1
        if self.choice4.get() == True:
            if self.cb_datagis.current() == -1:
                showinfo(title="Внимание!", message="Выберите данные с Gismeteo или уберите галочку")
                return -1
            if self.cb_gisxy.current() == -1:
                showinfo(title="Внимание!", message="Выберите ось для данных c Gismeteo или уберите галочку")
                return -1
            if self.choice1.get() != 3:
                showinfo(title="Внимание!", message="Gismeteo показывает данные осредненные за сутки\nВыберите соответствующий парамер")
                return -1

    def selectET_data(self):
        D1 = int(self.spinboxD1.get())
        D2 = int(self.spinboxD2.get())
        M1 = int(self.spinboxM1.get())
        M2 = int(self.spinboxM2.get())
        H1 = int(self.spinboxH1.get())
        H2 = int(self.spinboxH2.get())
        Min1 = int(self.spinboxMin1.get())
        Min2 = int(self.spinboxMin2.get())


        if self.cb_ET1.current() == 0:
            t = self.cb_dataX.current()
            h = self.cb_dataY.current()
            t_value = self.cb_dataX.get()
            h_value = self.cb_dataY.get()
        else:
            t = self.cb_dataY.current()
            h = self.cb_dataX.current()
            t_value = self.cb_dataY.get()
            h_value = self.cb_dataX.get()

        x_arr = []
        y_arr = []
        xmin_arr = []
        xmax_arr = []
        ymin_arr = []
        ymax_arr = []

        flag = 0
        flagMid = 0
        wait_day = 0
        wait_hour = 0
        wait_min = 0
        middlet = []
        middleh = []

        if file_name[-3:] == "csv":

            for row in lines:
                cur_day = int(row[0][0:row[0].find(' ')].split('-')[2])
                cur_mounth = int(row[0][0:row[0].find(' ')].split('-')[1])
                cur_min = int(row[0][row[0].find(' ') + 1:].split(':')[1])
                cur_hour = int(row[0][row[0].find(' ') + 1:].split(':')[0])

                if (cur_mounth == M1 and cur_day > D1) or (cur_mounth > M1) \
                        or (cur_mounth == M1 and cur_day == D1 and cur_hour > H1) \
                        or (cur_mounth == M1 and cur_day == D1 and cur_hour == H1 and cur_min >= Min1):
                    flag = 1
                if (cur_mounth == M2 and cur_day > D2) or (cur_mounth > M2) \
                        or (cur_mounth == M2 and cur_day == D2 and cur_hour > H2) \
                        or (cur_mounth == M2 and cur_day == D2 and cur_hour == H2 and cur_min >= Min2):
                    flag = 0

                if flag == 1:

                    if self.choice1.get() == 0:
                        x_arr.append(row[0])
                        #ЭТ=t−0.4∗( t−10)∗(1−h/100)
                        cur_t = float(row[t])
                        cur_h = float(row[h])
                        y_arr.append(cur_t-0.4*(cur_t-10)*(1-cur_h/100))

                    elif self.choice1.get() == 1:  # час################################################

                        if flagMid == 0:
                            flagMid = 1
                            wait_hour = (cur_hour + 1) % 24
                            wait_min = cur_hour

                            middlet.append(float(row[t]))
                            middleh.append(float(row[h]))

                        elif flagMid == 1:
                            if cur_hour != wait_hour or (cur_hour == wait_hour and cur_min < wait_min):

                                middlet.append(float(row[t]))
                                middleh.append(float(row[h]))

                            else:  # прошел час
                                x_arr.append(row[0][:-6])
                                cur_t = sum(middlet) / len(middlet)
                                cur_h = sum(middleh) / len(middleh)
                                y_arr.append(cur_t-0.4*(cur_t-10)*(1-cur_h/100))
                                middlet = []
                                middleh = []

                                wait_hour = (cur_hour + 1) % 24
                                wait_min = cur_min

                                middlet.append(float(row[t]))
                                middleh.append(float(row[h]))


                    elif self.choice1.get() == 2:  # 3 часа ################################################

                        if flagMid == 0:
                            flagMid = 1
                            wait_hour = (cur_hour + 3) % 24
                            wait_min = cur_hour

                            middlet.append(float(row[t]))
                            middleh.append(float(row[h]))

                        elif flagMid == 1:
                            if cur_hour != wait_hour or (cur_hour == wait_hour and cur_min < wait_min):

                                middlet.append(float(row[t]))
                                middleh.append(float(row[h]))

                            else:
                                x_arr.append(row[0][:-6])
                                cur_t = sum(middlet) / len(middlet)
                                cur_h = sum(middleh) / len(middleh)
                                y_arr.append(cur_t - 0.4 * (cur_t - 10) * (1 - cur_h / 100))
                                middlet = []
                                middleh = []

                                wait_hour = (cur_hour + 3) % 24
                                wait_min = cur_min

                                middlet.append(float(row[t]))
                                middleh.append(float(row[h]))

                    elif self.choice1.get() == 3:  # сутки #################################################
                        if flagMid == 0:
                            flagMid = 1

                            wait_day = cur_day + 1
                            wait_hour = cur_hour

                            middlet.append(float(row[t]))
                            middleh.append(float(row[h]))

                        elif flagMid == 1:
                            if (wait_day - cur_day) == 1 or ((wait_day - cur_day) != 1 and cur_hour < wait_hour):

                                middlet.append(float(row[t]))
                                middleh.append(float(row[h]))

                            else:  # прошли сутки
                                x_arr.append(row[0][:10])
                                cur_t = sum(middlet) / len(middlet)
                                cur_h = sum(middleh) / len(middleh)
                                y_arr.append(cur_t - 0.4 * (cur_t - 10) * (1 - cur_h / 100))
                                middlet = []
                                middleh = []

                                wait_day = cur_day + 1
                                wait_hour = cur_hour

                                middlet.append(float(row[t]))
                                middleh.append(float(row[h]))

                    elif self.choice1.get() == 4:  # мин и макс за сутки
                        if flagMid == 0:
                            flagMid = 1
                            wait_day = cur_day + 1
                            wait_hour = cur_hour

                            middlet.append(float(row[t]))
                            middleh.append(float(row[h]))

                        elif flagMid == 1:
                            if (wait_day - cur_day) == 1 or ((wait_day - cur_day) != 1 and cur_hour < wait_hour):
                                middlet.append(float(row[t]))
                                middleh.append(float(row[h]))

                            else:  # прошли сутки
                                xmin_arr.append(row[0][:10])
                                xmax_arr.append(row[0][:10])
                                middlet.sort()
                                middleh.sort()
                                cur_tmin = middlet[0]
                                cur_tmax = middlet[-1]
                                cur_hmin = middleh[0]
                                cur_hmax = middleh[-1]
                                ymin_arr.append(cur_tmin - 0.4 * (cur_tmin - 10) * (1 - cur_hmin / 100))
                                ymax_arr.append(cur_tmax - 0.4 * (cur_tmax - 10) * (1 - cur_hmax / 100))

                                middlet = []
                                middleh = []

                                wait_day = cur_day + 1
                                wait_hour = cur_hour

                                middlet.append(float(row[t]))
                                middleh.append(float(row[h]))



            if (len(middlet) > 0 or len(middleh) > 0) and (
                    self.choice1.get() == 1 or self.choice1.get() == 2):
                cur_t = sum(middlet) / len(middlet)
                cur_h = sum(middleh) / len(middleh)
                y_arr.append(cur_t - 0.4 * (cur_t - 10) * (1 - cur_h / 100))
                x_arr.append(row[0][:-6])

                middleX = []
                middleY = []
            elif (len(middlet) > 0 or len(middleh) > 0) and self.choice1.get() == 3:
                cur_t = sum(middlet) / len(middlet)
                cur_h = sum(middleh) / len(middleh)
                y_arr.append(cur_t - 0.4 * (cur_t - 10) * (1 - cur_h / 100))
                x_arr.append(row[0][:10])

                middleX = []
                middleY = []

            elif (len(middlet) > 2 or len(middleh) > 2) and self.choice1.get() == 4:
                xmin_arr.append(row[0][:10])
                xmax_arr.append(row[0][:10])

                middlet.sort()
                middleh.sort()
                cur_tmin = middlet[0]
                cur_tmax = middlet[-1]
                cur_hmin = middleh[0]
                cur_hmax = middleh[-1]
                ymin_arr.append(cur_tmin - 0.4 * (cur_tmin - 10) * (1 - cur_hmin / 100))
                ymax_arr.append(cur_tmax - 0.4 * (cur_tmax - 10) * (1 - cur_hmax / 100))

                middlet = []
                middleh = []

            else:
                pass

        else:

            for unit in lines:

                if unit['uName'] + ' ' + '(' + unit['serial'] + ')' == self.cb_device.get():
                    cur_day = int(unit['Date'][0:unit['Date'].find(' ')].split('-')[2])
                    cur_mounth = int(unit['Date'][0:unit['Date'].find(' ')].split('-')[1])
                    cur_min = int(unit['Date'][unit['Date'].find(' ') + 1:].split(':')[1])
                    cur_hour = int(unit['Date'][unit['Date'].find(' ') + 1:].split(':')[0])

                    if (cur_mounth == M1 and cur_day > D1) or (cur_mounth > M1) \
                            or (cur_mounth == M1 and cur_day == D1 and cur_hour > H1) \
                            or (cur_mounth == M1 and cur_day == D1 and cur_hour == H1 and cur_min >= Min1):
                        flag = 1
                    elif (cur_mounth == M2 and cur_day > D2) or (cur_mounth > M2) \
                            or (cur_mounth == M2 and cur_day == D2 and cur_hour > H2) \
                            or (cur_mounth == M2 and cur_day == D2 and cur_hour == H2 and cur_min >= Min2):
                        flag = 0

                    if flag == 1:

                        if self.choice1.get() == 0:
                            x_arr.append(unit['Date'])
                            # ЭТ=t−0.4∗( t−10)∗(1−h/100)
                            cur_t = float(unit['data'][t_value])
                            cur_h = float(unit['data'][h_value])
                            y_arr.append(cur_t - 0.4 * (cur_t - 10) * (1 - cur_h / 100))

                        elif self.choice1.get() == 1:  # час################################################

                            if flagMid == 0:
                                flagMid = 1
                                wait_hour = (cur_hour + 1) % 24
                                wait_min = cur_hour

                                middlet.append(float(unit['data'][t_value]))
                                middleh.append(float(unit['data'][h_value]))

                            elif flagMid == 1:
                                if cur_hour != wait_hour or (cur_hour == wait_hour and cur_min < wait_min):

                                    middlet.append(float(unit['data'][t_value]))
                                    middleh.append(float(unit['data'][h_value]))

                                else:  # прошел час
                                    x_arr.append(unit['Date'][:-6])
                                    cur_t = sum(middlet) / len(middlet)
                                    cur_h = sum(middleh) / len(middleh)
                                    y_arr.append(cur_t - 0.4 * (cur_t - 10) * (1 - cur_h / 100))
                                    middlet = []
                                    middleh = []

                                    wait_hour = (cur_hour + 1) % 24
                                    wait_min = cur_min

                                    middlet.append(float(unit['data'][t_value]))
                                    middleh.append(float(unit['data'][h_value]))


                        elif self.choice1.get() == 2:  # 3 часа ################################################

                            if flagMid == 0:
                                flagMid = 1
                                wait_hour = (cur_hour + 3) % 24
                                wait_min = cur_hour

                                middlet.append(float(unit['data'][t_value]))
                                middleh.append(float(unit['data'][h_value]))

                            elif flagMid == 1:
                                if cur_hour != wait_hour or (cur_hour == wait_hour and cur_min < wait_min):

                                    middlet.append(float(unit['data'][t_value]))
                                    middleh.append(float(unit['data'][h_value]))

                                else:
                                    x_arr.append(unit['Date'][:-6])
                                    cur_t = sum(middlet) / len(middlet)
                                    cur_h = sum(middleh) / len(middleh)
                                    y_arr.append(cur_t - 0.4 * (cur_t - 10) * (1 - cur_h / 100))
                                    middlet = []
                                    middleh = []

                                    wait_hour = (cur_hour + 3) % 24
                                    wait_min = cur_min

                                    middlet.append(float(unit['data'][t_value]))
                                    middleh.append(float(unit['data'][h_value]))

                        elif self.choice1.get() == 3:  # сутки #################################################
                            if flagMid == 0:
                                flagMid = 1

                                wait_day = cur_day + 1
                                wait_hour = cur_hour

                                middlet.append(float(unit['data'][t_value]))
                                middleh.append(float(unit['data'][h_value]))

                            elif flagMid == 1:
                                if (wait_day - cur_day) == 1 or ((wait_day - cur_day) != 1 and cur_hour < wait_hour):

                                    middlet.append(float(unit['data'][t_value]))
                                    middleh.append(float(unit['data'][h_value]))

                                else:  # прошли сутки
                                    x_arr.append(unit['Date'][:10])
                                    cur_t = sum(middlet) / len(middlet)
                                    cur_h = sum(middleh) / len(middleh)
                                    y_arr.append(cur_t - 0.4 * (cur_t - 10) * (1 - cur_h / 100))
                                    middlet = []
                                    middleh = []

                                    wait_day = cur_day + 1
                                    wait_hour = cur_hour

                                    middlet.append(float(unit['data'][t_value]))
                                    middleh.append(float(unit['data'][h_value]))

                        elif self.choice1.get() == 4:  # мин и макс за сутки
                            if flagMid == 0:
                                flagMid = 1
                                wait_day = cur_day + 1
                                wait_hour = cur_hour

                                middlet.append(float(unit['data'][t_value]))
                                middleh.append(float(unit['data'][h_value]))

                            elif flagMid == 1:
                                if (wait_day - cur_day) == 1 or ((wait_day - cur_day) != 1 and cur_hour < wait_hour):
                                    middlet.append(float(unit['data'][t_value]))
                                    middleh.append(float(unit['data'][h_value]))

                                else:  # прошли сутки
                                    xmin_arr.append(unit['Date'][:10])
                                    xmax_arr.append(unit['Date'][:10])
                                    middlet.sort()
                                    middleh.sort()
                                    cur_tmin = middlet[0]
                                    cur_tmax = middlet[-1]
                                    cur_hmin = middleh[0]
                                    cur_hmax = middleh[-1]
                                    ymin_arr.append(cur_tmin - 0.4 * (cur_tmin - 10) * (1 - cur_hmin / 100))
                                    ymax_arr.append(cur_tmax - 0.4 * (cur_tmax - 10) * (1 - cur_hmax / 100))

                                    middlet = []
                                    middleh = []

                                    wait_day = cur_day + 1
                                    wait_hour = cur_hour

                                    middlet.append(float(unit['data'][t_value]))
                                    middleh.append(float(unit['data'][h_value]))



            if (len(middlet) > 0 or len(middleh) > 0) and (
                    self.choice1.get() == 1 or self.choice1.get() == 2):
                cur_t = sum(middlet) / len(middlet)
                cur_h = sum(middleh) / len(middleh)
                y_arr.append(cur_t - 0.4 * (cur_t - 10) * (1 - cur_h / 100))
                x_arr.append(unit['Date'][:-6])

                middleX = []
                middleY = []
            elif (len(middlet) > 0 or len(middleh) > 0) and self.choice1.get() == 3:
                cur_t = sum(middlet) / len(middlet)
                cur_h = sum(middleh) / len(middleh)
                y_arr.append(cur_t - 0.4 * (cur_t - 10) * (1 - cur_h / 100))
                x_arr.append(unit['Date'][:10])

                middleX = []
                middleY = []

            elif (len(middlet) > 2 or len(middleh) > 2) and self.choice1.get() == 4:
                xmin_arr.append(unit['Date'][:10])
                xmax_arr.append(unit['Date'][:10])

                middlet.sort()
                middleh.sort()
                cur_tmin = middlet[0]
                cur_tmax = middlet[-1]
                cur_hmin = middleh[0]
                cur_hmax = middleh[-1]
                ymin_arr.append(cur_tmin - 0.4 * (cur_tmin - 10) * (1 - cur_hmin / 100))
                ymax_arr.append(cur_tmax - 0.4 * (cur_tmax - 10) * (1 - cur_hmax / 100))

                middlet = []
                middleh = []

            else:
                pass

        if len(xmin_arr) > 0:
            return xmin_arr, ymin_arr, xmax_arr, ymax_arr
        else:
            return x_arr, y_arr

    def select_dopdata(self):
        D1 = int(self.spinboxD1.get())
        D2 = int(self.spinboxD2.get())
        M1 = int(self.spinboxM1.get())
        M2 = int(self.spinboxM2.get())
        H1 = int(self.spinboxH1.get())
        H2 = int(self.spinboxH2.get())
        Min1 = int(self.spinboxMin1.get())
        Min2 = int(self.spinboxMin2.get())

        flag = 0
        flagMid = 0
        wait_day = 0
        wait_hour = 0
        wait_min = 0
        middle = []

        xy = self.cb_datadop.current() + 1  # для csv
        dop_value = self.cb_datadop.get() #для json
        arr = []
        min_arr = []
        max_arr = []

        if file_name[-3:] == "csv":
            global lines
            file = open(file_name, "r", encoding='cp1251')
            f1 = file.readline()
            f2 = file.readline()
            lines = csv.reader(file, delimiter=';')

            for row in lines:
                cur_day = int(row[0][0:row[0].find(' ')].split('-')[2])
                cur_mounth = int(row[0][0:row[0].find(' ')].split('-')[1])
                cur_min = int(row[0][row[0].find(' ') + 1:].split(':')[1])
                cur_hour = int(row[0][row[0].find(' ') + 1:].split(':')[0])
                if (cur_mounth == M1 and cur_day > D1) or (cur_mounth > M1) \
                        or (cur_mounth == M1 and cur_day == D1 and cur_hour > H1) \
                        or (cur_mounth == M1 and cur_day == D1 and cur_hour == H1 and cur_min >= Min1):
                    flag = 1
                if (cur_mounth == M2 and cur_day > D2) or (cur_mounth > M2) \
                        or (cur_mounth == M2 and cur_day == D2 and cur_hour > H2) \
                        or (cur_mounth == M2 and cur_day == D2 and cur_hour == H2 and cur_min >= Min2):
                    flag = 0

                if flag == 1:

                    if self.choice1.get() == 0:  # как есть
                        arr.append(row[xy])

                    elif self.choice1.get() == 1:  # час################################################

                        if flagMid == 0:
                            flagMid = 1
                            wait_hour = (cur_hour + 1) % 24
                            wait_min = cur_hour

                            middle.append(float(row[xy]))

                        elif flagMid == 1:
                            if cur_hour != wait_hour or (cur_hour == wait_hour and cur_min < wait_min):
                                middle.append(float(row[xy]))

                            else:  # прошел час
                                arr.append(sum(middle) / len(middle))
                                middle = []

                                wait_hour = (cur_hour + 1) % 24
                                wait_min = cur_min
                                middle.append(float(row[xy]))



                    elif self.choice1.get() == 2:  # 3 часа ################################################
                        # если не хватило часов можно закинуть как есть
                        if flagMid == 0:
                            flagMid = 1
                            wait_hour = (cur_hour + 3) % 24
                            wait_min = cur_hour
                            middle.append(float(row[xy]))


                        elif flagMid == 1:
                            if cur_hour != wait_hour or (cur_hour == wait_hour and cur_min < wait_min):
                                middle.append(float(row[xy]))

                            else:  # прошло 3 часa
                                arr.append(sum(middle) / len(middle))
                                middle = []

                                wait_hour = (cur_hour + 3) % 24
                                wait_min = cur_min
                                middle.append(float(row[xy]))


                    elif self.choice1.get() == 3:  # сутки #################################################
                        if flagMid == 0:
                            flagMid = 1

                            wait_day = cur_day + 1
                            wait_hour = cur_hour
                            middle.append(float(row[xy]))

                        elif flagMid == 1:
                            if (wait_day - cur_day) == 1 or ((wait_day - cur_day) != 1 and cur_hour < wait_hour):
                                middle.append(float(row[xy]))

                            else:  # прошли сутки
                                arr.append(sum(middle) / len(middle))
                                middle = []

                                wait_day = cur_day + 1
                                wait_hour = cur_hour
                                middle.append(float(row[xy]))

                    elif self.choice1.get() == 4:  # мин и макс за сутки
                        if flagMid == 0:
                            flagMid = 1
                            wait_day = cur_day + 1
                            wait_hour = cur_hour
                            middle.append(float(row[xy]))

                        elif flagMid == 1:
                            if (wait_day - cur_day) == 1 or ((wait_day - cur_day) != 1 and cur_hour < wait_hour):
                                middle.append(float(row[xy]))

                            else:  # прошли сутки
                                middle.sort()
                                min_arr.append(middle[0])
                                max_arr.append(middle[-1])

                                middle = []

                                wait_day = cur_day + 1
                                wait_hour = cur_hour
                                middle.append(float(row[xy]))



            if len(middle) > 0 and self.choice1.get() != 4:
                arr.append(sum(middle) / len(middle))
                middle = []

            elif len(middle) > 2 and self.choice1.get() == 4:
                middle.sort()
                min_arr.append(middle[0])  # добавили мин
                max_arr.append(middle[-1])  # добавили макс
                middle = []
            else:
                pass

        else: #json
            for unit in lines:
                if unit['uName'] + ' ' + '(' + unit['serial'] + ')' == self.cb_device.get() :
                    cur_day = int(unit['Date'][0:unit['Date'].find(' ')].split('-')[2])
                    cur_mounth = int(unit['Date'][0:unit['Date'].find(' ')].split('-')[1])
                    cur_min = int(unit['Date'][unit['Date'].find(' ') + 1:].split(':')[1])
                    cur_hour = int(unit['Date'][unit['Date'].find(' ') + 1:].split(':')[0])
                    if (cur_mounth == M1 and cur_day > D1) or (cur_mounth > M1) \
                            or (cur_mounth == M1 and cur_day == D1 and cur_hour > H1) \
                            or (cur_mounth == M1 and cur_day == D1 and cur_hour == H1 and cur_min >= Min1):
                        flag = 1
                    if (cur_mounth == M2 and cur_day > D2) or (cur_mounth > M2) \
                            or (cur_mounth == M2 and cur_day == D2 and cur_hour > H2) \
                            or (cur_mounth == M2 and cur_day == D2 and cur_hour == H2 and cur_min >= Min2):
                        flag = 0

                    if flag == 1:

                        if self.choice1.get() == 0:  # как есть
                            arr.append(float(unit['data'][dop_value]))

                        elif self.choice1.get() == 1:  # час################################################
                            if flagMid == 0:
                                flagMid = 1
                                wait_hour = (cur_hour + 1) % 24
                                wait_min = cur_hour
                                middle.append(float(unit['data'][dop_value]))


                            elif flagMid == 1:
                                if cur_hour != wait_hour or (cur_hour == wait_hour and cur_min < wait_min):
                                    middle.append(float(unit['data'][dop_value]))

                                else:  # прошел час
                                    arr.append(sum(middle) / len(middle))
                                    middle = []

                                    wait_hour = (cur_hour + 1) % 24
                                    wait_min = cur_min
                                    middle.append(float(unit['data'][dop_value]))

                        elif self.choice1.get() == 2:  # 3 часа ################################################
                            # если не хватило часов можно закинуть как есть
                            if flagMid == 0:
                                flagMid = 1
                                wait_hour = (cur_hour + 3) % 24
                                wait_min = cur_hour
                                middle.append(float(unit['data'][dop_value]))

                            elif flagMid == 1:
                                if cur_hour != wait_hour or (cur_hour == wait_hour and cur_min < wait_min):
                                    middle.append(float(unit['data'][dop_value]))

                                else:  # прошло 3 часа
                                    arr.append(sum(middle) / len(middle))
                                    middle = []

                                    wait_hour = (cur_hour + 3) % 24
                                    wait_min = cur_min
                                    middle.append(float(unit['data'][dop_value]))

                        elif self.choice1.get() == 3:  # сутки #################################################
                            if flagMid == 0:
                                flagMid = 1

                                wait_day = cur_day + 1
                                wait_hour = cur_hour
                                middle.append(float(unit['data'][dop_value]))

                            elif flagMid == 1:
                                if (wait_day - cur_day) == 1 or ((wait_day - cur_day) != 1 and cur_hour < wait_hour):
                                    middle.append(float(unit['data'][dop_value]))

                                else:  # прошли сутки
                                    arr.append(sum(middle) / len(middle))
                                    middle = []

                                    wait_day = cur_day + 1
                                    wait_hour = cur_hour
                                    middle.append(float(unit['data'][dop_value]))

                        elif self.choice1.get() == 4:  # мин и макс за сутки
                            if flagMid == 0:
                                flagMid = 1
                                wait_day = cur_day + 1
                                wait_hour = cur_hour
                                middle.append(float(unit['data'][dop_value]))

                            elif flagMid == 1:
                                if (wait_day - cur_day) == 1 or ((wait_day - cur_day) != 1 and cur_hour < wait_hour):
                                    middle.append(float(unit['data'][dop_value]))

                                else:  # прошли сутки

                                    middle.sort()
                                    min_arr.append(middle[0])  # добавили мин
                                    max_arr.append(middle[-1])  # добавили макс

                                    middle = []

                                    wait_day = cur_day + 1
                                    wait_hour = cur_hour
                                    middle.append(float(unit['data'][dop_value]))

            if len(middle) > 0 and self.choice1.get() != 4:
                arr.append(sum(middle) / len(middle))
                middle = []

            elif len(middle) > 2 and self.choice1.get() == 4:
                middle.sort()
                min_arr.append(middle[0])  # добавили мин
                max_arr.append(middle[-1])  # добавили макс
                middle = []
            else:
                pass


        if len(min_arr) > 0:
            return min_arr, max_arr
        else:
            return arr

    def get_html_page(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        }
        try:
            r = requests.get(url, headers=headers)
        except requests.exceptions.RequestException:
            html = None
        else:
            if r.ok:
                html = r.text
        return html

    def select_gismeteo(self):
        D1 = int(self.spinboxD1.get())
        D2 = int(self.spinboxD2.get())
        M1 = int(self.spinboxM1.get())
        M2 = int(self.spinboxM2.get())
        H2 = int(self.spinboxH2.get())
        Min2 = int(self.spinboxMin2.get())
        arr = []
        arr_dop = []
        html2 = None
        if M1 == 4:
            html1 = self.get_html_page(URL1)
            if M2 == 5:
                html2 = self.get_html_page(URL2)
        else:
            html1 = self.get_html_page(URL2)
        if html2 == None:
            soup1 = BeautifulSoup(html1, features="html.parser")
            table1 = soup1.find('table')
            data1 = table1.find('tbody').findAll('tr')
        else:
            soup1 = BeautifulSoup(html1, features="html.parser")
            table1 = soup1.find('table')
            data1 = table1.find('tbody').findAll('tr')
            soup2 = BeautifulSoup(html2, features="html.parser")
            table2 = soup2.find('table')
            data2 = table2.find('tbody').findAll('tr')
        flag = 0
        if html2 == None:
            for row in data1:#апрель или май
                day = row.findAll('td')
                cur_day = int(day[0].text)
                if D1 <= cur_day < D2:
                    flag = 1
                elif cur_day == D2 and (H2 > 0 or Min2 >0):
                    flag = 1
                else:
                    flag = 0

                if flag == 1:
                    if self.cb_datagis.current() == 0: #temp
                        arr.append((int(day[1].text) + int(day[6].text)) / 2)
                    elif self.cb_datagis.current() == 1: #pressure
                        arr.append((int(day[2].text) + int(day[7].text)) / 2)
                    elif self.cb_datagis.current() == 2: # 2 in 1
                        arr.append((int(day[1].text) + int(day[6].text)) / 2)
                        arr_dop.append((int(day[2].text) + int(day[7].text)) / 2)
                    else:
                        pass
        else:
            for row in data1:#апрель
                day = row.findAll('td')
                cur_day = int(day[0].text)
                if D1 <= cur_day <= 30:
                    flag = 1
                else:
                    flag = 0

                if flag == 1:
                    if self.cb_datagis.current() == 0: #temp
                        arr.append((int(day[1].text) + int(day[6].text)) / 2)
                    elif self.cb_datagis.current() == 1: #pressure
                        arr.append((int(day[2].text) + int(day[7].text)) / 2)
                    elif self.cb_datagis.current() == 2: # 2 in 1
                        arr.append((int(day[1].text) + int(day[6].text)) / 2)
                        arr_dop.append((int(day[2].text) + int(day[7].text)) / 2)
                    else:
                        pass

            for row in data2:#май
                day = row.findAll('td')
                cur_day = int(day[0].text)
                if cur_day < D2:
                    flag = 1
                elif cur_day == D2 and (H2 > 0 or Min2 >0):
                    flag = 1
                else:
                    flag = 0

                if flag == 1:
                    if self.cb_datagis.current() == 0:  # temp
                        arr.append((int(day[1].text) + int(day[6].text)) / 2)
                    elif self.cb_datagis.current() == 1:  # pressure
                        arr.append((int(day[2].text) + int(day[7].text)) / 2)
                    elif self.cb_datagis.current() == 2:  # 2 in 1
                        arr.append((int(day[1].text) + int(day[6].text)) / 2)
                        arr_dop.append((int(day[2].text) + int(day[7].text)) / 2)
                    else:
                        pass

        if len(arr_dop) > 0:
            return arr, arr_dop
        else:
            return arr


    def build_graph(self):
        if self.check_param() == -1:
            return
        plt.figure(figsize=(15.5, 7))
        if self.choice2.get() == 0:#линейный
            if self.choice1.get() != 4:
                arr_x, arr_y = self.select_data()

                if self.choice3.get() == True: #добавляем еще данные
                    plt.plot(arr_x, arr_y, color='navy', label=f'f({self.cb_dataX.get()}, {self.cb_dataY.get()})')
                    if self.cb_xory.current() == 0:
                        plt.plot(self.select_dopdata(), arr_y, color='k', label=f'f({self.cb_datadop.get()}, {self.cb_dataY.get()})')
                    else:
                        plt.plot(arr_x, self.select_dopdata(), color='k', label=f'f({self.cb_dataX.get()}, {self.cb_datadop.get()})')
                    plt.legend()
                else:
                    plt.plot(arr_x, arr_y, color='navy', label='Данные с прибора')

                if self.choice1.get() == 3 and self.choice4.get() == True: #добавляем с гисметео
                    if self.cb_datagis.current() != 2: #берем 1 значение
                        arr_gis = self.select_gismeteo()
                        if len(arr_gis) != len(arr_x): #если приборы вуза не работали с 29 по 3
                            r = len(arr_gis) - len(arr_x) #сколько элем удалить с 29
                            for i in range(r):
                                if self.cb_dataX.current() == 0:
                                    arr_gis.pop(arr_x.index('2022-04-28')+1)
                                else:
                                    arr_gis.pop(arr_y.index('2022-04-28')+1)

                        if self.cb_gisxy.current() == 0:
                            plt.plot(arr_gis, arr_y, color='cadetblue', label=f'Данные {self.cb_datagis.get()} с гисметео')
                        else:
                            plt.plot(arr_x, arr_gis, color='cadetblue', label=f'Данные {self.cb_datagis.get()} с гисметео')
                    else: #берем 2 значения
                        arr_temp, arr_press = self.select_gismeteo()
                        if len(arr_temp) != len(arr_x):  # если приборы вуза не работали с 29 по 3
                            r = len(arr_temp) - len(arr_x)  # сколько элем удалить с 29
                            for i in range(r):
                                if self.cb_dataX.current() == 0:
                                    arr_temp.pop(arr_x.index('2022-04-28') + 1)
                                    arr_press.pop(arr_x.index('2022-04-28') + 1)
                                else:
                                    arr_temp.pop(arr_y.index('2022-04-28') + 1)
                                    arr_press.pop(arr_y.index('2022-04-28') + 1)

                        if self.cb_gisxy.current() == 0:
                            plt.plot(arr_temp, arr_y, color='cadetblue', label=f'Данные temp с гисметео')
                            plt.plot(arr_press, arr_y, color='tan', label=f'Данные pressure с гисметео')
                        else:
                            plt.plot(arr_x, arr_temp, color='cadetblue', label=f'Данные temp с гисметео')
                            plt.plot(arr_x, arr_press, color='tan', label=f'Данные pressure с гисметео')
                    plt.legend()



            else: #мин и макс значения
                arr_xmin, arr_ymin, arr_xmax, arr_ymax = self.select_data()

                if self.choice3.get() == True: #добавляем еще данные
                    plt.plot(arr_xmax, arr_ymax, label=f'Максимальные значения f({self.cb_dataX.get()}, {self.cb_dataY.get()})', color='navy')
                    plt.plot(arr_xmin, arr_ymin, label=f'Минимальные значения f({self.cb_dataX.get()}, {self.cb_dataY.get()})', color='fuchsia')
                    dop_min, dop_max = self.select_dopdata()
                    if self.cb_xory.current() == 0:
                        plt.plot(dop_max, arr_ymax, color='k', label=f'Максимальные значения f({self.cb_datadop.get()}, {self.cb_dataY.get()})')
                        plt.plot(dop_min, arr_ymin, color='brown', label=f'Минимальные значения f({self.cb_datadop.get()}, {self.cb_dataY.get()})')
                    else:
                        plt.plot(arr_xmax, dop_max, color='k', label=f'Максимальные значения f({self.cb_dataX.get()}, {self.cb_datadop.get()})')
                        plt.plot(arr_xmin, dop_min, color='brown', label=f'Минимальные значения f({self.cb_dataX.get()}, {self.cb_datadop.get()})')
                else:
                    plt.plot(arr_xmax, arr_ymax, label=f'Максимальные значения', color='navy')
                    plt.plot(arr_xmin, arr_ymin, label=f'Минимальные значения', color='fuchsia')
                plt.legend()

        elif self.choice2.get() == 1: #столбчатый
            if self.choice1.get() != 4:
                arr_x, arr_y = self.select_data()

                if self.choice3.get() == True: #добавляем еще данные
                    plt.bar(arr_x, arr_y, edgecolor='navy', label=f'f({self.cb_dataX.get()}, {self.cb_dataY.get()})', color=[0.1, 0.1, 0.1, 0], linestyle='dotted')
                    if self.cb_xory.current() == 0:
                        plt.bar(self.select_dopdata(), edgecolor='k', label=f'f({self.cb_datadop.get()}, {self.cb_dataY.get()})', color=[0.1, 0.1, 0.1, 0], linestyle='--')
                    else:
                        plt.bar(arr_x, self.select_dopdata(), edgecolor='k', label=f'f({self.cb_dataX.get()}, {self.cb_datadop.get()})', color=[0.1, 0.1, 0.1, 0], linestyle='--')
                    plt.legend()
                else:
                    plt.bar(arr_x, arr_y, edgecolor='navy', label='Данные с прибора', color=[0.1, 0.1, 0.1, 0], linestyle='dotted')

                if self.choice1.get() == 3 and self.choice4.get() == True: #добавляем с гисметео
                    if self.cb_datagis.current() != 2:
                        arr_gis = self.select_gismeteo()
                        if len(arr_gis) != len(arr_x): #если приборы вуза не работали с 29 по 3
                            r = len(arr_gis) - len(arr_x) #сколько элем удалить с 29
                            for i in range(r):
                                if self.cb_dataX.current() == 0:
                                    arr_gis.pop(arr_x.index('2022-04-28')+1)
                                else:
                                    arr_gis.pop(arr_y.index('2022-04-28')+1)

                        if self.cb_gisxy.current() == 0:
                            plt.bar(arr_gis, arr_y, edgecolor='cadetblue', label=f'Данные {self.cb_datagis.get()} с гисметео', color=[0.1, 0.1, 0.1, 0], linestyle='-.')
                        else:
                            plt.bar(arr_x, arr_gis, edgecolor='cadetblue', label=f'Данные {self.cb_datagis.get()} с гисметео', color=[0.1, 0.1, 0.1, 0], linestyle='-.')
                    else: #берем 2 значения
                        arr_temp, arr_press = self.select_gismeteo()
                        if len(arr_temp) != len(arr_x):  # если приборы вуза не работали с 29 по 3
                            r = len(arr_temp) - len(arr_x)  # сколько элем удалить с 29
                            for i in range(r):
                                if self.cb_dataX.current() == 0:
                                    arr_temp.pop(arr_x.index('2022-04-28') + 1)
                                    arr_press.pop(arr_x.index('2022-04-28') + 1)
                                else:
                                    arr_temp.pop(arr_y.index('2022-04-28') + 1)
                                    arr_press.pop(arr_y.index('2022-04-28') + 1)

                        if self.cb_gisxy.current() == 0:
                            plt.bar(arr_temp, arr_y, edgecolor='cadetblue', label=f'Данные temp с гисметео', color=[0.1, 0.1, 0.1, 0], linestyle='-.')
                            plt.bar(arr_press, arr_y, edgecolor='tan', label=f'Данные pressure с гисметео', color=[0.1, 0.1, 0.1, 0], linestyle='-.')
                        else:
                            plt.bar(arr_x, arr_temp, edgecolor='cadetblue', label=f'Данные temp с гисметео', color=[0.1, 0.1, 0.1, 0], linestyle='-.')
                            plt.bar(arr_x, arr_press, edgecolor='tan', label=f'Данные pressure с гисметео', color=[0.1, 0.1, 0.1, 0], linestyle='-.')
                    plt.legend()

            else: #мин и макс значения
                arr_xmin, arr_ymin, arr_xmax, arr_ymax = self.select_data()
                if self.choice3.get() == True: #добавляем еще данные
                    dop_min, dop_max = self.select_dopdata()

                    plt.bar(arr_xmax, arr_ymax, label=f'Максимальные значения f({self.cb_dataX.get()}, {self.cb_dataY.get()})', edgecolor='navy', color=[0.1, 0.1, 0.1, 0], linestyle='dotted')
                    plt.bar(arr_xmin, arr_ymin, label=f'Минимальные значения f({self.cb_dataX.get()}, {self.cb_dataY.get()})', edgecolor='fuchsia', color=[0.1, 0.1, 0.1, 0], linestyle='dotted')

                    if self.cb_xory.current() == 0:
                        plt.bar(dop_max, arr_ymax, edgecolor='k', label=f'Максимальные значения f({self.cb_datadop.get()}, {self.cb_dataY.get()})', color=[0.1, 0.1, 0.1, 0], linestyle='--')
                        plt.bar(dop_min, arr_ymin, edgecolor='brown', label=f'Минимальные значения f({self.cb_datadop.get()}, {self.cb_dataY.get()})', color=[0.1, 0.1, 0.1, 0], linestyle='--')
                    else:
                        plt.bar(arr_xmax, dop_max, edgecolor='k', label=f'Максимальные значения f({self.cb_dataX.get()}, {self.cb_datadop.get()})', color=[0.1, 0.1, 0.1, 0], linestyle='--')
                        plt.bar(arr_xmin, dop_min, edgecolor='brown', label=f'Минимальные значения f({self.cb_dataX.get()}, {self.cb_datadop.get()})', color=[0.1, 0.1, 0.1, 0], linestyle='--')

                else:
                    plt.bar(arr_xmax, arr_ymax, label=f'Максимальные значения', color='navy')
                    plt.bar(arr_xmin, arr_ymin, label=f'Минимальные значения', color='fuchsia')
                plt.legend()

        else: #точечный
            if self.choice1.get() != 4:
                arr_x, arr_y = self.select_data()

                if self.choice3.get() == True: #добавляем еще данные
                    plt.scatter(arr_x, arr_y, color='navy', label=f'f({self.cb_dataX.get()}, {self.cb_dataY.get()})')
                    if self.cb_xory.current() == 0:
                        plt.scatter(self.select_dopdata(), arr_y, color='k',label=f'f({self.cb_datadop.get()}, {self.cb_dataY.get()})')
                    else:
                        plt.scatter(arr_x, self.select_dopdata(), color='k',label=f'f({self.cb_dataX.get()}, {self.cb_datadop.get()})')
                    plt.legend()
                else:
                    plt.scatter(arr_x, arr_y, color='navy', label='Данные с прибора')

                if self.choice1.get() == 3 and self.choice4.get() == True:  # добавляем с гисметео
                    if self.cb_datagis.current() != 2:
                        arr_gis = self.select_gismeteo()
                        if len(arr_gis) != len(arr_x):  # если приборы вуза не работали с 29 по 3
                            r = len(arr_gis) - len(arr_x)  # сколько элем удалить с 29
                            for i in range(r):
                                if self.cb_dataX.current() == 0:
                                    arr_gis.pop(arr_x.index('2022-04-28') + 1)
                                else:
                                    arr_gis.pop(arr_y.index('2022-04-28') + 1)

                        if self.cb_gisxy.current() == 0:
                            plt.scatter(arr_gis, arr_y, color='cadetblue', label=f'Данные {self.cb_datagis.get()} с гисметео')
                        else:
                            plt.scatter(arr_x, arr_gis, color='cadetblue', label=f'Данные {self.cb_datagis.get()} с гисметео')
                    else: #берем 2 значения
                        arr_temp, arr_press = self.select_gismeteo()
                        if len(arr_temp) != len(arr_x):  # если приборы вуза не работали с 29 по 3
                            r = len(arr_temp) - len(arr_x)  # сколько элем удалить с 29
                            for i in range(r):
                                if self.cb_dataX.current() == 0:
                                    arr_temp.pop(arr_x.index('2022-04-28') + 1)
                                    arr_press.pop(arr_x.index('2022-04-28') + 1)
                                else:
                                    arr_temp.pop(arr_y.index('2022-04-28') + 1)
                                    arr_press.pop(arr_y.index('2022-04-28') + 1)

                        if self.cb_gisxy.current() == 0:
                            plt.scatter(arr_temp, arr_y, color='cadetblue', label=f'Данные temp с гисметео')
                            plt.scatter(arr_press, arr_y, color='tan', label=f'Данные pressure с гисметео')
                        else:
                            plt.scatter(arr_x, arr_temp, color='cadetblue', label=f'Данные temp с гисметео')
                            plt.scatter(arr_x, arr_press, color='tan', label=f'Данные pressure с гисметео')
                    plt.legend()


            else: # мин и макс значения
                arr_xmin, arr_ymin, arr_xmax, arr_ymax = self.select_data()

                if self.choice3.get() == True: #добавляем еще данные
                    plt.scatter(arr_xmax, arr_ymax,label=f'Максимальные значения f({self.cb_dataX.get()}, {self.cb_dataY.get()})',color='navy')
                    plt.scatter(arr_xmin, arr_ymin,label=f'Минимальные значения f({self.cb_dataX.get()}, {self.cb_dataY.get()})',color='fuchsia')
                    dop_min, dop_max = self.select_dopdata()
                    if self.cb_xory.current() == 0:
                        plt.scatter(dop_max, arr_ymax, color='k',label=f'Максимальные значения f({self.cb_datadop.get()}, {self.cb_dataY.get()})')
                        plt.scatter(dop_min, arr_ymin, color='brown',label=f'Минимальные значения f({self.cb_datadop.get()}, {self.cb_dataY.get()})')
                    else:
                        plt.scatter(arr_xmax, dop_max, color='k',label=f'Максимальные значения f({self.cb_dataX.get()}, {self.cb_datadop.get()})')
                        plt.scatter(arr_xmin, dop_min, color='brown',label=f'Минимальные значения f({self.cb_dataX.get()}, {self.cb_datadop.get()})')
                else:
                    plt.scatter(arr_xmax, arr_ymax, label=f'Максимальные значения', color='navy')
                    plt.scatter(arr_xmin, arr_ymin, label=f'Минимальные значения', color='fuchsia')
                plt.legend()




        if self.choice1.get() > 2:
            plt.grid(True)
        if self.choice3.get() == True and self.cb_xory.current() == 0:
            plt.xlabel(f'{self.cb_dataX.get()} / {self.cb_datadop.get()}')
            plt.ylabel(self.cb_dataY.get())
        elif self.choice3.get() == True and self.cb_xory.current() == 1:
            plt.xlabel(self.cb_dataX.get())
            plt.ylabel(f'{self.cb_dataY.get()} / {self.cb_datadop.get()}')
        else:
            plt.xlabel(self.cb_dataX.get())
            plt.ylabel(self.cb_dataY.get())
        if self.cb_dataX.current() == 0:
            plt.xticks(rotation=90, fontsize=6)

        plt.title(f'График данных с прибора {self.cb_device.get()}')

        plt.get_current_fig_manager().window.wm_geometry('+0+0')
        plt.show()
        if file_name[-3:] == "csv":
            self.open_file(1)

    def decorate(self, start, finish, xcolor):

        for item in range(start, finish):
            if item >= 30:
                plt.fill_between(xcolor, 30, finish, color='red')
                plt.text(0, 30, 'Очень жарко')
            elif 24 <= item < 30:
                plt.fill_between(xcolor, 24, 30, color='orangered')
                plt.text(0, 24, 'Жарко')
            elif 18 <= item < 24:
                plt.fill_between(xcolor, 18, 24, color='orange')
                plt.text(0, 18, 'Тепло')
            elif 12 <= item < 18:
                plt.fill_between(xcolor, 12, 18, color='yellow')
                plt.text(0, 12, 'Умеренно тепло')
            elif 6 <= item < 12:
                plt.fill_between(xcolor, 6, 12, color='springgreen')
                plt.text(0, 6, 'Прохладно')
            elif 0 <= item < 6:
                plt.fill_between(xcolor, 0, 6, color='aquamarine')
                plt.text(0, 0, 'Умеренно')
            elif -12 <= item < 0:
                plt.fill_between(xcolor, -12, 0, color='mediumturquoise')
                plt.text(0, -12, 'Холодно')
            elif -24 <= item < -12:
                plt.fill_between(xcolor, -24, -12, color='lightblue')
                plt.text(0, -24, 'Очень холодно')
            elif -30 < item < -24:
                plt.fill_between(xcolor, -30, -24, color='deepskyblue')
                plt.text(0, -30, 'Крайне холодно')
            elif item <= -30:
                plt.fill_between(xcolor, start, -30, color='dodgerblue')
                plt.text(0, -33, 'Вечная мерзлота')

    def buildET_graph(self):
        if self.cb_ET1.current() == -1 or self.cb_ET2.current() == -1 or self.cb_ET1.current() == self.cb_ET2.current():
            showinfo(title="Внимание!", message="Выберите данные для t и h")
            return
        if self.cb_dataX.current() == 0 or self.cb_dataY.current() == 0:
            showinfo(title="Внимание!", message="t или h не могут быть датой")
            return
        if self.choice3.get() == True:
            showinfo(title="Внимание!", message="t и h уже выбраны, другие данные не нужны, уберите галочку")
            return
        if self.choice4.get() == True:
            showinfo(title="Внимание!", message="Gismeteo не предоставляет данные о влажности, уберите галочку")
            return
        if self.check_param() == -1:
            return

        if self.choice2.get() == 0: #линейный
            if self.choice1.get() != 4:
                arr_x, arr_y = self.selectET_data()
                start = math.floor(sorted(arr_y)[0])
                finish = math.ceil(sorted(arr_y)[-1])
                self.decorate(start, finish, arr_x)
                plt.plot(arr_x, arr_y, color='navy')
            else:
                arr_xmin, arr_ymin, arr_xmax, arr_ymax = self.selectET_data()
                start = math.floor(sorted(arr_ymin)[0])
                finish = math.ceil(sorted(arr_ymax)[-1])
                self.decorate(start, finish, arr_xmin)
                plt.plot(arr_xmax, arr_ymax, label='Максимальные значения', color='navy')
                plt.plot(arr_xmin, arr_ymin, label='Минимальные значения', color='fuchsia')
                plt.legend()


        elif self.choice2.get() == 1: #столбчатый
            if self.choice1.get() != 4:
                arr_x, arr_y = self.selectET_data()
                start = math.floor(sorted(arr_y)[0])
                finish = math.ceil(sorted(arr_y)[-1])
                if start > 0:
                    start = 0
                self.decorate(start, finish, arr_x)
                plt.bar(arr_x, arr_y, color = [0.1, 0.1, 0.1, 0], linestyle = '--', edgecolor = 'navy')
            else:
                arr_xmin, arr_ymin, arr_xmax, arr_ymax = self.selectET_data()
                start = math.floor(sorted(arr_ymin)[0])
                finish = math.ceil(sorted(arr_ymax)[-1])
                if start > 0:
                    start = 0
                self.decorate(start, finish, arr_xmin)
                plt.bar(arr_xmin, arr_ymin, label='Минимальные значения', color=[0.1, 0.1, 0.1, 0], linestyle='--', edgecolor='navy')
                plt.bar(arr_xmax, arr_ymax, label='Максимальные значения', color = [0.1, 0.1, 0.1, 0], linestyle = '--', edgecolor = 'fuchsia')
                plt.legend()

        else: #точечный
            if self.choice1.get() != 4:
                arr_x, arr_y = self.selectET_data()
                start = math.floor(sorted(arr_y)[0])
                finish = math.ceil(sorted(arr_y)[-1])
                self.decorate(start, finish, arr_x)
                plt.scatter(arr_x, arr_y, color='navy')
            else:
                arr_xmin, arr_ymin, arr_xmax, arr_ymax = self.selectET_data()
                start = math.floor(sorted(arr_ymin)[0])
                finish = math.ceil(sorted(arr_ymax)[-1])
                self.decorate(start, finish, arr_xmin)
                plt.scatter(arr_xmin, arr_ymin, label='Минимальные значения', color='navy')
                plt.scatter(arr_xmax, arr_ymax, label='Максимальные значения', color='fuchsia')
                plt.legend()

        plt.xlabel('Date')
        plt.xticks(rotation=90)
        plt.ylabel(self.cb_dataY.get())
        plt.title('График')
        plt.show()


#делаем чекбокс добавить кривую

if __name__ == '__main__':
    window = MainWindow()
    window.run()







