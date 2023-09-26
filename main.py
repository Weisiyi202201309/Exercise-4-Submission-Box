import sqlite3


# Function to create the database and tables
def create_database():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Books (
        BookID TEXT PRIMARY KEY,
        Title TEXT,
        Author TEXT,
        ISBN TEXT,
        Status TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
        UserID TEXT PRIMARY KEY,
        Name TEXT,
        Email TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Reservations (
        ReservationID INTEGER PRIMARY KEY AUTOINCREMENT,
        BookID TEXT,
        UserID TEXT,
        ReservationDate TEXT,
        FOREIGN KEY (BookID) REFERENCES Books(BookID),
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    )''')

    conn.commit()
    conn.close()


# Function to add a new book to the database
def add_book():
    book_id = input('Enter Book ID: ')
    title = input('Enter Title: ')
    author = input('Enter Author: ')
    isbn = input('Enter ISBN: ')
    status = input('Enter Status: ')

    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO Books (BookID, Title, Author, ISBN, Status) VALUES (?, ?, ?, ?, ?)',
                   (book_id, title, author, isbn, status))

    conn.commit()
    conn.close()

    print('Book added successfully.')


# Function to find a book's details based on BookID
def find_book_details():
    book_id = input('Enter Book ID: ')

    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status,
                      Users.Name, Users.Email, Reservations.ReservationDate
                      FROM Books
                      LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                      LEFT JOIN Users ON Reservations.UserID = Users.UserID
                      WHERE Books.BookID = ?''', (book_id,))

    result = cursor.fetchone()

    if result is None:
        print('Book not found.')
    else:
        book_details = {
            'BookID': result[0],
            'Title': result[1],
            'Author': result[2],
            'ISBN': result[3],
            'Status': result[4]
        }

        if result[5] is not None:
            user_details = {
                'Name': result[5],
                'Email': result[6]
            }
            reservation_date = result[7]
            print('Book details:')
            print(book_details)
            print('Reserved by:')
            print(user_details)
            print('Reservation Date:', reservation_date)
        else:
            print('Book details:')
            print(book_details)
            print('Book is not reserved.')

    conn.close()


# Function to find a book's reservation status based on BookID, Title, UserID, or ReservationID
def find_reservation_status():
    search_text = input('Enter Book ID, Title, UserID, or ReservationID: ')

    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    if search_text.startswith('LB'):
        cursor.execute('SELECT BookID, Status FROM Books WHERE BookID = ?', (search_text,))
        result = cursor.fetchone()

        if result is None:
            print('Book not found.')
        else:
            print('BookID:', result[0])
            print('Reservation Status:', result[1])

    elif search_text.startswith('LU'):
        cursor.execute('''SELECT Books.BookID, Books.Status
                          FROM Books
                          INNER JOIN Reservations ON Books.BookID = Reservations.BookID
                          WHERE Reservations.UserID = ?''', (search_text,))
        results = cursor.fetchall()

        if len(results) == 0:
            print('User has not reserved any books.')

        for result in results:
            print('BookID:', result[0])
            print('Reservation Status:', result[1])

    elif search_text.startswith('LR'):
        cursor.execute('''SELECT Books.BookID, Books.Status
                          FROM Books
                          INNER JOIN Reservations ON Books.BookID = Reservations.BookID
                          WHERE Reservations.ReservationID = ?''', (search_text,))
        result = cursor.fetchone()

        if result is None:
            print('Reservation not found.')
        else:
            print('BookID:', result[0])
            print('Reservation Status:', result[1])

    else:
        cursor.execute('''SELECT Books.BookID, Books.Title, Books.Status,
                          Users.Name, Users.Email
                          FROM Books
                          LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                          LEFT JOIN Users ON Reservations.UserID = Users.UserID
                          WHERE Books.Title = ?''', (search_text,))
        results = cursor.fetchall()

        if len(results) == 0:
            print('Book not found.')

        for result in results:
            print('BookID:', result[0])
            print('Title:', result[1])
            print('Reservation Status:', result[2])
            if result[3] is not None:
                print('Reserved by:')
                print('Name:', result[3])
                print('Email:', result[4])

    conn.close()


