
import streamlit as st
import cv2
import numpy as np
import pandas as pd
import face_recognition
import os
from datetime import datetime
from PIL import Image
import time


# making the code reads our images to work upon
#"Training_images" is the folder in which all the images of students are added to track their attendance

path = 'Training_images'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

#converting our images to encode images which is readable by function as it reads only RGB img

def findEncodings(images):
    encodeList = []

    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# computing the facial embedding for the face
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(images)

#tracking the attendance of students in a file Attendance.csv
# line is like a string of an array, each element of a line is a string of comma seprated values (name, time)
# entry is a small two elememt array whose elements are name and time.
# f.writelines adding names and time in csv file

def markAttendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

#website framework with streamlit

@st.cache
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

hhide_st_style = """ 
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hhide_st_style, unsafe_allow_html=True) #hide streamlit menu


def main():
    st.title("Smart Attendance Project")
    menu = ["Home", "Face Recognition","Register", "Data", "About"]
    choice = st.sidebar.selectbox("Select Activity", menu)
    st.sidebar.markdown(""" 
            Developed by: Hashem Mohammad and Almotasem Abuqamar
            
            
            [GitHub] (put link here)
            """)

#HTML framework of Home page
    if choice == "Home":
        html_temp_home1 = """<div style="background-color:#6D7B8D;padding:10px">
                                            <h4 style="color:white;text-align:center;">
                                            A Face Recognition application using OpenCV, Face recognition and Streamlit.</h4>
                                            </div>
                                            </br>"""
        st.markdown(html_temp_home1, unsafe_allow_html=True)
        st.write("""
                 The application has two functionalities.
                 1. Real time face detection using web camera feed.
                 2. Real time Attendance Creation.
                 """)

#HTML frame work and working part of face recognition project
    elif choice == "Face Recognition":
        st.header("Webcam Live Attendance")

    #start checkbox by clicking on it web cam start detecting face along with attendance,to "stop" uncheck the start checkbox
        st.write("Click on start to use your web camera and detect your face to mark your attendance")
        FRAME_WINDOW = st.image([])
        run = st.checkbox('Start')
        cap = cv2.VideoCapture(0)

        while run:
            _, img = cap.read()
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)

#finding the face locations from frame/image captured from webcam and encoding the image
            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

#comparing the captured image with encodelistknown (the encoded data images)
#the machine comapare whose embeddings is more close to webcame image and give a index
#the image from data images having highest match.index will be the person in webcame and his respective name will shown up
            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    name = classNames[matchIndex].upper()

#after finding the face location we are going to make a rectangle with thename of person on it.
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    markAttendance(name)
                    time.sleep(3)
                #new code
                else:
                    y1,x2,y2,x1 = faceLoc
                    y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                    cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),2)
                    cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,0,255),cv2.FILLED)
                    cv2.putText(img,"Unknown",(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)


            FRAME_WINDOW.image(img)
            # st.dataframe(pd.read_csv('Attendance.csv'))


        else:
            csv = convert_df(pd.read_csv('Attendance.csv'))
            st.download_button(
                "Press to Download Attendance sheet",
                csv,
                "attendance.csv",
                "text/csv",
                key='download-csv'
                )


        #register menu
    elif choice == 'Register':
        st.markdown('Drag and drop an image to save it in the images folder')

        def load_image(image_file):
            img = Image.open(image_file)
            return img  

        image_file = st.file_uploader("Upload An Image",type=['png','jpeg','jpg'])
        if image_file is not None:
            file_details = {"FileName":image_file.name,"FileType":image_file.type}
            st.write(file_details)
            img = load_image(image_file)
            with open(os.path.join("Training_images",image_file.name),"wb") as f: 
                f.write(image_file.getbuffer())         
            st.success("Saved File")    

    #read data menu
    elif choice == 'Data':
        df = pd.read_csv('attendance.csv')
        st.subheader("Read Data")
        df = pd.read_csv('attendance.csv')
        st.write(df)

#about webpage framework
    elif choice == "About":
        st.subheader("About this application")
        html_temp_about1= """<div style="background-color:#6D7B8D;padding:10px">
                                    <h5 style="color:white;text-align:center;">
                                    This project involves building an attendance system which utilizes facial recognition to mark the presence. It covers areas such as facial detection, alignment, and recognition, 
                                    along with the development of a web application using OpenCV, Face recognition and streamlit.</h5>
                                    </div>
                                    </br>"""
                                    
        st.markdown(html_temp_about1, unsafe_allow_html=True)

        html_temp4 = """
                             		<div style="background-color:#98AFC7;padding:10px">
                             		<h4 style="color:white;text-align:center;">Have A Nice Day</h4>
                             		<h4 style="color:white;text-align:center;">Thanks for Visiting</h4>
                             		</div>
                             		<br></br>
                             		<br></br>"""

        st.markdown(html_temp4, unsafe_allow_html=True)

    else:
        pass


if __name__ == "__main__":
    main()