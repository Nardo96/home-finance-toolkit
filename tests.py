from main import *

con = sql.connect('hft.db')
cur = con.cursor()

# Query values as test
print('\n\n\n---------TEST: SELECT * FROM ACCOUNTS-------\n')
results = cur.execute("""
SELECT * 
FROM Accounts
""")
for row in results:
    print(row)

print('\n\n\n---------TEST: SELECT * FROM USERS-------\n')
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