# Function to retrieve all the books in the database
def retrieve_all_books():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status,
                      Users.Name, Users.Email, Reservations.ReservationDate
                      FROM Books
                      LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                      LEFT JOIN Users ON Reservations.UserID = Users.UserID''')

    results = cursor.fetchall()

    if len(results) == 0:
        print('No books found in the database.')

    for result in results:
        print('BookID:', result[0])
        print('Title:', result[1])
        print('Author:', result[2])
        print('ISBN:', result[3])
        print('Status:', result[4])
        if result[5] is not None:
            print('Reserved by:')
            print('Name:', result[5])
            print('Email:', result[6])
            print('Reservation Date:', result[7])
        print('-----------------------')

    conn.close()


# Function to modify/update book details based on BookID
def modify_book_details():
    book_id = input('Enter Book ID: ')

    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Books WHERE BookID = ?', (book_id,))
    result = cursor.fetchone()

    if result is None:
        print('Book not found.')
    else:
        print('Current Book Details:')
        print('BookID:', result[0])
        print('Title:', result[1])
        print('Author:', result[2])
        print('ISBN:', result[3])
        print('Status:', result[4])

        choice = input('What details do you want to modify (Title, Author, ISBN, Status)? ')
        new_value = input('Enter new value: ')

        if choice.lower() == 'status':
            cursor.execute('UPDATE Books SET Status = ? WHERE BookID = ?', (new_value, book_id))
            cursor.execute('UPDATE Reservations SET BookID = ? WHERE BookID = ?', (new_value, book_id))
            print('Book status updated successfully.')
        else:
            cursor.execute('UPDATE Books SET ' + choice.capitalize() + ' = ? WHERE BookID = ?', (new_value, book_id))
            print('Book details updated successfully.')

    conn.commit()
    conn.close()

# Function to add a new user to the database
def add_user():
    user_id = input('Enter User ID: ')
    name = input('Enter Name: ')
    email = input('Enter Email: ')

    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO Users (UserID, Name, Email) VALUES (?, ?, ?)', (user_id, name, email))

    conn.commit()
    conn.close()

    print('User added successfully.')

# Function to reserve a book
def reserve_book():
    book_id = input('Enter Book ID: ')
    user_id = input('Enter User ID: ')
    reservation_date = input('Enter Reservation Date (YYYY-MM-DD): ')

    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Books WHERE BookID = ?', (book_id,))
    book_result = cursor.fetchone()

    if book_result is None:
        print('Book not found.')
    else:
        cursor.execute('SELECT * FROM Users WHERE UserID = ?', (user_id,))
        user_result = cursor.fetchone()

        if user_result is None:
            print('User not found.')
        else:
            cursor.execute('INSERT INTO Reservations (BookID, UserID, ReservationDate) VALUES (?, ?, ?)',
                           (book_id, user_id, reservation_date))

            conn.commit()
            print('Book reserved successfully.')

    conn.close()


# Function to delete a book based on its BookID
def delete_book():
    book_id = input('Enter Book ID: ')

    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Books WHERE BookID = ?', (book_id,))
    result = cursor.fetchone()

    if result is None:
        print('Book not found.')
    else:
        cursor.execute('DELETE FROM Books WHERE BookID = ?', (book_id,))
        cursor.execute('DELETE FROM Reservations WHERE BookID = ?', (book_id,))

        print('Book deleted successfully.')

    conn.commit()
    conn.close()



# Main program loop
def main():
    create_database()

    while True:
        print('-----------------------')
        print('Library Management System')
        print('-----------------------')
        print('1. Add a new book')
        print('2. Find a book\'s details')
        print('3. Find a book\'s reservation status')
        print('4. Find all the books')
        print('5. Modify/update book details')
        print('6. Delete a book')
        print('7. Add a new user')  # Added option to add a new user
        print('8. Reserve a book')  # Added option to reserve a book
        print('9. Exit')
        print('-----------------------')

        choice = input('Enter your choice (1-9): ')

        if choice == '1':
            add_book()
        elif choice == '2':
            find_book_details()
        elif choice == '3':
            find_reservation_status()
        elif choice == '4':
            retrieve_all_books()
        elif choice == '5':
            modify_book_details()
        elif choice == '6':
            delete_book()
        elif choice == '7':
            add_user()  # Added a new function call for adding a new user
        elif choice == '8':
            reserve_book()  # Added a new function call for reserving a book
        elif choice == '9':
            break
        else:
            print('Invalid choice. Please try again.')

    print('Exiting...')


if __name__ == '__main__':
    main()
