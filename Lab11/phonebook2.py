import psycopg2
import json 

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
    CREATE TABLE IF NOT EXISTS phonebook2(
         id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        surname VARCHAR(100) NOT NULL,
        phone VARCHAR(50) NOT NULL
    );
"""
    cur=conn.cursor()
    cur.execute(create_table_query)
    conn.commit()
    cur.close()

def call_search_by_pattern(conn):
    pattern = input("Enter pattern to search: ")
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_records(%s);", (pattern,)) # procedure "search_records(%s)"
    rows = cur.fetchall()
    
    if rows:
        print("\nMatching Records:")
        for row in rows:
            print(row)
    else:
        print("\nNo records found.")
    
    cur.close()


def call_insert_or_update_user(conn):
    name = input("Enter name: ")
    surname = input("Enter surname: ")
    phone = input("Enter phone: ")
    cur = conn.cursor()
    cur.execute("CALL insert_or_update_user(%s, %s, %s);", (name, surname, phone))
    conn.commit()
    cur.close()
    print("User inserted or updated.")

def call_insert_bulk_users(conn):
    print("Enter users as JSON array of arrays (e.g. [[\"name1\", \"surname1\", \"+77777777777\"], ...]):")
    raw = input(">> ")
    users = json.loads(raw)
    cur = conn.cursor()
    cur.execute("CALL insert_bulk_users(%s);", [json.dumps(users)])
    conn.commit()
    cur.close()
    print("Bulk insert completed.")

def call_paginated_query(conn):
    page = 1
    page_size = 5
    while True:
        cur = conn.cursor()
        cur.execute("SELECT * FROM paginated_query(%s, %s);", (page, page_size))
        rows = cur.fetchall()
        cur.close()

        if not rows:
            print("No more data.")
            break

        print(f"\n— Page {page} —")
        print("ID\tName\tSurname\tPhone")
        print("-" * 40)
        for row in rows:
            print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}")

        command = input("← Назад (a), → Вперёд (d), Выход (q): ").strip().lower()
        if command == "d":
            page += 1
        elif command == "a" and page > 1:
            page -= 1
        elif command == "q":
            break

def call_delete_user(conn):
    identifier = input("Enter name or phone to delete: ")
    cur = conn.cursor()
    cur.execute("CALL delete_user(%s);", (identifier,))
    conn.commit()
    cur.close()
    print("User deleted if existed.")

def main():
    conn = create_connection()
    create_table(conn)
    
    while True:
        print("\nMENU")
        print("1. Get records by pattern")
        print("2. Insert or update a user")
        print("3. Insert multiple data (json)")
        print("4. Paginated querying")
        print("5. Delete User by Name or Phonea")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            call_search_by_pattern(conn)
        elif choice == '2':
            call_insert_or_update_user(conn)
        elif choice == '3':
            call_insert_bulk_users(conn)
        elif choice == '4':
            call_paginated_query(conn)
        elif choice == '5':
            call_delete_user(conn)
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
    
    conn.close()

if __name__ == '__main__':
    main()
        