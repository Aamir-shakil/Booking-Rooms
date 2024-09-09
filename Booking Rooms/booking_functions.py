#File for all functions except main function 

import sqlite3 as db
from datetime import datetime
import pandas as pd
import main

connection = db.connect("bookings.db")
cursor = connection.cursor()



def get_rooms():
    data = pd.read_sql_query("SELECT * FROM Rooms", connection)
    print(data)
    cursor.execute('''SELECT * FROM Rooms''')
    return cursor.fetchall()

def create_room(room_reference, capacity, facilities, hire_price):
      # Check if the room_reference already exists
    cursor.execute('''SELECT * FROM Rooms WHERE room_reference=?''', (room_reference,))
    existing_room = cursor.fetchone()
    if existing_room:
        print("\nError: Room reference already exists. Please choose a unique room reference.\nReturning to Main Booking System...")
        main.main()  # return to main booking system if the room reference already exists
    
    # If the room_reference is unique data is inserted
    cursor.execute('''INSERT INTO Rooms (room_reference, capacity, facilities, hire_price) 
                VALUES (?, ?, ?, ?)''', (room_reference, capacity, facilities, hire_price))
    connection.commit()

def update_room(room_id, new_capacity, new_facilities, new_hire_price):
    cursor.execute('''UPDATE Rooms SET capacity=?, facilities=?, hire_price=? WHERE room_id=?''',
              (new_capacity, new_facilities, new_hire_price, room_id))
    connection.commit()
    if cursor.rowcount == 0:
        print("Sorry, no room available with this ID.")
    else:
        print("Room deleted successfully.")
        

def delete_room(room_id):
    cursor.execute('''DELETE FROM Rooms WHERE room_id=?''', (room_id,))
    connection.commit()
    if cursor.rowcount == 0:
        print("Sorry, no room available with this ID.")
    else:
        print("Room deleted successfully.")
        

def add_customer(first_name, surname, postcode, house_number, phone_number):
    cursor.execute('''INSERT INTO Customers (first_name, surname, postcode, house_number, phone_number) 
                VALUES (?, ?, ?, ?, ?)''', (first_name, surname, postcode, house_number, phone_number))
    connection.commit()

def get_customers():
    data = pd.read_sql_query("SELECT * FROM Customers", connection)
    print(data)
    cursor.execute('''SELECT * FROM Customers''')
    return cursor.fetchall()

def delete_customer(customer_id):
    cursor.execute('''DELETE FROM Customers WHERE customer_id=?''', (customer_id,))
    connection.commit()

def book_room(room_id, customer_id, booking_date, notes=''):
    cursor.execute('''SELECT * FROM Bookings WHERE room_id=? AND booking_date=?''', (room_id, booking_date))
    existing_booking = cursor.fetchone()
    if existing_booking:
        print("\nError: This room is already booked on the specified date. Please choose another date or room.\n")
        return
    cursor.execute('''INSERT INTO Bookings (room_id, customer_id, booking_date, notes) 
                VALUES (?, ?, ?, ?)''', (room_id, customer_id, booking_date, notes))
    connection.commit()
    print("Room booked successfully!")

def get_bookings_by_customer_name(name):
    data = pd.read_sql_query('''SELECT Bookings.booking_id, Customers.first_name, Customers.surname, Rooms.room_reference, Bookings.booking_date, Bookings.notes
                                FROM Bookings
                                INNER JOIN Customers ON Bookings.customer_id = Customers.customer_id
                                INNER JOIN Rooms ON Bookings.room_id = Rooms.room_id
                                WHERE first_name LIKE ? OR surname LIKE ?''', connection, params=('%' + name + '%', '%' + name + '%'))
    if data.empty:
        print("No bookings made under this Name.")
    
    else:
        print(data)
    return data

def get_bookings_on_date(date=None):
    data = pd.read_sql_query('''SELECT Bookings.booking_id, Customers.first_name, Customers.surname, Rooms.room_reference, Bookings.booking_date, Bookings.notes
                                FROM Bookings
                                INNER JOIN Customers ON Bookings.customer_id = Customers.customer_id
                                INNER JOIN Rooms ON Bookings.room_id = Rooms.room_id
                                WHERE booking_date=?''', connection, params=(date,))
    if data.empty:
        print("Sorry, no bookings made on this date.")
    else:
        print(data)
    return data

def delete_booking(booking_id):
    cursor.execute('''DELETE FROM Bookings WHERE booking_id=?''', (booking_id,))
    connection.commit()

def get_bookings():
    data = pd.read_sql_query('''SELECT Bookings.booking_id, Customers.first_name, Customers.surname, Rooms.room_reference, Bookings.booking_date, Bookings.notes
                                FROM Bookings
                                INNER JOIN Customers ON Bookings.customer_id = Customers.customer_id
                                INNER JOIN Rooms ON Bookings.room_id = Rooms.room_id''', connection)
    print(data)
    return data