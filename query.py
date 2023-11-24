import mysql.connector
import streamlit as st

# connection
conn=mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    passwd="",
    db="insurancedb"
)

c=conn.cursor()

# fetch data
def view_all_data():
    c.execute("select * from insurance order by id asc")
    data = c.fetchall()
    return data


# Initialize connection.
# conn = st.connection('mysql', type='sql')

# Perform query.
# df = conn.query('SELECT * insurance order by id asc;', ttl=600)
