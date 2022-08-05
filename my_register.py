import streamlit as st
import os
from PIL import Image


def register():
    st.markdown('Drag and drop an image to save it in the images folder')

    def load_image(image_file):
        img = Image.open(image_file)
        return img  

    image_file = st.file_uploader("Upload An Image",type=['png','jpeg','jpg'])
    if image_file is not None:
        file_details = {"FileName":image_file.name,"FileType":image_file.type}
        # st.write(file_details)
        img = load_image(image_file)
        with open(os.path.join("Training_images",image_file.name),"wb") as f: 
            f.write(image_file.getbuffer())         
        st.success("Saved File")   