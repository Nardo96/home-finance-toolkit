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

        #Make tabs expandable/shrinkable to window size
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        #--------------------------SET UP USERS AND ACCOUNTS TAB----------------------------
        #Create Users and Accounts frame
        users_frame = ttk.Frame(container, height=500, width=800)
        users_frame.grid(column=0, row=0, sticky='nsew')
        container.add(users_frame, text='Users and Accounts')

        #Split frame into two smaller left and right frames
        users_frame_left = ttk.Frame(users_frame, height=500, width=200, borderwidth=4,
                                     relief='ridge')
        users_frame_left.grid(column=0, row=0, sticky='nsew')

        users_frame_right = ttk.Frame(users_frame, height=500, width=400, borderwidth=4,
                                      relief='ridge')
        users_frame_right.grid(column=1, row=0, sticky='nsew')

        users_frame.rowconfigure(0, weight=1)
        users_frame.columnconfigure(0, weight=0)
        users_frame.columnconfigure(1, weight=3)

        #Set up users in the left frame
        def loadUsers():
            nonlocal users_frame_left
            users = getUsers()
            user_names = []
            for user in users:
                user_names.append(user[1])

            users_var = tk.StringVar(value=user_names)
            users_listbox = tk.Listbox(users_frame_left, height=10, width=12, listvariable=users_var)
            users_listbox.grid(column=0, row=0, sticky='nsew')
            return users_listbox

        users_listbox = loadUsers()
        users_frame_left.rowconfigure(0, weight=1)
        users_frame_left.columnconfigure(0, weight=1)

        #Add buttons to add, delete, or select users
        def addNewUser(user_name):
            nonlocal users_listbox
            nonlocal user_name_var
            addUser(user_name)
            users_listbox = loadUsers()
            user_name_var.set('')

        users_buttons_frame = ttk.Frame(users_frame_left)
        users_buttons_frame.grid(column=0, row=1, sticky='nsew')
        users_frame_left.rowconfigure(1, weight=1)

        user_name_var = tk.StringVar()
        users_add_entry = ttk.Entry(users_buttons_frame, textvariable=user_name_var)
        users_add_button = ttk.Button(users_buttons_frame, text="Add User",
                                      command=lambda: addNewUser(user_name_var.get()))

        users_add_entry.grid(column=0, row=0)
        users_add_button.grid(column=0, row=1)
        users_buttons_frame.rowconfigure(0, weight=1)
        users_buttons_frame.rowconfigure(1, weight=1)
        users_buttons_frame.columnconfigure(0, weight=1)

        def deleteExistingUser():
            nonlocal users_listbox
            user_list = getUsers()
            user_ids = {}
            for user in user_list:
                user_ids[user[1]] = user[0]

            selected_index = users_listbox.curselection()
            deleteUser(user_ids[users_listbox.get(selected_index)])
            users_listbox.delete(selected_index)

        users_delete_button = ttk.Button(users_buttons_frame, text='Delete User',
                                         command= deleteExistingUser)
        users_delete_button.grid(column=0, row=2)
        users_buttons_frame.rowconfigure(2, weight=1)

        selected_user_id = tk.StringVar()
        selected_user_id.set(1)
        def selectUser():
            nonlocal selected_user_id
            nonlocal users_listbox

            user_list = getUsers()
            user_ids = {}
            for user in user_list:
                user_ids[user[1]] = user[0]

            selected_index = users_listbox.curselection()
            selected_user_id.set((user_ids[users_listbox.get(selected_index)]))
            print(selected_user_id.get())
            loadAccounts()
            users_listbox.selection_clear(0, tk.END)

        user_select_button = ttk.Button(users_buttons_frame, text='Select User',
                                        command= selectUser)
        user_select_button.grid(column=0, row=3)
        users_buttons_frame.rowconfigure(3, weight=1)
        #Set up right Accounts frame
        def loadAccounts():
            nonlocal users_frame_right
            nonlocal selected_user_id
            userid = int(selected_user_id.get())
            accounts_list = getAccounts(userid)

            accounts_table = ttk.Treeview(users_frame_right)
            accounts_table['columns'] = ('Account ID', 'Account Name', 'Checking', '401k')

            accounts_table.column('#0', width=0, stretch=tk.NO)
            accounts_table.column('Account ID', anchor=tk.CENTER, width=20)
            accounts_table.column('Account Name', anchor=tk.CENTER, width=20)
            accounts_table.column('Checking', anchor=tk.CENTER, width=20)
            accounts_table.column('401k', anchor=tk.CENTER, width=80)
            accounts_table.heading('#0', text='', anchor=tk.CENTER)
            accounts_table.heading('Account ID', text='Account ID', anchor=tk.CENTER)
            accounts_table.heading('Account Name', text='Account Name', anchor=tk.CENTER)
            accounts_table.heading('Checking', text='Checking', anchor=tk.CENTER)
            accounts_table.heading('401k', text='401k', anchor=tk.CENTER)

            for i, row in enumerate(accounts_list):
                accounts_table.insert(parent='', index='end', iid=i, text='',
                                          values=row)
            accounts_table.grid(column=0, row=0, sticky='nsew')

            return accounts_table

        accounts_table = loadAccounts()
        users_frame_right.rowconfigure(0, weight=1)
        users_frame_right.columnconfigure(0, weight=1)




        #--------------------------SET UP TRANSACTIONS TAB---------------------

        #Create individual tab frames and grid to container
        transactions_frame = ttk.Frame(container, height=500, width=800, borderwidth=4,
                                       relief="ridge")
        transactions_frame.grid(column=0, row=0, sticky='nsew')

        options_frame = ttk.Frame(container, height=500, width=800, borderwidth=4,
                                  relief="ridge")
        options_frame.grid(column=0, row=0, sticky='nsew')


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
        def createTransactionTable(userid):
            data = getTransactions(int(userid))

            transactions_table = ttk.Treeview(transactions_container)
            transactions_table['columns'] = ('TransactionID', 'Account', 'Transaction Type',
                                             'Date', 'Value')
            transactions_table.column('#0', width=0, stretch=tk.NO)
            transactions_table.column('TransactionID', anchor=tk.CENTER,width=20)
            transactions_table.column('Account', anchor=tk.CENTER, width=20)
            transactions_table.column('Transaction Type', anchor=tk.CENTER, width=20)
            transactions_table.column('Date', anchor=tk.CENTER, width=80)
            transactions_table.column('Value', anchor=tk.CENTER, width=40)
            transactions_table.heading('#0', text='', anchor=tk.CENTER)
            transactions_table.heading('TransactionID', text='Transaction ID', anchor=tk.CENTER)
            transactions_table.heading('Account', text='Transaction Type ID', anchor=tk.CENTER)
            transactions_table.heading('Transaction Type', text='Account ID', anchor=tk.CENTER)
            transactions_table.heading('Date', text='Date', anchor=tk.CENTER)
            transactions_table.heading('Value', text='Value', anchor=tk.CENTER)

            for i, row in enumerate(data):
                transactions_table.insert(parent='', index='end', iid=i, text='',
                                          values=row)
            transactions_table.grid(column=0, row=0, sticky='nsew')
            transactions_container.rowconfigure(0, weight=1)
            transactions_container.columnconfigure(0, weight=1)

            return transactions_table

        transactions_table = createTransactionTable(1)

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

        all_data = getTransactions() + getDeletedTransactions()
        rowcount = len(all_data)

        def addTransactionTable(AccountID, TransactionTypeID, Date, Value):
            #Add transaction to DB, update GUI table, and set inputs back to blank
            nonlocal rowcount
            addTransaction(AccountID, TransactionTypeID, Date, Value)
            rowcount += 1
            row = [rowcount, AccountID, TransactionTypeID, Date, Value]
            transactions_table.insert(parent='', index='end', iid=rowcount, text='',
                                      values=row)
            account_entry_var.set('')
            transaction_type_entry_var.set('')
            date_entry_var.set('')
            value_entry_var.set('')

        add_transaction_button = ttk.Button(transactions_input_container_right,
                                   text='Add Transaction',
                                   command=lambda: addTransactionTable(int(account_entry_var.get()),
                                                                  int(transaction_type_entry_var.get()),
                                                                  date_entry_var.get(),
                                                                  float(value_entry_var.get())))
        add_transaction_button.grid(column=0, row=0, sticky='nsew')

        def changeTransactionTable(AccountID, TransactionTypeID, Date, Value):
            #Get ID of selected item, update DB values and table, and reset input to blank
            selected_item = transactions_table.focus()
            transactionID = int(transactions_table.item(selected_item)['values'][0])
            updateTransaction(transactionID, AccountID, TransactionTypeID, Date, Value)
            values = [AccountID, TransactionTypeID, Date, Value]
            for i in range(4):
                transactions_table.set(selected_item, column=i+1, value=values[i])
            for item in transactions_table.selection():
                transactions_table.selection_remove(item)
            account_entry_var.set('')
            transaction_type_entry_var.set('')
            date_entry_var.set('')
            value_entry_var.set('')


        change_transaction_button = ttk.Button(transactions_input_container_right,
                                       text='Change Transaction Data',
                                       command=lambda: changeTransactionTable(int(account_entry_var.get()),
                                                                         int(transaction_type_entry_var.get()),
                                                                         date_entry_var.get(),
                                                                         float(value_entry_var.get())))
        change_transaction_button.grid(column=1, row=0, sticky='nsew')

        def deleteTransactionTable():
            #Take selected row and delete from db (isDeleted=1) and table
            selected_item = transactions_table.focus()
            transactionID = transactions_table.item(selected_item)['values'][0]
            deleteTransaction(transactionID)
            transactions_table.delete(selected_item)


        delete_transaction_button = ttk.Button(transactions_input_container_right,
                                               text='Delete Transaction',
                                               command=deleteTransactionTable)
        delete_transaction_button.grid(column=2, row=0, sticky='nsew')


        for child in transactions_frame.winfo_children():
            x = child.winfo_x()
            y = child.winfo_y()
            transactions_frame.columnconfigure(y, weight=1)
            transactions_frame.rowconfigure(x, weight=1)








root = tk.Tk()
hft = HomeFinanceToolkit(root)
root.mainloop()
