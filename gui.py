from main import *
import tkinter as tk
from tkinter import ttk

class HomeFinanceToolkit:
    def __init__(self, parent):
        parent.title("Home Finance Toolkit")

        #Set up Notebook container
        container = ttk.Notebook(parent, height=450, width=800, padding="0 0 0 0")
        container.grid(column=0, row=0, sticky='nsew')
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)

        #Create individual tab frames and grid to container
        transactions_frame = ttk.Frame(container, height=500, width=800, borderwidth=4,
                                       relief="ridge")
        transactions_frame.grid(column=0, row=0, sticky='nsew')

        options_frame = ttk.Frame(container, height=500, width=800, borderwidth=4,
                                  relief="ridge")
        options_frame.grid(column=0, row=0, sticky='nsew')

        #Make tabs expandable/shrinkable to window size
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        #Add frames as individual tabs to notebook
        container.add(transactions_frame, text="Transactions")
        container.add(options_frame, text="Options")

        #Set up Transactions Tab
        #Set up Transactions Table frame
        transactions_container = ttk.Frame(transactions_frame,  height=400, width=600,
                                       relief="ridge")
        transactions_container.grid(column=0, row=0, sticky='nsew')

        #Set up data table
        #Set up header and add data filtered for selected columns
        data = getTransactions()
        data_filtered = []
        for row in data:
            if row[5] != 1:
                data_filtered.append(row[0:2] + row[3:5])

        transactions_table = ttk.Treeview(transactions_container)
        transactions_table['columns'] = ('TransactionID', 'AccountID', 'Date', 'Value')
        transactions_table.column('#0', width=0, stretch=tk.NO)
        transactions_table.column('TransactionID', anchor=tk.CENTER,width=20)
        transactions_table.column('AccountID', anchor=tk.CENTER, width=20)
        transactions_table.column('Date', anchor=tk.CENTER, width=80)
        transactions_table.column('Value', anchor=tk.CENTER, width=40)
        transactions_table.heading('#0', text='', anchor=tk.CENTER)
        transactions_table.heading('TransactionID', text='Transaction ID', anchor=tk.CENTER)
        transactions_table.heading('AccountID', text='Account ID', anchor=tk.CENTER)
        transactions_table.heading('Date', text='Date', anchor=tk.CENTER)
        transactions_table.heading('Value', text='Value', anchor=tk.CENTER)

        for i, row in enumerate(data_filtered):
            transactions_table.insert(parent='', index='end', iid=i, text='',
                                      values=row)
        transactions_table.grid(column=0, row=0, sticky='nsew')
        transactions_container.rowconfigure(0, weight=1)
        transactions_container.columnconfigure(0, weight=1)

        # for child in transactions_table.winfo_children():
        #     x = child.winfo_x()
        #     y = child.winfo_y()
        #     transactions_table.columnconfigure(y, weight=1)
        #     transactions_table.rowconfigure(x, weight=1)

        #Set up input frame
        transactions_input_frame = ttk.Frame(transactions_frame, height=80, width=800,
                                             relief="ridge")
        transactions_input_frame.grid(column=0, row=1, sticky='sew')

        for child in transactions_frame.winfo_children():
            x = child.winfo_x()
            y = child.winfo_y()
            transactions_frame.columnconfigure(y, weight=1)
            transactions_frame.rowconfigure(x, weight=1)






root = tk.Tk()
hft = HomeFinanceToolkit(root)
root.mainloop()