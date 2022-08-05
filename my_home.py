import streamlit as st


#HTML framework of Home page
def home():


        # -------------Header Section------------------------------------------------   

    sub_title = '<p style="font-size: 20px;font-weight: 250; ">A Face Recognition application built using OpenCV, Face recognition and Streamlit.</p>'
    st.markdown(sub_title, unsafe_allow_html=True)    


    st.image("./assets/ai.png")
    title = '<p style="font-size: 25px;font-weight: 550;">Face Detection Settings</p>'
    st.markdown(title, unsafe_allow_html=True)

    supported_modes = "<html> " \
                      "<body><div> Supported  Modes (Change modes from sidebar menu)" \
                      "<ul><li>Image Upload Then Face Detection</li><li>Real-time Face Detection And Recognition </li><li>Viewing Attendance</li><li>Registering New Students</li></ul>" \
                      "</div></body></html>"

    st.markdown(supported_modes, unsafe_allow_html=True)    

    st.info("NOTE : Click the arrow icon at Top-Left to open Sidebar menu. ")