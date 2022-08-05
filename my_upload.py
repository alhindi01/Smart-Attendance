import streamlit as st
import cv2
import numpy as np
from PIL import Image
from io import BytesIO



def image_upload():
    
    # Haar-Cascade Parameters
    minimum_neighbors = 4
    # Minimum possible object size
    min_object_size = (50, 50)
    # bounding box thickness
    # bounding box color
    bbox_color = (0, 255, 0)


    st.markdown(
        "Upload an image, then Frontal-face detection using OpenCV and Haar-Cascade Algorithm will be applied to it"
    )    

 
    uploaded_file = st.file_uploader(
        "Upload Image (Only PNG & JPG images allowed)", type=['png', 'jpg'])

    if uploaded_file is not None:

        with st.spinner("Detecting faces..."):
            img = Image.open(uploaded_file)

            # To convert PIL Image to numpy array:
            img = np.array(img)

            # Load the cascade
            face_cascade = cv2.CascadeClassifier(
                'haarcascade_frontalface_default.xml')

            # Convert into grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Detect faces
            faces = face_cascade.detectMultiScale(
                gray, 1.1, minNeighbors=minimum_neighbors, minSize=min_object_size)

            if len(faces) == 0:
                st.warning(
                    "No Face Detected in Image. Make sure your face is visible in the camera with proper lighting."
                    " Also try adjusting detection parameters")
            else:
                # Draw rectangle around the faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h),
                                  color=bbox_color)

                # Display the output
                st.image(img)

                if len(faces) > 1:
                    st.success("Total of " + str(
                        len(faces)) + " faces detected inside the image. Try adjusting minimum object size if we missed anything")

                    # convert to pillow image
                    img = Image.fromarray(img)
                    buffered = BytesIO()
                    img.save(buffered, format="JPEG")

                    # Creating columns to center button
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        pass
                    with col3:
                        pass
                    with col2:
                        st.download_button(
                            label="Download image",
                            data=buffered.getvalue(),
                            file_name="output.png",
                            mime="image/png")
                else:
                    st.success(
                        "Only 1 face detected inside the image. Try adjusting minimum object size if we missed anything.")

                    # convert to pillow image
                    img = Image.fromarray(img)
                    buffered = BytesIO()
                    img.save(buffered, format="JPEG")

                    # Creating columns to center button
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        pass
                    with col3:
                        pass
                    with col2:
                        st.download_button(
                            label="Download image",
                            data=buffered.getvalue(),
                            file_name="output.png",
                            mime="image/png")
