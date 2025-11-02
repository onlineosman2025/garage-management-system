import sqlite3

conn = sqlite3.connect('garage.db')
cursor = conn.cursor()

print("=" * 50)
print("INVOICES TABLE:")
print("=" * 50)
cursor.execute('SELECT id, customer_id, amount, tax_rate, total_amount, status FROM invoices')
invoices = cursor.fetchall()
for inv in invoices:
    print(f"ID: {inv[0]}, Customer: {inv[1]}, Amount: {inv[2]}, Tax: {inv[3]}%, Total: {inv[4]}, Status: {inv[5]}")

print(f"\nTotal invoices: {len(invoices)}")

print("\n" + "=" * 50)
print("CUSTOMERS TABLE:")
print("=" * 50)
cursor.execute('SELECT id, name, email FROM customers')
customers = cursor.fetchall()
for cust in customers:
    print(f"ID: {cust[0]}, Name: {cust[1]}, Email: {cust[2]}")

print(f"\nTotal customers: {len(customers)}")

print("\n" + "=" * 50)
print("JOBS TABLE:")
print("=" * 50)
cursor.execute('SELECT id, customer_id, service_type, cost, status FROM jobs')
jobs = cursor.fetchall()
for job in jobs:
    print(f"ID: {job[0]}, Customer: {job[1]}, Service: {job[2]}, Cost: {job[3]}, Status: {job[4]}")

print(f"\nTotal jobs: {len(jobs)}")

conn.close()
