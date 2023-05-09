import sqlite3 as sql
import csv

# Connect to database
con = sql.connect('hft.db')
cur = con.cursor()

def addTransaction(AccountID, TransactionTypeID, Date, Value):
    try:
        row = [AccountID, TransactionTypeID, Date, Value]
        cur.execute("""
        INSERT INTO Transactions(AccountID, TransactionTypeID, Date, Value)
        VALUES (?,?,?,?)
        """, row)
        con.commit()
    except:
        print("Input Error in addTransaction")


def deleteTransaction(TransactionID):
    cur.execute(f'UPDATE Transactions SET IsDeleted = 1 \
    WHERE TransactionID = CAST({TransactionID} AS INTEGER)')
    con.commit()

def updateTransaction(TransactionID, AccountID=None,
                      TransactionTypeID=None, Date=None, Value=None, IsDeleted=None):
    try:
        if AccountID != None:
            cur.execute(f'UPDATE Transactions SET AccountID = {AccountID} \
            WHERE TransactionID = CAST({TransactionID} AS INTEGER)')
        if TransactionTypeID != None:
            cur.execute(f'UPDATE Transactions SET TransactionTypeID = {TransactionTypeID} \
            WHERE TransactionID = CAST({TransactionID} AS INTEGER)')
        if Date != None:
            cur.execute(f'Update Transactions SET Date = {Date} \
            WHERE TransactionID = CAST({TransactionID} AS INTEGER)')
        if Value != None:
            cur.execute(f'UPDATE Transactions SET Value = {Value} \
            WHERE TransactionID = CAST({TransactionID} AS INTEGER)')
        if IsDeleted != None:
            cur.execute(f'UPDATE Transactions SET IsDeleted = {IsDeleted} \
            WHERE TransactionID = CAST({TransactionID} AS INTEGER)')
    except:
        print("Input error in updateTransaction")

    con.commit()

def getTransactions():
    results = cur.execute('SELECT * FROM Transactions')
    results_list = []
    for row in results:
        results_list.append(row)
    return results_list


if __name__ == '__main__':
    # TODO: import from csv method
    #    DATAFILENAME = 'Budget.xlsx'
    #    FILEPATH = './'

    # Create tables if they don't exist
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Transactions(
    TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
    AccountID INTEGER,
    TransactionTypeID Integer,    
    Date TEXT,
    Value REAL,
    IsDeleted Integer)
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Accounts(
    AccountID INTEGER PRIMARY KEY AUTOINCREMENT,
    AccountName TEXT,
    UserID INTEGER,
    Checking INTEGER,
    [401K] INTEGER)
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Users(
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT)
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Configurations(
    ConfigurationID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID Integer,
    ConfigurationTypeID INTEGER,
    DateCreated TEXT,
    Value REAL)
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ConfigurationTypes(
    ConfigurationTypeID INTEGER PRIMARY KEY AUTOINCREMENT,
    TypeDescription TEXT)
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS TransactionTypes(
    TransactionTypeID INTEGER PRIMARY KEY AUTOINCREMENT,
    TypeDescription TEXT)
    """)

    con.commit()

    # Insert static schema description data
    cur.execute("""
    INSERT OR IGNORE INTO ConfigurationTypes VALUES
    (1, 'Salary'),
    (2, 'Hourly Rate'),
    (3, 'Hours per Year'),
    (4, 'Needs Rate'),
    (5, 'Discretionary Rate'),
    (6, 'Savings Rate'),
    (7, 'Down Payment %'),
    (8, 'Interest Rate')
    """)

    cur.execute("""
    INSERT OR IGNORE INTO TransactionTypes VALUES
    (1, 'UserTransaction'),
    (2, 'EmployerContribution'),
    (3, 'CurrentTransaction')
    """)

    # Insert example data
    with open('findata.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, dialect='excel')
        data = []
        for i, row in enumerate(reader):
            data.append(row)
            #Remove \ufeff prefix in first element
            if i == 0:
                data[0][0] = 1
            #Set datatypes to match Transactions table
            data[i][0] = int(data[i][0])
            data[i][1] = int(data[i][1])
            data[i][2] = int(data[i][2])
            data[i][4] = float(data[i][4])
        cur.executemany("""
        INSERT OR IGNORE INTO Transactions(TransactionID, AccountID, TransactionTypeID, Date, Value) 
        VALUES(?, ?, ?, ?, ?)""", data)
        con.commit()

    cur.execute("""
    INSERT OR IGNORE INTO Accounts VALUES
    (1, 'Wells Fargo Checking', 1, 1, 0),
    (2, 'Citbank Savings', 1, 0, 0),
    (3, 'Slavic 401k', 1, 0, 1),
    (4, 'WeBull',1, 0, 0)
    """)
    con.commit()

    cur.execute("""
    INSERT OR IGNORE INTO Users VALUES
    (1, 'Bernardo')
    """)
    con.commit()

