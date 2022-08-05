import pandas as pd
import streamlit as st



def data():
    df = pd.read_csv('attendance.csv')
    st.subheader("Read Data")
    df = pd.read_csv('attendance.csv')
    st.write(df)