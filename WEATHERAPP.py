import sqlite3
from tkinter import *
import tkinter as tk
import requests


'''Basic Tkinter Setup'''
root = Tk()
a = ("Comic Sans MS", 15, "bold")
b = ("Comic Sans MS", 20, "bold")
root.geometry("430x430")
root.configure(bg='#0099FF')
root.resizable(False, False)


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
        self.label1 = tk.Label(root, bg='#0099FF', font=b)
        self.label2 = tk.Label(root, bg='#0099FF', font=a)
        self.loc_entry = Entry(root, bg="#00CCFF", font=a, justify='center', text="PASS", width=25)
        self.Show_btn = Button(root, text="History", font=a, command=self.PressedHistory, bg='#00CCFF')
        self.Search_btn = Button(root, text="Search", font=a, command=self.Get_Weather_Info, bg='#00CCFF')

    def Add_Search_to_database(self, location):
        # CONNECT TO DATABASE;
        conn = sqlite3.connect('HistoryDB.db')
        cursor = conn.cursor()

        # SAVE LOCATION TO search_history TABLE;
        cursor.execute("INSERT INTO search_history VALUES (:location)", {'location': location})

        # CLEAR SEARCH BOX TO ENTER A NEW SEARCH;
        self.loc_entry.delete(0, END)

        # CLOSE CONNECTION;
        conn.commit()
        conn.close()

    def Get_Weather_Info(self, city=None):
        if city is not None:
            location = city
        else:
            location = self.loc_entry.get()
        try:
            self.api = "https://api.openweathermap.org/data/2.5/weather?q=" + location + "&appid=06c921750b9a82d8f5d1294e1586276f"

            # RESULT IS RETURNED IN JSON FORMAT;
            json_data = requests.get(self.api).json()

            # COLLECTING THE NECESSARY INFO I NEED FROM THE RESULT;
            self.condition = json_data['weather'][0]['main']
            self.temp = int(json_data['main']['temp'] - 273.15)
            self.min_temp = int(json_data['main']['temp_min'] - 273.15)
            self.max_temp = int(json_data['main']['temp_max'] - 273.15)
            self.pressure = json_data['main']['pressure']
            self.humidity = json_data['main']['humidity']
            self.wind = json_data['wind']['speed']

            # FORMAT TO STRING....MAKING IT LOOK NEAT
            self.first_result = self.condition + "\n" + str(self.temp) + "°C"

            self.second_results = "\n" + "Min Temp: " + str(self.min_temp) + "°C" + "\n" + "Max Temp: " + str(

                self.max_temp) + "°C" + "\n" + "Pressure: " + str(self.pressure) + "\n" + "Humidity: " + str(
                self.humidity) + "\n" + "Wind Speed: " + str(self.wind)

            # RESULTS SHOULD BE RETURNED ON TKINTER SCREEN AS LABELS;
            self.label1.config(text=self.first_result, font=b)
            self.label2.config(text=self.second_results, font=a)

            # EACH SUCCESSFUL SEARCH IS SAVED TO DATABASE;
            self.Add_Search_to_database(location)

        # BUT IF SEARCH WAS UNSUCCESSFUL,
        except (AttributeError, KeyError):
            # CLEAR SEARCH BOX FOR NEW SEARCH;
            self.loc_entry.delete(0, END)

            # LET USER KNOW THEIR SEARCH WAS WRONG
            self.label1.config(text="Location does not exist :/", font=a)
            self.label2.config(text=" ")

            return "Location does not exist"

        return self.first_result + "\n" + self.second_results

    def PressedHistory(self):
        # FUNCTION IS CALLED WHEN USER CLICKS THE HISTORY BUTTON,
        # ALL WIDGETS ARE DESTROYED AND THEY ARE TAKEN TO A NEW PAGE;
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
        self.Show_widgets()

    def create_widgets(self):
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)

        self.search_list = self.History_Table()
        self.list_var = tk.StringVar(value=self.search_list)


        self.List_box = tk.Listbox(root, listvariable=self.list_var, selectmode='extended',bg="#00CCFF",height=10, font=('Comic Sans MS', 18),selectforeground='White')
        self.scrollbar = Scrollbar(root, orient='vertical', command=self.List_box.yview)
        self.clear_btn = Button(root, text='Clear History', command=self.Clear_History,
                                font=('Comic Sans MS', 12, "bold"), bg='#00CCFF')
        self.Back_btn = Button(root, text='<', command=self.Back_to_FirstPage, font=("Comic Sans MS", 12, "bold"),bg='#00CCFF')

    def Show_widgets(self):
        self.List_box.grid(row=1, column=0, sticky='nwes')
        self.scrollbar.grid(row=1, column=1, sticky='nsw')
        self.clear_btn.grid(row=0, column=1, sticky='w', ipady=10)
        self.Back_btn.grid(row=0, column=0, ipady=10, sticky='w')
        self.List_box.bind('<<ListboxSelect>>', self.When_city_in_History_is_clicked)

    def History_Table(self):
        # CONNECT TO DATABASE;
        conn = sqlite3.connect('HistoryDB.db')
        cursor = conn.cursor()

        # GET SEARCHES SAVED TO search_history TABLE;
        cursor.execute("SELECT * FROM search_history")
        searches = cursor.fetchall()

        # ADDING SEARCHES TO A LIST;
        self.search_list = []
        for search in searches:
            self.search_list.append(str(search[0]))

        # CLOSE CONNECTION;
        conn.commit()
        conn.close()

        return self.search_list

    def Clear_History(self):
        # FUNCTION IS CALLED WHEN THE CLEAR HISTORY BUTTON IS CLICKED;
        # CONNECT TO DATABASE;
        conn = sqlite3.connect('HistoryDB.db')
        cursor = conn.cursor()

        # DELETE EVERYTHING IN search_history TABLE;
        cursor.execute("DELETE FROM search_history")
        self.List_box.delete(0, END)

        # CHECKING IF DELETION WAS SUCCESSFUL;
        cursor.execute("""SELECT * FROM search_history""")
        empty_History_list = cursor.fetchall()

        # CLOSE CONNECTION;
        conn.commit()
        conn.close()

        return empty_History_list

    def Back_to_FirstPage(self):
        # FUNCTION IS CALLED WHEN THE '<' IS CLICKED, WIDGETS ARE DESTROYED AND USER IS TAKEN BACK TO HOMEPAGE;
        self.List_box.destroy()
        self.scrollbar.destroy()
        self.clear_btn.destroy()
        self.Back_btn.destroy()
        FirstPage(root)

    def When_city_in_History_is_clicked(self,event):
        # FUNCTION IS CALLED WHEN A USER CLICKS ON AN ITEM IN THE HISTORY TABLE,
        # THEY ARE TAKEN BACK TO HOME PAGE AND SELECTED ITEM APPEARS IN SEARCH BOX;

        self.selected_indices = self.List_box.curselection()  # get selected indices
        self.selected_word = ",".join([self.List_box.get(i) for i in self.selected_indices])  # get selected items

        self.List_box.destroy()
        self.scrollbar.destroy()
        self.clear_btn.destroy()
        self.Back_btn.destroy()
        FirstPage(root, self.selected_word)

        return self.selected_word





root.mainloop()
