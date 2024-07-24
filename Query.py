import mysql.connector as conn
import streamlit as st

# Establish a connection to the database using secrets
try:
    connection = conn.connect(
        host=st.secrets["mysql"]["host"],
        port=st.secrets["mysql"]["port"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"]
    )
    cursor = connection.cursor()
except conn.Error as err:
    st.error(f"Error: {err}")
    st.stop()

def view_all_data():
    cursor.execute('SELECT * FROM insurance_data ORDER BY id ASC')
    data = cursor.fetchall()
    return data
