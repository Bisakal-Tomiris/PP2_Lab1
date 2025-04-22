import psycopg2
import csv

# Database connection
conn = psycopg2.connect(
    dbname="phonebook",
    user="postgres",
    password="tomi2007",
    host="localhost",
    port="5432" 
)
cur = conn.cursor()

# Create table
def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            phone VARCHAR(20) UNIQUE
        );
    """)
    conn.commit()

# Insert from CSV file
def insert_from_csv(filename):
    with open(filename, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                cur.execute("""
                    INSERT INTO phonebook (first_name, last_name, phone)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (phone) DO NOTHING;
                """, (row['first_name'], row['last_name'], row['phone']))
            except Exception as e:
                print("Error inserting:", e)
    conn.commit()
    print("Data loaded from CSV.")

# Insert from console
def insert_from_console():
    fname = input("First name: ")
    lname = input("Last name: ")
    phone = input("Phone: ")
    try:
        cur.execute("""
            INSERT INTO phonebook (first_name, last_name, phone)
            VALUES (%s, %s, %s);
        """, (fname, lname, phone))
        conn.commit()
        print("Contact added.")
    except Exception as e:
        print("Error:", e)
        conn.rollback()

# Update data
def update_entry():
    phone = input("Enter phone number to update: ")
    new_fname = input("New first name (leave empty to skip): ")
    new_phone = input("New phone number (leave empty to skip): ")

    if new_fname:
        cur.execute("UPDATE phonebook SET first_name = %s WHERE phone = %s;", (new_fname, phone))
    if new_phone:
        cur.execute("UPDATE phonebook SET phone = %s WHERE phone = %s;", (new_phone, phone))
    conn.commit()
    print("Updated.")

# Query data with filter
def query_entries():
    print("Search by: 1) First Name 2) Last Name 3) Phone")
    option = input("Choose: ")
    value = input("Enter value: ")

    if option == "1":
        cur.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s;", ('%' + value + '%',))
    elif option == "2":
        cur.execute("SELECT * FROM phonebook WHERE last_name ILIKE %s;", ('%' + value + '%',))
    elif option == "3":
        cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s;", ('%' + value + '%',))
    rows = cur.fetchall()
    for row in rows:
        print(row)

# Delete entry
def delete_entry():
    value = input("Enter first name or phone to delete: ")
    cur.execute("DELETE FROM phonebook WHERE first_name = %s OR phone = %s;", (value, value))
    conn.commit()
    print("Deleted.")

# Main menu
def menu():
    create_table()
    while True:
        print("\n--- PhoneBook Menu ---")
        print("1. Insert from CSV")
        print("2. Insert from Console")
        print("3. Update Contact")
        print("4. Search Contact")
        print("5. Delete Contact")
        print("6. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            insert_from_csv("data.csv")
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_entry()
        elif choice == "4":
            query_entries()
        elif choice == "5":
            delete_entry()
        elif choice == "6":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    menu()
    cur.close()
    conn.close()