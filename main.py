import sqlite3 as sql

if __name__ == '__main__':
#TODO: import from csv method
#    DATAFILENAME = 'Budget.xlsx'
#    FILEPATH = './'

    con = sql.connect('hft.db')
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Transactions(
    TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
    AccountID INTEGER,
    TransactionTypeID Integer,    
    Date TEXT,
    Value REAL)
    """)
    con.commit()

results = cur.execute("""
SELECT * 
FROM Transactions
""")
con.commit()

print(results.fetchall())



