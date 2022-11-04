import dlib,cv2
import numpy as np
from keras.models import load_model
import pymysql
from dotenv import load_dotenv
import os
from flask import Flask, jsonify, request
import json

#oad_model = load_model('tl_20_cropped_e20_b200.h5')
load_model = load_model('face_model.h5')

load_dotenv(verbose=True)
AWS_RDS_HOST=os.getenv('AWS_RDS_HOST')
AWS_RDS_USERNAME=os.getenv('AWS_RDS_USERNAME')
AWS_RDS_PORT=3306
AWS_RDS_DATABASE=os.getenv('AWS_RDS_DATABASE')
AWS_RDS_PASSWORD=os.getenv('AWS_RDS_PASSWORD')


class flasklogin():    # 구 Thread 현 flasklogin
    def __init__(self):
        print("hello")
        
    def login(self):  # 구 run 현
        #print("1")
        detector = dlib.get_frontal_face_detector()
        #cam = cv2.VideoCapture(0, cv2.CAP_DSHOW) 삭제?
        user_list = np.empty(shape=self.user_num)
        self.l = [0 for i in range(4)]
        print(self.user_num)
    
        frame = cv2.imread('./image/temp0.jpg',1)
        face = detector(frame)
        for f in face:
                # dlib으로 얼굴 검출
            cv2.rectangle(frame, (f.left(), f.top()), (f.right(), f.bottom()), (0, 0, 255), 1)
        
        if len(face) == 1:
            crop = frame[f.top():f.bottom(), f.left():f.right()]
            crop = cv2.resize(crop, (224, 224))
            image = np.array(crop)
            image = image.astype('float32') / 255
                #
                # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  ####gray
                # image = np.expand_dims(image,-1)                 ####gray

            image = np.expand_dims(image, 0)
                #print(image.shape)
            a = load_model.predict(image)   
            print(a[0][np.argmax(a)])
            user_list = a[0]
            print(a[0])
            print(user_list)
            cv2.imshow('VideoFrame', crop) #사진 보이기 테스트
            cv2.waitKey(1000)
            cv2.imwrite('./image/tempcrop.jpg',crop)
            a = np.sort(user_list)[::-1]
            for i in range(4):
                self.l[i] = np.where(user_list==a[i])[0][0]
                
        
            print("end")
            print(self.l)
            
        else:
            print("얼굴이 없습니다")
            
        # frame = cv2.flip(frame, 1) #좌우반전
        #cvt_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #색상공간변환함수
        #h, w, c = cvt_frame.shape
        
        return
        
    def crop(self):
        detector = dlib.get_frontal_face_detector()
        frame = cv2.imread('./image/temp0.jpg',1)
        face = detector(frame)
        for f in face:
                # dlib으로 얼굴 검출
            cv2.rectangle(frame, (f.left(), f.top()), (f.right(), f.bottom()), (0, 0, 255), 1)
        
        if len(face) == 1:
            crop = frame[f.top():f.bottom(), f.left():f.right()]
            crop = cv2.resize(crop, (224, 224))
            image = np.array(crop)
            image = image.astype('float32') / 255
            #print(image.shape)
            cv2.imwrite('./image/tempcrop.jpg',crop)
            print("end")
            
        else:
            print("얼굴이 없습니다")
        return
        
    def loginDB(self):
        
        self.predict_list=[]
        #print(self.l)
        sql = "select * from sho where memberID =" + str(self.l[0]+1)
        self.curs.execute(sql)
        self.predict_list.append(self.curs.fetchone())
        sql = "select * from sho where memberID =" + str(self.l[1]+1)
        self.curs.execute(sql)
        self.predict_list.append(self.curs.fetchone())
        sql = "select * from sho where memberID =" + str(self.l[2]+1)
        self.curs.execute(sql)
        self.predict_list.append(self.curs.fetchone())
        sql = "select * from sho where memberID =" + str(self.l[3]+1)
        self.curs.execute(sql)
        self.predict_list.append(self.curs.fetchone())
        '''
        sql = "select * from sho where memberID in ("+str(self.l[1]+1)+"," + str(self.l[2]+1)+"," + str(self.l[3]+1)+")"
        self.curs.execute(sql)
        self.predict_list.append(self.curs.fetchall())
        '''
        print(self.predict_list)

        return jsonify({"0" : {"id":self.predict_list[0][0],"name": self.predict_list[0][1],"password":self.predict_list[0][2],
                 "Date":self.predict_list[0][3],"gender":self.predict_list[0][4],"phonenumber":self.predict_list[0][5]},
                  "1" : {"id":self.predict_list[1][0],"name": self.predict_list[1][1],"password":self.predict_list[1][2],
                 "Date":self.predict_list[1][3],"gender":self.predict_list[1][4],"phonenumber":self.predict_list[1][5]},
                  "2" : {"id":self.predict_list[2][0],"name": self.predict_list[2][1],"password":self.predict_list[2][2],
                 "Date":self.predict_list[2][3],"gender":self.predict_list[2][4],"phonenumber":self.predict_list[2][5]},
                  "3" : {"id":self.predict_list[3][0],"name": self.predict_list[3][1],"password":self.predict_list[3][2],
                 "Date":self.predict_list[3][3],"gender":self.predict_list[3][4],"phonenumber":self.predict_list[3][5]}})
          
    
        
    def db_check(self):
        try:
            self.conn = self.connectDB()
            self.curs = self.conn.cursor()
            sql1 = "Select max(memberID) from sho"
            self.curs.execute(sql1)
            result = self.curs.fetchone()
            self.user_num = result[0]
            print(self.user_num)
        except:
            print("DB 연결 실패")
    def usernum_check(self):
        try:
            self.conn = self.connectDB()
            self.curs = self.conn.cursor()
            sql1 = "Select max(memberID) from sho"
            self.curs.execute(sql1)
            result = self.curs.fetchone()
            self.user_num = result[0]
            return(self.user_num+1)
        except:
            print("DB 연결 실패")
            
            
    def connectDB(self):
        
        host = AWS_RDS_HOST
        username = AWS_RDS_USERNAME
        port = AWS_RDS_PORT
        database = AWS_RDS_DATABASE
        password = AWS_RDS_PASSWORD

        conn = pymysql.connect(host=host, user=username, password=password, db=database, port=port)
        return (conn)
