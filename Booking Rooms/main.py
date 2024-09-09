import sqlite3 as db
from datetime import datetime
import pandas as pd
import booking_functions

connection = db.connect("bookings.db")

cursor = connection.cursor()

cursor.execute('''
               DROP TABLE IF EXISTS ROOMS
               ''')
cursor.execute('''
               DROP TABLE IF EXISTS CUSTOMERS
               ''')
cursor.execute('''
               DROP TABLE IF EXISTS Bookings
               ''')
# Creating tables for the database
cursor.execute('''CREATE TABLE IF NOT EXISTS Rooms (
    room_id INTEGER PRIMARY KEY,
    room_reference TEXT UNIQUE,
    capacity INTEGER,
    facilities TEXT,
    hire_price REAL
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT,
    surname TEXT,
    postcode TEXT,
    house_number INT,
    phone_number NUMERIC
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Bookings (
    booking_id INTEGER PRIMARY KEY,
    room_id INTEGER,
    customer_id INTEGER,
    booking_date NUMERIC,
    notes TEXT,
    FOREIGN KEY(room_id) REFERENCES Rooms(room_id),
    FOREIGN KEY(customer_id) REFERENCES Customers(customer_id)
)''')

connection.commit()

# data for rooms inserted into rooms table
rooms_data = [
    ("Room1", 50, "Projector room", 100.00),
    ("Room2", 30, "dance studio", 80.00),
    ("Room3", 20, "dining room", 60.00),
    ("Room4", 40, "Games room", 90.00)
]

cursor.executemany('''INSERT INTO Rooms (room_reference, capacity, facilities, hire_price) 
                VALUES (?, ?, ?, ?)''', rooms_data)
connection.commit()

# sample of customers 
sample_customers = [
    ("Brad", "Pitt", "ol4 2rj", "10", "07503819870"),
    ("Aamir", "Shakil", "ol4 2gh", "13", "07303818976"),
    ("Sharukh", "Khan", "kl1 2mp", "26", "07203818977"),
    ("Spongebob", "Squarepants", "mp3 6hu", "81", "07903818369")
]

for customer_data in sample_customers:
    cursor.execute('''INSERT INTO Customers (first_name, surname, postcode, house_number, phone_number) 
                VALUES (?, ?, ?, ?, ?)''', customer_data)

connection.commit()

# Sample bookings
sample_bookings = [
    (1, 4, '2024-05-10', 'add an extra table'),
    (3, 2, '2024-05-12', 'Bring projector'),
    (4, 3, '2024-05-15', 'Birthday party bring cake'),
]

for booking_data in sample_bookings:
    cursor.execute('''INSERT INTO Bookings (room_id, customer_id, booking_date, notes) 
                VALUES (?, ?, ?, ?)''', booking_data)

connection.commit()

    
# User Interface(Main menu)
def main():
    print("Welcome to the Room Booking System")
    while True:
        print("\nSelect one of the options below to proceed:")
        print("1. View Rooms")
        print("2. Book Room")
        print("3. Search Bookings by Customer Name")
        print("4. Search Bookings by Date")
        print("5. Exit")
        print("6. Delete room")
        print("7. Create a room")
        print("8. Add a customer")
        print("9. View Customers")
        print("10. Update Room")
        print("11. View Bookings")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("\nRooms:")
            booking_functions.get_rooms()
            
        elif choice == '2':
            print("\nRooms:")
            booking_functions.get_rooms()
            print("Customers:")
            booking_functions.get_customers()
            room_id = input("Enter Room ID: ")
            customer_id = input("Enter Customer ID: ")
            booking_date = input("Enter Booking Date (YYYY-MM-DD): ")
            notes = input("Enter Additional Notes/Requests: ")
            booking_functions.book_room(room_id, customer_id, booking_date, notes)
        
        elif choice == '3':
            name = input("Enter Customer Name: ")
            print("\nBookings:")
            booking_functions.get_bookings_by_customer_name(name)
        
        elif choice == '4':
            date = input("Enter Date in the format (YYYY-MM-DD,): ")
            print("\nBookings on", date)
            booking_functions.get_bookings_on_date(date)

        elif choice == '5':
            print("Thank you for using the Room Booking System!")
            connection.close()  # Closes the database connection before exiting the program
            break

        elif choice == '6':
            print("\nRooms:")
            booking_functions.get_rooms()
            print("\n")
            room_id = input("Enter the room id of the room you want to delete")
            booking_functions.delete_room(room_id)
            
        elif choice == '7':
            room_reference = input("Enter unique Room Reference ")
            capacity = input("Enter Capacity of Room ")
            try:
                capacity = float(capacity)
            except:
                print("\nError type as a number only,e.g, 23.0\nReturning to Main Booking system...")
                continue
            facilities = input("Enter Facilities of room ")
            hire_price = input("Enter the Hire Price ")
            try:
                hire_price = float(hire_price)  # Convert hire price to float
            except ValueError:
                print("\nError: Please Type as number only for hire price hire price.\nReturning to Main Booking system...")
                continue
            booking_functions.create_room(room_reference, capacity, facilities, hire_price)
            print("Room created successfully!")
        
        elif choice == '8':
            first_name = input("Enter Customer's first name:")
            surname = input("Enter Customer's Surname:")
            postcode = input("Enter Customer's Postcode:")
            house_number = input("Enter Customer's House Number:")
            phone_number = input("Enter Customer's Phone Number ")
            booking_functions.add_customer(first_name, surname, postcode, house_number, phone_number)
            print("Customer added successfully!")

        elif choice == '9':
            print("Customers:")
            booking_functions.get_customers()
            
        elif choice == '10':
            print("\nRooms:")
            booking_functions.get_rooms()  
            room_id = input("\nEnter the Room id of the room you want to update: ")
            new_capacity = input("Enter New Capacity of room: ")
            new_facilities = input("Enter New Facilities of room: ")
            new_hire_price = input("Enter New Hire Price for the room: ")
            booking_functions.update_room(room_id, new_capacity, new_facilities, new_hire_price)

        elif choice == '11':
            print("Bookings: ")
            booking_functions.get_bookings()
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
