import sqlite3
from database import connect_db
import pandas as pd
from sklearn.linear_model import LinearRegression

DB_NAME = "data/messmind.db"


def train_model():

    conn = connect_db()

    query = """
    SELECT prepared, consumed
    FROM meals
    WHERE prepared > 0
    """

    data = pd.read_sql_query(query, conn)

    conn.close()

    if len(data) < 3:
        print("\nNot enough data for prediction.")
        print("Please enter at least 3 meal records.")
        return None

    X = data[["prepared"]]
    y = data["consumed"]

    model = LinearRegression()

    model.fit(X, y)

    return model


def predict_food():

    model = train_model()

    if model is None:
        return

    students = int(
        input("\nEnter expected number of students: ")
    )

    prediction = model.predict([[students]])

    predicted_consumption = int(prediction[0])

    buffer = int(predicted_consumption * 0.05)

    recommended = predicted_consumption + buffer

    print("\n========== FOOD PREDICTION ==========")

    print("Expected students:", students)
    print("Predicted consumption:", predicted_consumption)
    print("Safety buffer:", buffer)
    print("Recommended food preparation:", recommended)

    if recommended > students:
        print("\n⚠️ High food requirement predicted.")

    else:
        print("\n✅ Food quantity looks manageable.")