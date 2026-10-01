import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR,"messmind.db")



def connect_db():
    
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS meals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        meal_type TEXT,
        menu TEXT,
        prepared INTEGER,
        consumed INTEGER,
        wasted INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        attendance INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rescued_food (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        food_name TEXT,
        quantity INTEGER,
        student_name TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_meal():
    conn = connect_db()
    cursor = conn.cursor()

    date = input("Enter date (YYYY-MM-DD): ")
    meal_type = input("Enter meal type (Breakfast/Lunch/Dinner): ")
    menu = input("Enter menu: ")

    prepared = int(input("Food prepared: "))
    consumed = int(input("Food consumed: "))

    wasted = prepared - consumed

    cursor.execute("""
    INSERT INTO meals
    (date, meal_type, menu, prepared, consumed, wasted)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (date, meal_type, menu, prepared, consumed, wasted))

    conn.commit()
    conn.close()

    print("\nMeal record added successfully!")
    print("Food wasted:", wasted)


def show_meals():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM meals")

    records = cursor.fetchall()

    print("\n========== MEAL RECORDS ==========")

    if not records:
        print("No records found.")

    for row in records:
        print(
            f"ID: {row[0]} | Date: {row[1]} | "
            f"{row[2]} | {row[3]} | "
            f"Prepared: {row[4]} | "
            f"Consumed: {row[5]} | "
            f"Wasted: {row[6]}"
        )

    conn.close()