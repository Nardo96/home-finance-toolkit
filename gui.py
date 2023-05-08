from main import *
import tkinter as tk
from tkinter import ttk

class HomeFinanceToolkit:
    def __init__(self, parent):
        parent.title("Home Finance Toolkit")

        container = ttk.Notebook(parent, height=450, width=800, padding="0 0 0 0")
        container.grid(column=0, row=0, sticky='nsew')
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)

        transactions_frame = ttk.Frame(container, height=500, width=800, borderwidth=4,
                                       relief="ridge")
        transactions_frame.grid(column=0, row=0, sticky='nsew')

        options_frame = ttk.Frame(container, height=500, width=800, borderwidth=4,
                                  relief="ridge")
        options_frame.grid(column=0, row=0, sticky='nsew')

        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)
        container.add(transactions_frame, text="Transactions")
        container.add(options_frame, text="Options")






root = tk.Tk()
hft = HomeFinanceToolkit(root)
root.mainloop()