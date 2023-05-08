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
                data_filtered.append(row[0:5])

        transactions_table = ttk.Treeview(transactions_container)
        transactions_table['columns'] = ('TransactionID', 'AccountID', 'TransactionTypeID',
                                         'Date', 'Value')
        transactions_table.column('#0', width=0, stretch=tk.NO)
        transactions_table.column('TransactionID', anchor=tk.CENTER,width=20)
        transactions_table.column('AccountID', anchor=tk.CENTER, width=20)
        transactions_table.column('TransactionTypeID', anchor=tk.CENTER, width=20)
        transactions_table.column('Date', anchor=tk.CENTER, width=80)
        transactions_table.column('Value', anchor=tk.CENTER, width=40)
        transactions_table.heading('#0', text='', anchor=tk.CENTER)
        transactions_table.heading('TransactionID', text='Transaction ID', anchor=tk.CENTER)
        transactions_table.heading('TransactionTypeID', text='Transaction Type ID', anchor=tk.CENTER)
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
        transactions_input_container = ttk.Frame(transactions_frame, height=100, width=800)
        transactions_input_container.grid(column=0, row=1, sticky='ew')
        transactions_container.rowconfigure(1, weight=0)

        #Split input frame into left and right frames
        transactions_input_container_left = ttk.Frame(transactions_input_container, height=100, width=600)
        transactions_input_container_left.grid(column=0, row=0, sticky='nsew')
        transactions_input_container.rowconfigure(0, weight=0)
        transactions_input_container.columnconfigure(0, weight=1)

        #Set up left input entry headers
        for i, header in enumerate(['Account ID', 'Transaction Type ID', 'Date', 'Value']):
            l = ttk.Label(transactions_input_container_left, text=header, anchor=tk.CENTER,
                          relief='ridge')
            l.grid(row=0, column=i, sticky='ew')
        transactions_input_container_left.rowconfigure(0, weight=1)
        transactions_input_container_left.columnconfigure(0, weight=1)
        transactions_input_container_left.columnconfigure(1, weight=1)
        transactions_input_container_left.columnconfigure(2, weight=1)
        transactions_input_container_left.columnconfigure(3, weight=1)

        #Set up left input entries
        account_entry_var = tk.StringVar()
        transaction_type_entry_var = tk.StringVar()
        date_entry_var = tk.StringVar()
        value_entry_var = tk.StringVar()
        input_var_list = [account_entry_var, transaction_type_entry_var,
                          date_entry_var, value_entry_var]
        for i in range(4):
            e = ttk.Entry(transactions_input_container_left,
                          textvariable=input_var_list[i])
            e.grid(row=1, column=i, sticky='nsew')


        transactions_input_container_left.rowconfigure(1, weight=1)


        #Set up input buttons
        transactions_input_container_right = ttk.Frame(transactions_input_container, height=100,
                                               width=300)
        transactions_input_container_right.grid(row=0, column=1, rowspan=2, sticky='nsew')
        button_names = ['Add Personal Transaction', 'Add Employer Contribution',
                        'Add Current Value', 'Change Transaction Data',
                        'Delete Transaction']
        for i in range(3):
            b = ttk.Button(transactions_input_container_right, text=button_names[i],
                           padding='0 0 0 0')
            b.grid(column=0, row=i, sticky='nsew')
        for i in range(3, 5):
            b = ttk.Button(transactions_input_container_right, text=button_names[i],
                           padding='0 0 0 0')
            b.grid(column=1, row=i-3, sticky='nsew')

        for child in transactions_frame.winfo_children():
            x = child.winfo_x()
            y = child.winfo_y()
            transactions_frame.columnconfigure(y, weight=1)
            transactions_frame.rowconfigure(x, weight=1)






root = tk.Tk()
hft = HomeFinanceToolkit(root)
root.mainloop()