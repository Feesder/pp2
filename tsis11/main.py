import psycopg2
import csv

conn = psycopg2.connect(
    host="localhost",
    dbname="tsis_nine",
    user="yerdos",
    password="Xad7rZbD863nfUAGTWb5S6p3y6wyXG44",
    port="5432"
)
cur = conn.cursor()


def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            phone VARCHAR(20)
        );
    """)

    # Create the function to search by pattern
    cur.execute("""
        CREATE OR REPLACE FUNCTION search_by_pattern(pattern TEXT)
        RETURNS TABLE(id INTEGER, first_name VARCHAR, phone VARCHAR) AS $$
        BEGIN
            RETURN QUERY 
            SELECT phonebook.id, phonebook.first_name, phonebook.phone 
            FROM phonebook 
            WHERE phonebook.first_name ILIKE '%' || pattern || '%'
               OR phonebook.phone ILIKE '%' || pattern || '%';
        END;
        $$ LANGUAGE plpgsql;
    """)

    # Create procedure to insert or update user
    cur.execute("""
        CREATE OR REPLACE PROCEDURE upsert_user(
            user_name VARCHAR,
            user_phone VARCHAR
        )
        AS $$
        BEGIN
            IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = user_name) THEN
                UPDATE phonebook SET phone = user_phone WHERE first_name = user_name;
            ELSE
                INSERT INTO phonebook (first_name, phone) VALUES (user_name, user_phone);
            END IF;
        END;
        $$ LANGUAGE plpgsql;
    """)

    # Create function for pagination
    cur.execute("""
        CREATE OR REPLACE FUNCTION get_paginated_data(
            lim INTEGER,
            offs INTEGER
        )
        RETURNS TABLE(id INTEGER, first_name VARCHAR, phone VARCHAR) AS $$
        BEGIN
            RETURN QUERY 
            SELECT phonebook.id, phonebook.first_name, phonebook.phone 
            FROM phonebook 
            ORDER BY id
            LIMIT lim OFFSET offs;
        END;
        $$ LANGUAGE plpgsql;
    """)

    # Create procedure to delete by username or phone
    cur.execute("""
        CREATE OR REPLACE PROCEDURE delete_by_username_or_phone(
            search_value VARCHAR
        )
        AS $$
        BEGIN
            DELETE FROM phonebook 
            WHERE first_name = search_value OR phone = search_value;
        END;
        $$ LANGUAGE plpgsql;
    """)

    conn.commit()


def insert_from_csv(filename):
    try:
        with open(filename, newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
                            (row[0].strip(), row[1].strip()))
        conn.commit()
        print("Data inserted successfully")
    except FileNotFoundError:
        print("File not founded")


def insert_from_console():
    name = input("Enter first name: ")
    phone = input("Enter phone: ")
    cur.execute("CALL upsert_user(%s, %s)", (name, phone))
    conn.commit()
    print("User added/updated successfully")


def update_data():
    enter = input("What you want to update: 'name' or 'phone'? ").strip().lower()
    if enter == "name":
        old_name = input("Enter current name: ")
        new_name = input("Enter new name: ")
        cur.execute("SELECT * FROM phonebook WHERE first_name = %s", (old_name,))
        user = cur.fetchone()
        if user:
            cur.execute("UPDATE phonebook SET first_name = %s WHERE first_name = %s", (new_name, old_name))
            conn.commit()
            print("Data is updated.")
        else:
            print("No such user found.")
    elif enter == "phone":
        name = input("Enter name to change phone: ")
        new_phone = input("Enter new phone: ")
        cur.execute("CALL upsert_user(%s, %s)", (name, new_phone))
        conn.commit()
        print("Phone updated/inserted.")
    else:
        print("Wrong choice.")


def query_data():
    print("\nSelect request type:")
    print("1. Show all users")
    print("2. Search by pattern (name or phone)")
    print("3. Get paginated data")

    choice = input("Your choice (1-3): ").strip()

    if choice == "1":
        cur.execute("SELECT * FROM phonebook")
    elif choice == "2":
        pattern = input("Enter search pattern: ")
        cur.execute("SELECT * FROM search_by_pattern(%s)", (pattern,))
    elif choice == "3":
        limit = input("Enter limit: ")
        offset = input("Enter offset: ")
        cur.execute("SELECT * FROM get_paginated_data(%s, %s)", (limit, offset))
    else:
        print("Wrong choice.")
        return

    rows = cur.fetchall()
    if rows:
        print("\nResults:")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
    else:
        print("No results found.")


def delete_data():
    value = input("Enter name or phone to delete: ")
    cur.execute("CALL delete_by_username_or_phone(%s)", (value,))
    conn.commit()
    print("Deletion completed")


def insert_many_users():
    print("Enter users in format 'name,phone'. Enter 'done' when finished.")
    incorrect_entries = []

    while True:
        entry = input("Enter name and phone (or 'done'): ").strip()
        if entry.lower() == 'done':
            break

        if ',' not in entry:
            print("Invalid format. Use 'name,phone'")
            incorrect_entries.append(entry)
            continue

        name, phone = entry.split(',', 1)
        name = name.strip()
        phone = phone.strip()

        # Simple phone validation - adjust as needed
        if not phone.isdigit() or len(phone) < 5:
            print(f"Invalid phone number: {phone}")
            incorrect_entries.append(entry)
            continue

        try:
            cur.execute("CALL upsert_user(%s, %s)", (name, phone))
            conn.commit()
        except Exception as e:
            print(f"Error inserting {name}: {e}")
            incorrect_entries.append(entry)

    if incorrect_entries:
        print("\nIncorrect entries:")
        for entry in incorrect_entries:
            print(entry)


if __name__ == "__main__":
    create_table()
    while True:
        print("\nChoose one of the variations:")
        print("1 - insert from console")
        print("2 - insert from csv")
        print("3 - update values")
        print("4 - query data")
        print("5 - delete data")
        print("6 - insert many users")
        print("7 - exit")

        try:
            nado = int(input("Input number: "))
        except ValueError:
            print("Please enter a valid number")
            continue

        if nado == 1:
            insert_from_console()
        elif nado == 2:
            insert_from_csv("./data.csv")
        elif nado == 3:
            update_data()
        elif nado == 4:
            query_data()
        elif nado == 5:
            delete_data()
        elif nado == 6:
            insert_many_users()
        elif nado == 7:
            break
        else:
            print("Invalid choice")

    cur.close()
    conn.close()