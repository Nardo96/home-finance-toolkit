import sqlite3 as sql
import csv

if __name__ == '__main__':
#TODO: import from csv method
#    DATAFILENAME = 'Budget.xlsx'
#    FILEPATH = './'

    #Connect to database
    con = sql.connect('hft.db')
    cur = con.cursor()

    #Create tables if they don't exist
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Transactions(
    TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
    AccountID INTEGER,
    TransactionTypeID Integer,    
    Date TEXT,
    Value REAL)
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

    #Insert static schema description data
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

    #Insert example data
    with open('findata.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, dialect='excel')
        data = []
        for i, row in enumerate(reader):
            data.append(row)
        cur.executemany("INSERT OR IGNORE INTO Transactions VALUES(?, ?, ?, ?, ?)", data)
        con.commit()

    cur.execute("""
    INSERT OR IGNORE INTO Accounts VALUES
    (1, 'Wells Fargo Checking', 1, 1, 0),
    (2, 'Citbank Savings', 1, 0, 0),
    (3, 'Slavic 401k', 1, 0, 1),
    (4, 'WeBull',1, 0, 0)
    """)

    cur.execute("""
    INSERT OR IGNORE INTO Users VALUES
    (1, 'Bernardo')
    """)


results = cur.execute("""
SELECT *
FROM Transactions
""")
print(results.fetchall())

results = cur.execute("""
SELECT * 
FROM Accounts
""")
print(results.fetchall())

results = cur.execute("""
SELECT * 
FROM Users
""")
print(results.fetchall())

results = cur.execute("""
SELECT * 
FROM ConfigurationTypes
""")
print(results.fetchall())

results = cur.execute("""
SELECT * 
FROM TransactionTypes
""")
print(results.fetchall())

results = cur.execute("""
SELECT SUM(Value)
FROM Transactions
WHERE AccountID IN (2, 3, 4)
AND TransactionTypeID IN (1,2)
""")
print(results.fetchone())