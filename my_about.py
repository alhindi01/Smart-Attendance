import streamlit as st

def about():
    st.subheader("About this application")
    html_temp_about1= """<div style="background-color:#6D7B8D;padding:10px">
                                <h5 style="color:white;text-align:center;">
                                This project involves building an attendance system which utilizes facial recognition to mark the absence. It covers areas such as facial detection, and recognition, 
                                along with the development of a web application using OpenCV, Face recognition and streamlit.</h5>
                                </div>
                                </br>"""
                                
    st.markdown(html_temp_about1, unsafe_allow_html=True)
