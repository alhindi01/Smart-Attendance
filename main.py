import streamlit as st
#functions imports
from my_upload import image_upload
from my_recognition import recognition
from my_home import home
from my_register import register
from my_data import data
from my_about import about


def main():

    title = '<p style="text-align: center;font-size: 40px;font-weight: 550; "> Smart Monitoring Using Artificial Intelligence</p>'
    st.markdown(title, unsafe_allow_html=True)

    home_page = "Home"
    upload_page = "Upload"
    recognition_page = "Face Recognition"
    date_page = "View Attendance"
    register_page = "Add New Faces "
    about_page = "About"
    yousef_page = "yousef test"


    with st.sidebar:
        st.image("./assets/faceman_cropped.jpg", width=260)
        title = '<p style="font-size: 25px;font-weight: 550;">Face Detection Settings</p>'
        st.markdown(title, unsafe_allow_html=True)

    app_mode = st.sidebar.selectbox(
        "Choose the app mode",
        [
            home_page,
            upload_page,
            recognition_page,
            date_page,
            register_page,
            about_page,
            yousef_page
        ],
    )

    if app_mode == home_page:
        home()

    elif app_mode == upload_page:
        image_upload()

    elif app_mode == recognition_page:
        recognition()

    elif app_mode == register_page:
        register()

    elif app_mode == date_page:
        data()

    elif app_mode == about_page:
        about()

    elif app_mode == upload_page:
        image_upload()
        
    elif app_mode == yousef_page:
        data()


    st.sidebar.markdown(""" 
            Developed by: Hashem Mohammad and Almotasem Abuqamar
            
            
            [GitHub] (https://github.com/alhindi01/Smart-Attendance)
            """)


if __name__ == "__main__":
    main()
