from main import *

con = sql.connect('hft.db')
cur = con.cursor()

# Query values as test
print('\n\n\n---------TEST: SELECT * FROM Transactions-------\n')
results = getTransactions()
for row in results:
    print(row)

print('\n\n\n---------TEST: SELECT * FROM Accounts-------\n')
results = cur.execute("""
SELECT * 
FROM Accounts
""")
for row in results:
    print(row)

print('\n\n\n---------TEST: SELECT * FROM Users-------\n')
results = cur.execute("""
SELECT * 
FROM Users
""")
for row in results:
    print(row)

print('\n\n\n---------TEST: SELECT * FROM ConfigurationTypes------\n')
results = cur.execute("""
SELECT * 
FROM ConfigurationTypes
""")
for row in results:
    print(row)

print('\n\n\n---------TEST: SELECT * FROM TransactionTypes-------\n')
results = cur.execute("""
SELECT * 
FROM TransactionTypes
""")
for row in results:
    print(row)

print('\n\n\n---------TEST: SELECT SUM(Value) FROM Transactions (savings, deposited)-------\n')
results = cur.execute("""
SELECT SUM(Value)
FROM Transactions
WHERE AccountID IN (2, 3, 4)
AND TransactionTypeID IN (1,2)
""")
for row in results:
    print(row)

# Commented out addTransaction to stop adding transactions every test

# print('\n\n\n---------TEST: Add transaction with addTransaction()-------\n')
# addTransaction(1, 1, '2023-05-05', 0.01)
# results = cur.execute("""
# SELECT * FROM Transactions ORDER BY TransactionID DESC LIMIT 1
# """)
# for row in results:
#     print(row)


print('\n\n\n---------TEST: Delete transaction with deleteTransaction()-------\n')
#Get index of last row
results = cur.execute('SELECT COUNT(*) FROM Transactions')
for row in results:
    rowcount = int(row[0])
deleteTransaction(rowcount)
results = cur.execute("""
SELECT * FROM Transactions ORDER BY TransactionID DESC LIMIT 5
""")
for row in results:
    print(row)


print('\n\n\n---------TEST: Update transaction with updateTransaction()-------\n')
#Get index of last row
results = cur.execute('SELECT COUNT(*) FROM Transactions')
for row in results:
    rowcount = int(row[0])
updateTransaction(rowcount, Value=30.00)
results = cur.execute("""
SELECT * FROM Transactions ORDER BY TransactionID DESC LIMIT 5
""")
for row in results:
    print(row)

