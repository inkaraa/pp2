import psycopg2
import csv
import sys

def create_connection():
    """
    Establish and return a connection to the PostgreSQL database.
    Adjust connection parameters as needed.
    """
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="phonebookdb",
            user="inkara",
            password=""
        )
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        sys.exit(1)

def create_table(conn):
    """
    Create the PhoneBook table if it does not already exist.
    The table has an auto-increment id, a name, and a phone column.
    """
    cur = conn.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        phone VARCHAR(50) NOT NULL
    );
    """
    cur.execute(create_table_query)
    conn.commit()
    cur.close()

def insert_data_console(conn):
    """
    Insert a record into the PhoneBook table using user input from the console.
    """
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    cur = conn.cursor()
    insert_query = "INSERT INTO phonebook (name, phone) VALUES (%s, %s);"
    cur.execute(insert_query, (name, phone))
    conn.commit()
    cur.close()
    print("Data inserted from console.")

def insert_data_csv(conn, csv_file):
    """
    Insert records into the PhoneBook table from a CSV file.
    The CSV file must contain two columns: name and phone.
    """
    cur = conn.cursor()
    try:
        with open(csv_file, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                # Skip rows that do not have at least two columns
                if len(row) < 2:
                    continue
                name, phone = row[0], row[1]
                insert_query = "INSERT INTO phonebook (name, phone) VALUES (%s, %s);"
                cur.execute(insert_query, (name, phone))
        conn.commit()
        print("Data inserted from CSV file.")
    except Exception as e:
        print("Error reading CSV file:", e)
    finally:
        cur.close()

def update_data(conn):
    """
    Update a record in the PhoneBook table.
    User can choose to update the name or the phone for a given record.
    """
    choice = input("Update name (n) or phone (p)? ")
    cur = conn.cursor()
    if choice.lower() == 'n':
        old_name = input("Enter current name: ")
        new_name = input("Enter new name: ")
        update_query = "UPDATE phonebook SET name = %s WHERE name = %s;"
        cur.execute(update_query, (new_name, old_name))
    elif choice.lower() == 'p':
        name = input("Enter name of the user to update phone: ")
        new_phone = input("Enter new phone number: ")
        update_query = "UPDATE phonebook SET phone = %s WHERE name = %s;"
        cur.execute(update_query, (new_phone, name))
    else:
        print("Invalid choice.")
        cur.close()
        return
    conn.commit()
    cur.close()
    print("Data updated.")

def query_data(conn):
    """
    Query data from the PhoneBook table.
    Provides options for querying all data, or filtering by name or phone.
    """
    cur = conn.cursor()
    print("Query Options:")
    print("1. All data")
    print("2. Filter by name")
    print("3. Filter by phone")
    choice = input("Enter your choice: ")
    if choice == '1':
        query = "SELECT * FROM phonebook;"
        cur.execute(query)
    elif choice == '2':
        name = input("Enter name to filter: ")
        query = "SELECT * FROM phonebook WHERE name ILIKE %s;"
        cur.execute(query, (f'%{name}%',))
    elif choice == '3':
        phone = input("Enter phone to filter: ")
        query = "SELECT * FROM phonebook WHERE phone ILIKE %s;"
        cur.execute(query, (f'%{phone}%',))
    else:
        print("Invalid choice.")
        cur.close()
        return
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()

def delete_data(conn):
    """
    Delete a record from the PhoneBook table based on the user's name.
    """
    name = input("Enter name to delete: ")
    cur = conn.cursor()
    delete_query = "DELETE FROM phonebook WHERE name = %s;"
    cur.execute(delete_query, (name,))
    conn.commit()
    cur.close()
    print("Data deleted for name:", name)

def main():
    """
    Main menu loop for the PhoneBook application.
    """
    conn = create_connection()
    create_table(conn)
    
    while True:
        print("\nPhoneBook Menu:")
        print("1. Insert data from console")
        print("2. Insert data from CSV file")
        print("3. Update data")
        print("4. Query data")
        print("5. Delete data")
        print("6. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            insert_data_console(conn)
        elif choice == '2':
            csv_file = input("Enter CSV file path: ")
            insert_data_csv(conn, csv_file)
        elif choice == '3':
            update_data(conn)
        elif choice == '4':
            query_data(conn)
        elif choice == '5':
            delete_data(conn)
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
    
    conn.close()

if __name__ == '__main__':
    main()