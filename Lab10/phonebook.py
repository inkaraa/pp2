import psycopg2
import csv
def create_connection():
    conn=psycopg2.connect(
        host='localhost',
        database='phonebook',
        user='inkara',
        password=''
    )
    return conn
def create_table(conn):
    create_table_query="""
    CREATE TABLE IF NOT EXISTS phonebook(
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        phone VARCHAR(50) NOT NULL
    );
"""
    cur=conn.cursor()
    cur.execute(create_table_query)
    conn.commit()
    cur.close()
def insert_data_console(conn):
    name=input("Enter name: ")
    phone=input("Enter phone: ")
    cur=conn.cursor()
    insert_query="INSERT INTO phonebook (name , phone)  VALUES(%s , %s)"
    cur.execute(insert_query,(name,phone))
    conn.commit()
    cur.close()
    print("Data inserted.")
def insert_data_from_csv(conn, filename):
    try:
        cur = conn.cursor()
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader)  
            for row in reader:
                if len(row) >= 2: 
                    name, phone = row[0], row[1]
                    cur.execute(
                        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                        (name, phone)
                    )
        conn.commit()
        cur.close()
        print(f"Data from {filename} imported successfully.")
    except FileNotFoundError:
        print("File not found. Please check the filename.")
    except Exception as e:
        print(f"An error occurred: {e}")

def update_data(conn):
    print("\nUpdate options:")
    print("1. Update name")
    print("2. Update phone")
    choice = input("Enter your choice (1/2): ")
    
    if choice == '1':
        old_name = input("Enter current name: ")
        new_name = input("Enter new name: ")
        cur = conn.cursor()
        cur.execute(
            "UPDATE phonebook SET name = %s WHERE name = %s",
            (new_name, old_name)
        )
    elif choice == '2':
        name = input("Enter name: ")
        new_phone = input("Enter new phone: ")
        cur = conn.cursor()
        cur.execute(
            "UPDATE phonebook SET phone = %s WHERE name = %s",
            (new_phone, name)
        )
    else:
        print("Invalid choice.")
        return
    
    if cur.rowcount > 0:
        print("Data updated successfully.")
    else:
        print("No records found to update.")
    conn.commit()
    cur.close()

def query_data(conn):
    print("\nQuery options:")
    print("1. Get all contacts")
    print("2. Search by name")
    print("3. Search by phone")
    print("4. Search by partial name")
    choice = input("Enter your choice (1-4): ")
    
    cur = conn.cursor()
    
    if choice == '1':
        cur.execute("SELECT * FROM phonebook ORDER BY name")
    elif choice == '2':
        name = input("Enter name to search: ")
        cur.execute("SELECT * FROM phonebook WHERE name = %s", (name,))
    elif choice == '3':
        phone = input("Enter phone to search: ")
        cur.execute("SELECT * FROM phonebook WHERE phone = %s", (phone,))
    elif choice == '4':
        partial = input("Enter part of name to search: ")
        cur.execute("SELECT * FROM phonebook WHERE name LIKE %s", (f'%{partial}%',))
    else:
        print("Invalid choice.")
        return
    
    rows = cur.fetchall()
    if not rows:
        print("No records found.")
    else:
        print("\nID\tName\t\tPhone")
        print("-" * 30)
        for row in rows:
            print(f"{row[0]}\t{row[1]}\t{row[2]}")
    
    cur.close()

def delete_data(conn):
    print("\nDelete options:")
    print("1. Delete by name")
    print("2. Delete by phone")
    choice = input("Enter your choice (1/2): ")
    
    cur = conn.cursor()
    
    if choice == '1':
        name = input("Enter name to delete: ")
        cur.execute("DELETE FROM phonebook WHERE name = %s", (name,))
    elif choice == '2':
        phone = input("Enter phone to delete: ")
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
    else:
        print("Invalid choice.")
        return
    
    if cur.rowcount > 0:
        print(f"{cur.rowcount} record(s) deleted successfully.")
    else:
        print("No records found to delete.")
    conn.commit()
    cur.close()

def main():
    conn = create_connection()
    create_table(conn)
    
    while True:
        print("\nMENU")
        print("1. Insert data from console")
        print("2. Insert data from CSV file")
        print("3. Update data")
        print("4. Query data")
        print("5. Delete data")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            insert_data_console(conn)
        elif choice == '2':
            filename = input("Enter CSV filename: ")
            insert_data_from_csv(conn, filename)
        elif choice == '3':
            update_data(conn)
        elif choice == '4':
            query_data(conn)
        elif choice == '5':
            delete_data(conn)
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
    
    conn.close()

if __name__ == '__main__':
    main()
        