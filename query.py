# import mysql.connector
# import streamlit as st

# # connection
# conn=mysql.connector.connect(
#     host="localhost",
#     port="3306",
#     user="root",
#     passwd="",
#     db="insurancedb"
# )

# c=conn.cursor()

# # fetch data
# def view_all_data():
#     c.execute("select * from insurance order by id asc")
#     data = c.fetchall()
#     return data

import streamlit as st
import numpy as np
import pandas as pd
import pymysql
#import pyodbc
from sqlalchemy import create_engine, text

# connecting to the database
engine = create_engine("mysql+pymysql://root:@localhost/insurancedb")

@st.cache_data
def view_all_data():
    df = pd.read_sql("SELECT * FROM insurance", engine.connect())
    return df

# Initialize connection.
# conn = st.connection('mysql', type='sql')

# Perform query.
# df = conn.query('SELECT * insurance order by id asc;', ttl=600)
