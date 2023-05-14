from main import *
import tkinter as tk
from tkinter import ttk


class HomeFinanceToolkit:
    def __init__(self, parent):
        parent.title("Home Finance Toolkit")
        transaction_types = {'Transfer': 1, 'Employer Contribution': 2, 'Current Value': 3}

        #Set up Notebook container
        container = ttk.Notebook(parent, height=450, width=1000, padding="0 0 0 0")
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
        users_listbox.bind('<Double-1>', lambda e: selectUser())
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
                                         command=deleteExistingUser)
        users_delete_button.grid(column=0, row=2)
        users_buttons_frame.rowconfigure(2, weight=1)

        selected_user_id = tk.StringVar()
        selected_user_id.set(1)

        def selectUser():
            nonlocal selected_user_id
            nonlocal users_listbox
            nonlocal accounts_table
            nonlocal transactions_table
            nonlocal account_dropdown

            user_list = getUsers()
            user_ids = {}
            for user in user_list:
                user_ids[user[1]] = user[0]

            selected_index = users_listbox.curselection()
            selected_user_id.set((user_ids[users_listbox.get(selected_index)]))
            id = int(selected_user_id.get())
            print(id)
            accounts_table = createAccountsTable()
            transactions_table = createTransactionTable(id)
            accounts = getAccounts(id)
            account_names = []
            for account in accounts:
                account_names.append(account[1])
            account_dropdown_values = tuple(account_names)
            account_dropdown['values'] = account_dropdown_values
            users_listbox.selection_clear(0, tk.END)

        user_select_button = ttk.Button(users_buttons_frame, text='Select User',
                                        command=selectUser)
        user_select_button.grid(column=0, row=3)
        users_buttons_frame.rowconfigure(3, weight=1)

        #Set up right Accounts frame
        #Set up Accounts table
        def createAccountsTable():
            nonlocal users_frame_right
            nonlocal selected_user_id
            userid = int(selected_user_id.get())
            accounts_list = getAccounts(userid)
            accounts_list_filtered = []
            for account in accounts_list:
                accounts_list_filtered.append(account[0:2] + account[3:5])

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

            for i, row in enumerate(accounts_list_filtered):
                accounts_table.insert(parent='', index='end', iid=i, text='',
                                      values=row)
            accounts_table.grid(column=0, row=0, sticky='nsew')

            return accounts_table

        accounts_table = createAccountsTable()
        users_frame_right.rowconfigure(0, weight=1)
        users_frame_right.columnconfigure(0, weight=1)

        #Set up account entries
        users_frame_right_inputs = ttk.Frame(users_frame_right)
        users_frame_right_inputs.grid(row=1, column=0, sticky='nsew')
        users_frame_right.rowconfigure(1, weight=1)

        for i, header in enumerate(['Account Name', 'Checking', '401k']):
            l = ttk.Label(users_frame_right_inputs, text=header, anchor=tk.CENTER,
                          relief='ridge')
            l.grid(row=0, column=i, sticky='ew')
        users_frame_right_inputs.rowconfigure(0, weight=0)
        users_frame_right_inputs.columnconfigure(0, weight=1)
        users_frame_right_inputs.columnconfigure(1, weight=1)
        users_frame_right_inputs.columnconfigure(2, weight=1)
        users_frame_right_inputs.columnconfigure(3, weight=1)

        account_name_entry = tk.StringVar()
        account_checking_entry = tk.StringVar()
        account_retirement_entry = tk.StringVar()
        input_var_list = [account_name_entry, account_checking_entry,
                          account_retirement_entry]
        for i in range(3):
            e = ttk.Entry(users_frame_right_inputs,
                          textvariable=input_var_list[i])
            e.grid(row=2, column=i, sticky='nsew')
            users_frame_right_inputs.columnconfigure(i, weight=1)

        #Set up add account and delete account buttons

        accounts_count = len(getAccounts())

        def createNewAccount(account_name, checking, retirement):
            nonlocal accounts_count
            nonlocal accounts_table
            addAccount(account_name, selected_user_id.get(), checking, retirement)
            accounts_count += 1
            accounts_table = createAccountsTable()

            accounts = getAccounts(selected_user_id.get())
            account_names = []
            for account in accounts:
                account_names.append(account[1])
            account_dropdown_values = tuple(account_names)
            account_dropdown['values'] = account_dropdown_values

            account_name_entry.set('')
            account_checking_entry.set('')
            account_retirement_entry.set('')

        add_account_button = ttk.Button(users_frame_right_inputs,
                                        text='Add Account',
                                        command=lambda: createNewAccount(
                                            account_name_entry.get(),
                                            account_checking_entry.get(),
                                            account_retirement_entry.get()
                                        ))
        add_account_button.grid(column=1, row=3, sticky='nsew')
        users_frame_right_inputs.rowconfigure(3, weight=1)

        def deleteExistingAccount():
            selected_item = accounts_table.focus()
            account_id = int(accounts_table.item(selected_item)['values'][0])
            deleteAccount(account_id)
            accounts_table.delete(selected_item)

        delete_account_button = ttk.Button(users_frame_right_inputs,
                                           text='Delete Account',
                                           command=deleteExistingAccount)
        delete_account_button.grid(column=1, row=4, sticky='nsew')
        users_frame_right_inputs.rowconfigure(4, weight=1)

        #--------------------------SET UP TRANSACTIONS TAB---------------------

        #Create individual tab frames and grid to container
        transactions_frame = ttk.Frame(container, height=500, width=800, borderwidth=4,
                                       relief="ridge")
        transactions_frame.grid(column=0, row=0, sticky='nsew')

        #Add frame as individual tabs to notebook
        container.add(transactions_frame, text="Transactions")

        #Set up Transactions Tab
        #Set up Transactions Table frame
        transactions_container = ttk.Frame(transactions_frame,
                                           height=400, width=600,
                                           relief="ridge")
        transactions_container.grid(column=0, row=0, sticky='nsew')

        #Set up data table
        #Set up header and add data filtered for selected columns

        def getNamedData(userid):
            data = getTransactions(int(userid))
            named_data = []

            account_list = getAccounts(userid)
            account_names = {}
            for account in account_list:
                account_names[int(account[0])] = account[1]
            transaction_types = {1: 'Transfer', 2: 'Employer Contribution', 3: 'Current Value'}
            for row in account_list:
                account_names[int(row[0])] = row[1]

            for row in data:
                new_row = (row[0], account_names[row[1]], transaction_types[int(row[2])],
                           row[3], row[4])
                named_data.append(new_row)
            return named_data

        def getAccountID(account_name):
            accounts = getAccounts(int(selected_user_id.get()))
            accounts_id = {}
            for row in accounts:
                accounts_id[row[1]] = int(row[0])
            return accounts_id[account_name]


        def createTransactionTable(userid):
            data = getNamedData(userid)

            transactions_table = ttk.Treeview(transactions_container)
            transactions_table['columns'] = ('TransactionID', 'Account', 'Transaction Type',
                                             'Date', 'Value')
            transactions_table.column('#0', width=0, stretch=tk.NO)
            transactions_table.column('TransactionID', anchor=tk.CENTER, width=20)
            transactions_table.column('Account', anchor=tk.CENTER, width=20)
            transactions_table.column('Transaction Type', anchor=tk.CENTER, width=20)
            transactions_table.column('Date', anchor=tk.CENTER, width=80)
            transactions_table.column('Value', anchor=tk.CENTER, width=40)
            transactions_table.heading('#0', text='', anchor=tk.CENTER)
            transactions_table.heading('TransactionID', text='Transaction ID', anchor=tk.CENTER)
            transactions_table.heading('Account', text='Account', anchor=tk.CENTER)
            transactions_table.heading('Transaction Type', text='Transaction Type', anchor=tk.CENTER)
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
        for i, header in enumerate(['Account', 'Transaction Type', 'Date', 'Value']):
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

        input_var_list = [date_entry_var, value_entry_var]

        account_dropdown = ttk.Combobox(transactions_input_container_left,
                                         textvariable=account_entry_var)
        account_dropdown.grid(row=1, column=0, sticky='nsew')
        accounts = getAccounts(int(selected_user_id.get()))
        account_names = []
        for account in accounts:
            account_names.append(account[1])
        account_dropdown_values = tuple(account_names)
        account_dropdown['values'] = account_dropdown_values

        transaction_type_dropdown = ttk.Combobox(
            transactions_input_container_left,
            textvariable = transaction_type_entry_var)
        transaction_type_dropdown.grid(row=1, column=1, sticky='nsew')
        transaction_type_dropdown_values = ('Transfer', 'Employer Contribution',
                                            'Current Value')
        transaction_type_dropdown['values'] = transaction_type_dropdown_values

        for i in range(2):
            e = ttk.Entry(transactions_input_container_left,
                          textvariable=input_var_list[i])
            e.grid(row=1, column=i+2, sticky='nsew')
        transactions_input_container_left.rowconfigure(1, weight=1)

        #Set up input buttons
        transactions_input_container_right = ttk.Frame(
            transactions_input_container, height=100, width=300)
        transactions_input_container_right.grid(row=0, column=1, rowspan=2,
                                                sticky='nsew')
        all_data = getTransactions() + getDeletedTransactions()
        rowcount = len(all_data)

        def addTransactionTable(account_name, transaction_type, date, value):
            #Add transaction to DB, update GUI table, and set inputs back to blank
            nonlocal rowcount
            nonlocal transactions_table

            account_id = getAccountID(account_name)
            addTransaction(account_id,
                           transaction_types[transaction_type], date, value)
            rowcount += 1
            transactions_table = createTransactionTable(selected_user_id.get())
            account_entry_var.set('')
            transaction_type_entry_var.set('')
            date_entry_var.set('')
            value_entry_var.set('')

        add_transaction_button = ttk.Button(
            transactions_input_container_right,
            text='Add Transaction',
            command=lambda:
            addTransactionTable(
                account_entry_var.get(),
                transaction_type_entry_var.get(),
                date_entry_var.get(),
                float(value_entry_var.get())))
        add_transaction_button.grid(column=0, row=0, sticky='nsew')

        def changeTransactionTable(account_name, transaction_type, date, value):
            #Get ID of selected item, update DB values and table, and reset input to blank
            nonlocal transactions_table
            selected_item = transactions_table.focus()
            transactions_table = createTransactionTable(int(selected_user_id.get()))
            transaction_id = int(transactions_table.item(selected_item)['values'][0])

            account_id = getAccountID(account_name)
            updateTransaction(transaction_id, account_id, transaction_types[transaction_type], date,
                              value)
            values = [account_name, transaction_type, date, value]
            for i in range(4):
                transactions_table.set(selected_item, column=i+1, value=values[i])
            for item in transactions_table.selection():
                transactions_table.selection_remove(item)
            account_entry_var.set('')
            transaction_type_entry_var.set('')
            date_entry_var.set('')
            value_entry_var.set('')

        change_transaction_button = ttk.Button(
            transactions_input_container_right,
            text='Change Transaction Data',
            command=lambda: changeTransactionTable(
                account_entry_var.get(),
                transaction_type_entry_var.get(),
                date_entry_var.get(),
                float(value_entry_var.get())))
        change_transaction_button.grid(column=1, row=0, sticky='nsew')

        def deleteTransactionTable():
            #Take selected row and delete from db (isDeleted=1) and table
            selected_item = transactions_table.focus()
            transaction_id = transactions_table.item(selected_item)['values'][0]
            deleteTransaction(transaction_id)
            transactions_table.delete(selected_item)

        delete_transaction_button = ttk.Button(transactions_input_container_right,
                                               text='Delete Transaction',
                                               command=deleteTransactionTable)
        delete_transaction_button.grid(column=2, row=0, sticky='nsew')

        #-------------------------SET UP BALANCES TAB--------------------------------
        def getBalances(accounts):
            # Take list of account names, return dictionary of account:balances
            account_balances = {}
            for account in accounts:
                account_id = getAccountID(account)
                result = cur.execute(f'SELECT Checking FROM Accounts '
                                         f'WHERE AccountID = {account_id}')
                investment = int(result.fetchone()[0])
                #If investment account, get latest current value; else, sum transfers and employer contributions
                if investment == 0:
                    results = cur.execute(f'SELECT Value FROM Transactions WHERE AccountID = {account_id} '
                                          f'AND TransactionTypeID = 3 '
                                          f'ORDER BY TransactionID DESC')
                    if results.fetchone() == None:
                        result = cur.execute(f'SELECT SUM(Value) FROM Transactions WHERE AccountID = {account_id} '
                                             f'AND TransactionTypeID IN (1, 2)')
                        account_balances[account] = result.fetchone()[0]
                    else:
                        result = cur.execute(f'SELECT Value FROM Transactions WHERE AccountID = {account_id} '
                                             f'AND TransactionTypeID = 3 '
                                             f'ORDER BY TransactionID DESC')
                        account_balances[account] = result.fetchone()[0]
                else:
                    result = cur.execute(f'SELECT SUM(Value) FROM Transactions WHERE AccountID = {account_id} '
                                         f'AND TransactionTypeID IN (1, 2)')
                    account_balances[account] = result.fetchone()[0]
            return account_balances
        def getCurrentValues(accounts):
            #TODO: transfer investment account logic above into this function
            pass
        print(getBalances(['Wells Fargo Checking', 'Citbank Savings', 'Slavic 401k', 'WeBull']))


        #-------------------------SET UP CONFIGURATION OPTIONS TAB-------------------
        #Set up Options tab frame
        options_frame = ttk.Frame(container, height=500, width=800, borderwidth=4,
                                  relief="ridge")
        options_frame.grid(column=0, row=0, sticky='nsew')
        container.add(options_frame, text="Options")

        for child in transactions_frame.winfo_children():
            x = child.winfo_x()
            y = child.winfo_y()
            transactions_frame.columnconfigure(y, weight=1)
            transactions_frame.rowconfigure(x, weight=1)


root = tk.Tk()
hft = HomeFinanceToolkit(root)
root.mainloop()
