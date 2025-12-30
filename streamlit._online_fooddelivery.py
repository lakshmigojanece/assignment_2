
import streamlit as st
import mysql.connector
import pandas as pd

st.title("🍔 ONLINE FOOD DELIVERY INSIGHTS USING MYSQL")
st.header("📊 DASHBOARD")

st.subheader("Select any problem statement (1–7) to run the SQL queries")


option = st.selectbox(
    "Select Analysis",
    (
        "Total Orders",
        "Total Revenue",
        "Average Order Value",
        "Average Delivery Time",
        "Cancellation Rate",
        "Average Delivery Rating",
        "Profit Margin %"
    )
)

# DB connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="food_delivery_db"
)
cursor = db.cursor(dictionary=True)

# Queries
queries = {
    "Total Orders": """
        SELECT Order_Status,
               COUNT(*) AS total_orders
        FROM online_food_delivery
        GROUP BY Order_Status;
    """,

    "Total Revenue": """
        SELECT Order_Status,
               ROUND(SUM(Final_Amount),2) AS total_revenue
        FROM online_food_delivery
        GROUP BY Order_Status;
    """,

    "Average Order Value": """
        SELECT Order_Status,
               ROUND(AVG(Final_Amount),2) AS avg_order_value
        FROM online_food_delivery
        GROUP BY Order_Status;
    """,

    "Average Delivery Time": """
        SELECT Order_Status,
               ROUND(AVG(Delivery_Time_Min),2) AS avg_delivery_time
        FROM online_food_delivery
        GROUP BY Order_Status;
    """,

    "Cancellation Rate": """
        SELECT 
        ROUND(
            (SUM(CASE WHEN Order_Status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0) 
            / COUNT(*), 2
        ) AS cancellation_rate
        FROM online_food_delivery;
    """,

    "Average Delivery Rating": """
        SELECT Order_Status,
               ROUND(AVG(Delivery_Rating),2) AS avg_delivery_rating
        FROM online_food_delivery
        GROUP BY Order_Status;
    """,

    "Profit Margin %": """
        SELECT 
        ROUND(
            (SUM(Final_Amount - Discount_Applied) / SUM(Final_Amount)) * 100, 2
        ) AS profit_margin_percentage
        FROM online_food_delivery
        WHERE Order_Status = 'Delivered';
    """
}

# Button
if st.button("Run"):
    cursor.execute(queries[option])
    result = cursor.fetchall()
    df = pd.DataFrame(result)

    # Show result
    st.dataframe(df)
