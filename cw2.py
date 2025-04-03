import csv
import sqlite3
#CLI=> Command Line Interface
# go to git bash
# git config-- global user.name "prason"
#git config-- global user.email "shresthaprason99@gmail.com"
#git init
#git status=> if you want to check what are the status of file
#git diff=> if you want to check what are the damages
#git add. ==> track files and folder
#git commit-m "Your message"
#copy paste git code from github



#1 chnage the code
#2 git add.
#3 git commit -m "Your message"
#4 git push origin
def create_connection():
    try:
        con = sqlite3.connect('users.sqlite3')
        return con
    except Exception as e:
        print(e)
        return None

INPUT_STRING = """
        Enter the option:
            1. CREATE TABLE
            2. DUMP users from csv INTO user TABLE
            3. ADD new user INTO users TABLE
            4. QUERY all users from TABLE
            5. QUERY user by id from TABLE
            6. QUERY specified no. of records from TABLE
            7. DELETE all users
            8. DELETE user by id
            9. UPDATE user
            10. EXIT
            """

def create_table(con):
    CREATE_USERS_TABLE_QUERY = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name CHAR(255) NOT NULL,
            last_name CHAR(255) NOT NULL,
            company_name CHAR(255) NOT NULL,
            address CHAR(255) NOT NULL,
            city CHAR(255) NOT NULL,
            county CHAR(255) NOT NULL,
            state CHAR(255) NOT NULL,
            zip REAL NOT NULL,
            phone1 CHAR(255) NOT NULL,
            phone2 CHAR(255) NOT NULL,
            email CHAR(255) NOT NULL,
            web TEXT
        );
    """
    cur = con.cursor()
    cur.execute(CREATE_USERS_TABLE_QUERY)
    con.commit()
    print('User table was created successfully.')

def read_csv():
    users = []
    try:
        with open('sample_users.csv', 'r') as f:
            data = csv.reader(f)
            next(data)  # Skip header row
            for user in data:
                users.append(tuple(user))
        return users
    except FileNotFoundError:
        print("Error: sample_users.csv not found")
        return []
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []

def insert_user(con, users):
    user_add_query = """
        INSERT INTO users (
            first_name,
            last_name,
            company_name,
            address,
            city,
            county,
            state,
            zip,
            phone1,
            phone2,
            email,
            web
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    try:
        cur = con.cursor()
        cur.executemany(user_add_query, users)
        con.commit()
        print(f'{len(users)} users were imported successfully')
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def select_all_users(con):
    try:
        cur = con.cursor()
        users = cur.execute('SELECT * FROM users;')
        for user in users:
            print(user)
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def select_users_by_id(con, user_id):
    try:
        cur = con.cursor()
        cur.execute('SELECT * FROM users WHERE id = ?;', (user_id,))
        user = cur.fetchone()
        if user:
            print(user)
        else:
            print(f"No user found with id {user_id}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def select_specified_no_of_users(con, no_of_users):
    try:
        cur = con.cursor()
        cur.execute('SELECT * FROM users LIMIT ?;', (no_of_users,))
        users = cur.fetchall()
        if users:
            for user in users:
                print(user)
        else:
            print("No users found or table is empty")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
def delete_users(con):
    cur=con.cursor()
    cur.execute('DELETE FROM users;')
    con.commit()
    print('All users were deleted successfully')
COLUMNS=(
    'first_name',
    'last_name',
    'company_name',
    'address',
    'city',
    'county',
    'state',
    'zip',
    'phone1',
    'phone2',
    'email',
    'web'
)
def update_user_id(con,user_id,column_name,column_value):
    cur=con.cursor()
    cur.execute(
        f'UPDATE user set{column_name}=? where id=?;',(column_value,user_id)
    )
    con.commit()
    print(
        f'[{column_name}] was updated with value [{column_value}]of user with id[{user_id}]'
    )

def main():
    con = create_connection()
    if con is None:
        return

    user_input = input(INPUT_STRING)
    
    if user_input == '1':
        create_table(con)
    elif user_input == '2':
        users = read_csv()
        if users:
            insert_user(con, users)
    elif user_input == '3':
        data=[]
        for column in COLUMNS:
            column_value=input(f'Enter the value of {column}:')
            data.append(column_value)
        insert_user(con,[tuple(data)])
    elif user_input == '4':
        select_all_users(con)
    elif user_input == '5':
        user_id = input("Enter user ID: ")
        select_users_by_id(con, user_id)
    elif user_input == '6':
        try:
            no_of_users = int(input("Enter number of records to query: "))
            if no_of_users > 0:
                select_specified_no_of_users(con, no_of_users)
            else:
                print("Please enter a positive number")
        except ValueError:
            print("Please enter a valid number")
    elif user_input == '7':
        confirmation=input('Are you sure? Please type y to continue')
        if confirmation=='y':
            delete_users(con)
    elif user_input == '8':
        user_id=input('Enter your id:')
        if user_id.isnumeric():
            delete_users(con)
    elif user_input == '9':
        user_id=input("Enter the id of user")
        if user_id.isnumeric():
            column_name=input(
                f"Enter the column you want to edit.Please make sure column is with in{COLUMNS}:"
            )
            if column_name in COLUMNS:
                column_value=input(f'Enter the value of {column_name}')
                update_user_id(con,user_id,column_name,column_value) 
    elif user_input == '10':
        print("Exiting program...")
    else:
        print("Invalid option selected")

    con.close()
   
main()
