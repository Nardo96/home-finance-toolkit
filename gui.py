from main import *
import tkinter as tk
from tkinter import ttk

class HomeFinanceToolkit:
    def __init__(self, parent):
        parent.title("Home Finance Toolkit")
        # parent.geometry('800x500')

        container = ttk.Frame(parent, relief='ridge', padding="12 12 12 12")
        container.grid(column=0, row=0, sticky='nsew')
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)

        main_frame = ttk.Frame(container, height=500, width=800, borderwidth=4, relief='ridge')
        main_frame.grid(column=0, row=0, sticky='nsew')
        tabs_bar = ttk.Frame(container, height=50, width=800, borderwidth=4, relief='ridge')
        tabs_bar.grid(column=0, row=1, sticky='we')

        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)
        container.rowconfigure(1, weight=0)


        ttk.Label(tabs_bar, text='Transactions').grid(column=0, row=0, sticky='nsew')
        ttk.Label(tabs_bar, text='Options').grid(column=1, row=0, sticky='nsew')
        tabs_bar.columnconfigure(0, weight=1)
        tabs_bar.rowconfigure(0, weight=1)





root = tk.Tk()
hft = HomeFinanceToolkit(root)
root.mainloop()