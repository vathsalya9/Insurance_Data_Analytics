print("Query.py loaded")
import mysql.connector
import streamlit as st

conn = mysql.connector.connect(
        host=st.secrets.mysql.host,
        port=st.secrets.mysql.port,
        user=st.secrets.mysql.user,
        password=st.secrets.mysql.password,
        database=st.secrets.mysql.database
    )
cursor = conn.cursor()

def view_all_data():
    cursor.execute('SELECT * FROM insurance_data ORDER BY id ASC')
    data = cursor.fetchall()
    return data
