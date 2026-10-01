import sqlite3
from datetime import date
from database import connect_db

DB_NAME = "data/messmind.db"


def add_surplus_food():

    food = input("Enter food name: ")
    quantity = int(input("Enter available portions: "))

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO rescued_food
    (date, food_name, quantity, student_name, status)
    VALUES (?, ?, ?, ?, ?)
    """, (
        str(date.today()),
        food,
        quantity,
        "",
        "AVAILABLE"
    ))

    conn.commit()
    conn.close()

    print("\n♻️ Surplus food added successfully!")


def show_surplus():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM rescued_food
    WHERE status = 'AVAILABLE'
    """)

    records = cursor.fetchall()

    print("\n========== AVAILABLE FOOD ==========")

    if not records:
        print("No surplus food available.")

    for row in records:
        print(
            f"ID: {row[0]} | "
            f"Food: {row[2]} | "
            f"Quantity: {row[3]} | "
            f"Status: {row[5]}"
        )

    conn.close()


def reserve_food():

    show_surplus()

    food_id = int(
        input("\nEnter food ID to reserve: ")
    )

    student = input("Enter student name: ")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT quantity
    FROM rescued_food
    WHERE id = ? AND status = 'AVAILABLE'
    """, (food_id,))

    record = cursor.fetchone()

    if record is None:
        print("Food not available.")
        conn.close()
        return

    if record[0] <= 0:
        print("No portions remaining.")
        conn.close()
        return

    cursor.execute("""
    UPDATE rescued_food
    SET quantity = quantity - 1,
        student_name = ?,
        status = CASE
            WHEN quantity - 1 = 0 THEN 'RESCUED'
            ELSE 'AVAILABLE'
        END
    WHERE id = ?
    """, (student, food_id))

    conn.commit()
    conn.close()

    print("\n✅ Food successfully reserved!")