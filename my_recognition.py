import streamlit as st
import cv2
import numpy as np
import pandas as pd
import face_recognition
import os
from datetime import datetime
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






def mark_attendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime("%m/%d/%Y, %H:%M:%S")

            f.writelines(f'\n{name},{dtString}, present')

@st.cache

def convert_df(df):
   return df.to_csv(index=False)

hhide_st_style = """ 
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hhide_st_style, unsafe_allow_html=True) #hide streamlit menu



#HTL frame work and working part of face recognition project
def recognition():
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

#fiding the face locations from frame/image captured from webcam and encoding the image
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

#coparing the captured image with encodelistknown (the encoded data images)
#th machine comapare whose embeddings is more close to webcame image and give a index
#th image from data images having highest match.index will be the person in webcame and his respective name will shown up
        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()

#afer finding the face location we are going to make a rectangle with the name of person on it.
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                mark_attendance(name)
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
