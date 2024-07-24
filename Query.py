import mysql.connector as conn
import streamlit as st
import mysql

conn = mysql.connector.connect(
    host = "localhost",
    port = "3306",
    user = "root",
    passwd = "",
    db = "mydatabase"
)
c=conn.cursor()

def view_all_data() :
    c.execute('select * from insurance_data order by id asc')
    data = c.fetchall()
    return data
