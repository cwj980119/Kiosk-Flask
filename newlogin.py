import dlib,cv2
import numpy as np
from keras.models import load_model
import pymysql
from dotenv import load_dotenv
import os
from flask import Flask, jsonify, request
import json

#load_model = load_model('tl_20_cropped_e20_b200.h5')
load_model = load_model("face_model.h5")

load_dotenv(verbose=True)
AWS_RDS_HOST=os.getenv('AWS_RDS_HOST')
AWS_RDS_USERNAME=os.getenv('AWS_RDS_USERNAME')
AWS_RDS_PORT=3306
AWS_RDS_DATABASE=os.getenv('AWS_RDS_DATABASE')
AWS_RDS_PASSWORD=os.getenv('AWS_RDS_PASSWORD')
AWS_RDS_TABLE=os.getenv('AWS_RDS_TABLE')
AWS_RDS_MENUTABLE=os.getenv('AWS_RDS_MENUTABLE')
AWS_RDS_SIGNUPMENU=os.getenv('AWS_RDS_SIGNUPMENU')
AWS_RDS_NONSIGNUPMENU=os.getenv('AWS_RDS_NONSIGNUPMENU')
AWS_RDS_MENUDATA=os.getenv('AWS_RDS_MENUDATA')

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
    
        frame = cv2.imread('./image/temp.jpg',1)
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
            #cv2.imshow('VideoFrame', crop) #사진 보이기 테스트
            #cv2.waitKey(1000)
            #cv2.imwrite('./image/tempcrop.jpg',crop)
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
        frame = cv2.imread('./image/temp.jpg',1)
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
    
    def age_gendercheck(self):
        
        # 얼굴 탐지 모델 가중치
        cascade_filename = 'haarcascade_frontalface_alt.xml'
        # 모델 불러오기
        cascade = cv2.CascadeClassifier(cascade_filename)
        MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)

        age_net = cv2.dnn.readNetFromCaffe('deploy_age.prototxt','age_net.caffemodel')
        gender_net = cv2.dnn.readNetFromCaffe('deploy_gender.prototxt','gender_net.caffemodel')
        age_list = ['(0 ~ 2)','(4 ~ 6)','(8 ~ 12)','(15 ~ 20)', '(25 ~ 32)','(38 ~ 43)','(48 ~ 53)','(60 ~ 100)']
        gender_list = ['Male', 'Female']
        
        frame = cv2.imread('./image/temp.jpg',1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        # cascade 얼굴 탐지 알고리즘 
        results = cascade.detectMultiScale(gray)        

        for box in results:

            x, y, w, h = box
            face = frame[int(y):int(y+h),int(x):int(x+h)].copy()
            blob = cv2.dnn.blobFromImage(face, 1, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
            
            # gender detection
            gender_net.setInput(blob)
            gender_preds = gender_net.forward()
            gender = gender_preds.argmax()
            
            # Predict age
            age_net.setInput(blob)
            age_preds = age_net.forward()
            age = age_preds.argmax()
            info = gender_list[gender] +' '+ age_list[age]
            return jsonify({"gender": gender_list[gender]},{"age":age_list[age]})
            

        
    def loginDB(self):
        
        self.predict_list=[]
        #print(self.l)
        sql = "select memberID, name, date_format(birthdate, '%m%d') as date, gender from "+AWS_RDS_TABLE+" where memberID =" + str(self.l[0]+1)
        self.curs.execute(sql)
        self.predict_list.append(self.curs.fetchone())
        sql = "select memberID, name, date_format(birthdate, '%m%d') as date, gender from "+AWS_RDS_TABLE+" where memberID =" + str(self.l[1]+1)
        self.curs.execute(sql)
        self.predict_list.append(self.curs.fetchone())
        sql = "select memberID, name, date_format(birthdate, '%m%d') as date, gender  from "+AWS_RDS_TABLE+" where memberID =" + str(self.l[2]+1)
        self.curs.execute(sql)
        self.predict_list.append(self.curs.fetchone())
        sql = "select memberID, name, date_format(birthdate, '%m%d') as date, gender  from "+AWS_RDS_TABLE+" where memberID =" + str(self.l[3]+1)
        self.curs.execute(sql)
        self.predict_list.append(self.curs.fetchone())
        '''
        sql = "select * from "+AWS_RDS_TABLE+" where memberID in ("+str(self.l[1]+1)+"," + str(self.l[2]+1)+"," + str(self.l[3]+1)+")"
        self.curs.execute(sql)
        self.predict_list.append(self.curs.fetchall())
        '''
        print(self.predict_list)

        return jsonify({"0" : {"id":self.predict_list[0][0],"name": self.predict_list[0][1],
                 "Date":self.predict_list[0][2],"gender":self.predict_list[0][3]},
                  "1" : {"id":self.predict_list[1][0],"name": self.predict_list[1][1],
                 "Date":self.predict_list[1][2],"gender":self.predict_list[1][3]},
                  "2" : {"id":self.predict_list[2][0],"name": self.predict_list[2][1],
                 "Date":self.predict_list[2][2],"gender":self.predict_list[2][3]},
                  "3" : {"id":self.predict_list[3][0],"name": self.predict_list[3][1],
                 "Date":self.predict_list[3][2],"gender":self.predict_list[3][3]}})
          
    
        
    def db_check(self):
        try:
            self.conn = self.connectDB()
            self.curs = self.conn.cursor()
            sql1 = "Select max(memberID) from "+AWS_RDS_TABLE
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
            sql1 = "Select max(memberID) from "+AWS_RDS_TABLE
            self.curs.execute(sql1)
            result = self.curs.fetchone()
            self.user_num = result[0]
            return(self.user_num+1)
        except:
            print("DB 연결 실패")
    
    def loginmenu_check(self,object_name):
        try:
            self.conn = self.connectDB()
            self.curs = self.conn.cursor()
            sql1 = "Select memberID from "+AWS_RDS_TABLE+" Where name == "+object_name
            self.curs.execute(sql1)
            result = self.curs.fetchone()
            self.memberID = result[0]
            return(self.user_num)
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
    
    def signupDB(self,name,password,birthdate, gender,phonenumber):
        self.conn = self.connectDB()
        self.curs = self.conn.cursor()
        
        sql1 = "Select max(memberID) from "+AWS_RDS_TABLE
        self.curs.execute(sql1)
        result = self.curs.fetchone()
        #print(type(result))
        count=result[0]+1
        
        sql2="ALTER TABLE "+AWS_RDS_TABLE+" auto_increment = "+str(count)
        self.curs.execute(sql2)
        
        sql3="INSERT INTO "+AWS_RDS_TABLE+" ( name, password, birthdate, gender, phonenumber, train, test) VALUES ( %s, %s, %s, '%s', %s, 8, 3)"
        val3=( name, password, birthdate, gender, phonenumber)
        self.curs.execute(sql3,val3)
        print("signupdb입력완료")
        self.conn.commit()
        self.curs.close()
        self.conn.close()
        
    def signupmenuDB(self):
        # 회원가입시 모든 메뉴 디폴트 0값으로 만들기
        self.conn = self.connectDB()
        self.curs = self.conn.cursor()
        
        sql1 = "Select max(memberID) from "+AWS_RDS_TABLE
        self.curs.execute(sql1)
        result = self.curs.fetchone()
        #print(type(result))
        count1=result[0]
        print(count1)
        
        sql2 = "Select menuID from "+AWS_RDS_MENUTABLE
        self.curs.execute(sql2)
        menuID = self.curs.fetchall()
        print(menuID)
        menuID=[list(menuID[x]) for x in range(len(menuID))]
        print(menuID)
        
        for i in range(len(menuID)):
            sql3="INSERT INTO "+AWS_RDS_SIGNUPMENU+" ( memberID, menuID) VALUES ( %s, %s)"
            val3=(count1,menuID[i])
            self.curs.execute(sql3,val3)
            self.conn.commit()
            
        print("signupmenudb입력완료")
        self.curs.close()
        self.conn.close()
    
    def signupmenuprint(self,memberID):
        #memberID로 category별메뉴선호도 찾아 출력
        self.conn = self.connectDB()
        self.curs = self.conn.cursor()
        
        sql1 = "SELECT "+\
            AWS_RDS_SIGNUPMENU+".menuID AS menu, "+\
            AWS_RDS_SIGNUPMENU+".menucount AS count, "+\
            AWS_RDS_MENUTABLE+".category AS category \
            FROM "+AWS_RDS_MENUTABLE+" \
            INNER JOIN "+AWS_RDS_SIGNUPMENU+" ON "+AWS_RDS_MENUTABLE+".menuID = "+AWS_RDS_SIGNUPMENU+".menuID \
            WHERE category= 'main' AND "+AWS_RDS_SIGNUPMENU+".memberID = " +str(memberID)+" \
            ORDER BY "+AWS_RDS_SIGNUPMENU+".menucount DESC"
           
        self.curs.execute(sql1)
        self.conn.commit()
        mainresult = self.curs.fetchall()
        
        sql2 = "SELECT "+\
            AWS_RDS_SIGNUPMENU+".menuID AS menu, "+\
            AWS_RDS_SIGNUPMENU+".menucount AS count, "+\
            AWS_RDS_MENUTABLE+".category AS category \
            FROM "+AWS_RDS_MENUTABLE+" \
            INNER JOIN "+AWS_RDS_SIGNUPMENU+" ON "+AWS_RDS_MENUTABLE+".menuID = "+AWS_RDS_SIGNUPMENU+".menuID \
            WHERE category= 'side' AND "+AWS_RDS_SIGNUPMENU+".memberID = " +str(memberID)+" \
            ORDER BY "+AWS_RDS_SIGNUPMENU+".menucount DESC"
           
        self.curs.execute(sql2)
        self.conn.commit()
        sideresult = self.curs.fetchall()
        
        sql3 = "SELECT "+\
            AWS_RDS_SIGNUPMENU+".menuID AS menu, "+\
            AWS_RDS_SIGNUPMENU+".menucount AS count, "+\
            AWS_RDS_MENUTABLE+".category AS category \
            FROM "+AWS_RDS_MENUTABLE+" \
            INNER JOIN "+AWS_RDS_SIGNUPMENU+" ON "+AWS_RDS_MENUTABLE+".menuID = "+AWS_RDS_SIGNUPMENU+".menuID \
            WHERE category= 'drink' AND "+AWS_RDS_SIGNUPMENU+".memberID = " +str(memberID)+" \
            ORDER BY "+AWS_RDS_SIGNUPMENU+".menucount DESC"
           
        self.curs.execute(sql3)
        self.conn.commit()
        drinkresult = self.curs.fetchall()
        
        self.curs.close()
        self.conn.close()
        
        return
        
    def loginmenudata_update(self,memberID, menuID, menucount):
        
        self.conn = self.connectDB()
        self.curs = self.conn.cursor()
        sql="UPDATE "+AWS_RDS_SIGNUPMENU+" SET menucount = "+AWS_RDS_SIGNUPMENU+".menucount \
            + "+str(menucount)+" where memberID = (%s) AND menuID = (%s)"
        val=(memberID,menuID)
        self.curs.execute(sql,val)
        self.conn.commit()
        print("update")
        
        self.curs.close()
        self.conn.close()
        
    def nonloginmenu(self,age,gender):
        #회원데이터와 비회원데이터를 먼저 합치고 합쳐진 데이터로 추천
        self.conn = self.connectDB()
        self.curs = self.conn.cursor()
        #회원데이터를 agegroup으로 바꾸어 출력
        sql1 = "UPDATE "+AWS_RDS_MENUDATA+" SET menucount = "+AWS_RDS_MENUDATA+".menucount \
            + "+AWS_RDS_SIGNUPMENU+".menucount AND  where memberID = (%s) AND menuID = (%s)"
           
        self.curs.close()
        self.conn.close()
        
        
        
   
