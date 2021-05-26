import sqlite3
from tkinter import *
import tkinter as tk
import requests

root = Tk()
root.geometry("400x400")
root.configure(bg='cadetblue1')
root.resizable(False, False)
a = ("Comic Sans MS", 15, "bold")
b = ("Comic Sans MS", 20, "bold")


class FirstPage(tk.Frame):

    def __init__(self, master, word=None):
        super().__init__(master, word=None)
        self.word = word
        self.create_widgets()
        self.show_widgets()

    def show_widgets(self):
        self.Show_btn.grid(row=0, column=1, sticky='w', pady=5)
        self.Search_btn.grid(row=1, column=1, pady=5, padx=5, ipady=10, sticky='nw')
        self.loc_entry.grid(row=1, column=0, padx=5, pady=5, ipady=20, sticky='nw')
        self.label1.grid(row=2, column=0, sticky='ns', pady=0)
        self.label2.grid(row=3, column=0, sticky='ns', pady=0)

        if self.word != None:
            self.loc_entry.delete(0, "end")
            self.loc_entry.insert(0, self.word)

    def create_widgets(self):
        self.Show_btn = Button(root, text="History", font=a, command=self.PressedHistory)
        self.Search_btn = Button(root, text="Search", font=a, command=self.add)
        self.loc_entry = Entry(root, bg="white", font=a, justify='center', text="PASS", width=25)
        self.label1 = tk.Label(root, bg='cadetblue1', font=b)
        self.label2 = tk.Label(root, bg='cadetblue1', font=a)

    def add(self):
        self.location = self.loc_entry.get()
        api = "https://api.openweathermap.org/data/2.5/weather?q=" + self.location + "&appid=06c921750b9a82d8f5d1294e1586276f"

        # weather information;
        json_data = requests.get(api).json()
        self.condition = json_data['weather'][0]['main']
        self.temp = int(json_data['main']['temp'] - 273.15)
        self.min_temp = int(json_data['main']['temp_min'] - 273.15)
        self.max_temp = int(json_data['main']['temp_max'] - 273.15)
        self.pressure = json_data['main']['pressure']
        self.humidity = json_data['main']['humidity']
        self.wind = json_data['wind']['speed']

        # reconnect into database;
        conn = sqlite3.connect('HistoryDB.db')
        cursor = conn.cursor()

        # insert into database;
        cursor.execute("INSERT INTO search_history VALUES (:location)", {'location': self.loc_entry.get()})

        # clear entry box
        self.loc_entry.delete(0, END)

        # weather info to string
        first_result = self.condition + "\n" + str(self.temp) + "°C"
        second_results = "\n" + "Min Temp: " + str(self.min_temp) + "°C" + "\n" + "Max Temp: " + str(
            self.max_temp) + "°C" + "\n" + "Pressure: " + str(self.pressure) + "\n" + "Humidity: " + str(
            self.humidity) + "\n" + \
                         "Wind Speed: " + str(self.wind)

        # showing weather information on tkinter;
        self.label1.config(text=first_result, font=b)
        self.label2.config(text=second_results, font=a)

        conn.commit()
        conn.close()

    def PressedHistory(self):
        self.loc_entry.destroy()
        self.Search_btn.destroy()
        self.Show_btn.destroy()
        self.label1.destroy()
        self.label2.destroy()
        SecondPage(root)


FirstPage(root)


class SecondPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.create_widgets()
        self.show_widgets()

    def create_widgets(self):
        conn = sqlite3.connect('HistoryDB.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM search_history")
        searches = cursor.fetchall()
        search_list = []
        for search in searches:
            search_list.append(str(search[0]))

        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        self.list_var = tk.StringVar(value=search_list)
        self.List_box = tk.Listbox(root, listvariable=self.list_var, selectmode='extended')
        self.scrollbar = Scrollbar(root, orient='vertical', command=self.List_box.yview)
        self.clear_btn = Button(root, text='Clear History', command=self.clear, font=('Comic Sans MS', 12, "bold"))
        self.return_btn = Button(root, text='<', command=self.back, font=("Comic Sans MS", 12, "bold"))

        # close connection
        conn.commit()
        conn.close()

    def show_widgets(self):
        self.List_box.grid(row=1, column=0, sticky='nwes')
        self.scrollbar.grid(row=1, column=1, sticky='ns')
        self.clear_btn.grid(row=0, column=1, sticky='w', ipady=10)
        self.return_btn.grid(row=0, column=0, ipady=10, sticky='w')
        self.List_box.bind('<<ListboxSelect>>', self.onclick)

    def clear(self):
        # reconnect into database
        conn = sqlite3.connect('HistoryDB.db')
        cursor = conn.cursor()

        cursor.execute("DELETE FROM search_history")  # clear database

        self.List_box.delete(0, END)  # clear listbox

        # close connection
        conn.commit()
        conn.close()

    def back(self):
        self.List_box.destroy()
        self.scrollbar.destroy()
        self.clear_btn.destroy()
        self.return_btn.destroy()
        FirstPage(root)

    def onclick(self, event):
        self.selected_indices = self.List_box.curselection()  # get selected indices
        self.selected_word = ",".join([self.List_box.get(i) for i in self.selected_indices])  # get selected items
        self.List_box.destroy()
        self.scrollbar.destroy()
        self.clear_btn.destroy()
        self.return_btn.destroy()
        FirstPage(root, self.selected_word)


root.mainloop()
