import sqlite3
from database import connect_db
DB_NAME = "data/messmind.db"


def waste_report():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        SUM(prepared),
        SUM(consumed),
        SUM(wasted)
    FROM meals
    """)

    result = cursor.fetchone()

    conn.close()

    prepared = result[0] or 0
    consumed = result[1] or 0
    wasted = result[2] or 0

    print("\n========== FOOD WASTE REPORT ==========")

    print("Total food prepared :", prepared)
    print("Total food consumed :", consumed)
    print("Total food wasted   :", wasted)

    if prepared > 0:

        percentage = (wasted / prepared) * 100

        print(
            "Waste percentage    :",
            round(percentage, 2),
            "%"
        )

    print("========================================")


def menu_wise_report():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT menu, SUM(prepared), SUM(consumed), SUM(wasted)
    FROM meals
    GROUP BY menu
    """)

    records = cursor.fetchall()

    conn.close()

    print("\n========== MENU WISE WASTE ==========")

    for row in records:

        print(
            f"Menu: {row[0]} | "
            f"Prepared: {row[1]} | "
            f"Consumed: {row[2]} | "
            f"Wasted: {row[3]}"
        )