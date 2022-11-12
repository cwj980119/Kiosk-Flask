import os
import random
import dlib,cv2
import numpy as np
from keras.models import load_model
import pymysql
from dotenv import load_dotenv
import learning
from s3 import s3_connection, s3_put_object, s3_get_object

class flaskRegister():
    
    def __init__(self):
        
        self.path_train = './image/train/'
        self.path_test = './image/test/'
        if not os.path.exists(self.path_train):
            os.makedirs(self.path_train)
            os.makedirs(self.path_test)
        
        #print("res")
            
    def flaskframenumber(self):
        detector = dlib.get_frontal_face_detector()
        for i in range(10):
            file_name="./image/temp"+str(i)+".jpg"
            print(file_name)
            frame = cv2.imread(file_name,1) 
            face = detector(frame)
            for f in face:
                # dlib으로 얼굴 검출
                # cv2.rectangle(frame, (f.left() - 21, f.top() - 21), (f.right() + 21, f.bottom() + 21), (0, 0, 255), 1)
                cv2.rectangle(frame, (f.left(), f.top()), (f.right(), f.bottom()), (0, 0, 255), 1)
                
            if len(face)>1:
                print(len(face))
            elif len(face)==1:
                print(len(face))
            elif len(face)==0:
                print("zero")
        
        return
    
      
    