import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime



st.set_page_config(page_title="MessMind Prototype", page_icon="🍽️", layout="wide")


def get_conn():
    conn = sqlite3.connect("messmind.db", check_same_thread=False)
    conn.execute("""CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT, student_id TEXT, meal TEXT, status TEXT, date TEXT)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT, meal TEXT, category TEXT, rating INTEGER, comment TEXT, status TEXT)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS rescue (
        id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT, qty TEXT, safe_window TEXT, status TEXT)""")
    conn.commit()
    return conn

conn = get_conn()

st.title("🍽️ MessMind — Smart Mess & Food Waste Prototype")
st.caption("Eat Smart. Manage Smart. Waste Less. | Connected to messmind.db")

tab1, tab2, tab3, tab4 = st.tabs([
    "🎓 Student Portal",
    "📊 Manager & Prediction",
    "🤝 Food Rescue",
    "📁 Reports & Database"
])


with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Daily Meal Check-In")
        student_id = st.text_input("Student Roll No.", placeholder="e.g., CS202604")
        meal = st.selectbox("Select Meal", ["Breakfast", "Lunch", "Dinner"])
        attending = st.radio("Will you eat this meal?", ["Yes (Attending)", "No (Skipping)"], horizontal=True)
        if st.button("Confirm Attendance", type="primary"):
            conn.execute("INSERT INTO attendance (student_id, meal, status, date) VALUES (?, ?, ?, ?)",
                         (student_id or "Anonymous", meal, attending, datetime.now().strftime("%Y-%m-%d")))
            conn.commit()
            st.success(f"Recorded: {meal} -> {attending}")

    with col2:
        st.subheader("Submit Feedback / Issue")
        fb_meal = st.selectbox("Meal Session", ["Breakfast", "Lunch", "Dinner"], key="fb_meal")
        fb_cat = st.selectbox("Issue Category", ["Taste & Quality", "Hygiene", "Portion / Shortage", "Suggestion"])
        fb_rating = st.slider("Rating (1 = Poor, 5 = Excellent)", 1, 5, 4)
        fb_comment = st.text_area("Comments")
        if st.button("Submit Feedback"):
            conn.execute("INSERT INTO feedback (meal, category, rating, comment, status) VALUES (?, ?, ?, ?, ?)",
                         (fb_meal, fb_cat, fb_rating, fb_comment, "Open"))
            conn.commit()
            st.success("Feedback logged into messmind.db!")

with tab2:
    st.subheader("Demand Prediction Engine (prediction.py)")
    c1, c2, c3 = st.columns(3)
    day = c1.selectbox("Day of Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    pred_meal = c2.selectbox("Meal", ["Breakfast", "Lunch", "Dinner"], key="pred_meal")
    event = c3.selectbox("Campus Factor", ["Regular Day", "Exam Week (+8%)", "Weekend / Holiday (-25%)"])

    base = {"Breakfast": 290, "Lunch": 350, "Dinner": 330}[pred_meal]
    if day == "Wednesday":
        base += 25
    if day in ["Saturday", "Sunday"]:
        base -= 45
    if "Exam" in event:
        base = int(base * 1.08)
    elif "Holiday" in event:
        base = int(base * 0.75)

    st.metric(label=f"Recommended Preparation ({day} - {pred_meal})", value=f"{base} Plates", delta="-8% expected waste")

    st.divider()
    st.subheader("Live Student Feedback Log")
    fb_df = pd.read_sql_query("SELECT * FROM feedback ORDER BY id DESC", conn)
    st.dataframe(fb_df, use_container_width=True)

with tab3:
    st.subheader("Surplus Food Rescue Log (rescue.py)")
    with st.form("rescue_form"):
        item = st.text_input("Surplus Food Item(s)", placeholder="e.g., Dal Tadka & Steamed Rice")
        qty = st.text_input("Quantity", placeholder="e.g., 7.5 kg (~30 servings)")
        window = st.text_input("Safe Consume-By Window", placeholder="e.g., Within 3 hours (by 5:30 PM)")
        submitted = st.form_submit_button("Log Safe Surplus Batch")
        if submitted and item:
            conn.execute("INSERT INTO rescue (item, qty, safe_window, status) VALUES (?, ?, ?, ?)",
                         (item, qty, window, "Available for NGO Pickup"))
            conn.commit()
            st.success("Surplus batch logged!")

    rescue_df = pd.read_sql_query("SELECT * FROM rescue ORDER BY id DESC", conn)
    st.dataframe(rescue_df, use_container_width=True)

with tab4:
    st.subheader("MessMind Summary & Export (report.py)")
    att_df = pd.read_sql_query("SELECT * FROM attendance ORDER BY id DESC", conn)
    st.write("**Meal Check-In Records:**")
    st.dataframe(att_df, use_container_width=True)

    if not att_df.empty:
        csv = att_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Attendance Report (CSV)", csv, "messmind_report.csv", "text/csv")