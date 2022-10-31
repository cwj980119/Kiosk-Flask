import dlib,cv2,threading
import numpy as np
import pymysql
import random
import learning
import os


class Cam():
    def __init__(self):
        # s3로 수정 필요
        self.path_train = './dataset/train/'+str(self.parent.user_num)
        self.path_test = './dataset/test/'+str(self.parent.user_num)
        if not os.path.exists(self.path_train):
            os.makedirs(self.path_train)
            os.makedirs(self.path_test)

    def run(self):
        
        a = random.sample(range(0, 12), 3)  # 0부터 11까지의 범위중에 3개를 중복없이 뽑겠다.
        #cam = cv2.VideoCapture(0, cv2.CAP_DSHOW) 
        #width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
        #height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
        detector = dlib.get_frontal_face_detector()
        train_count = test_count = 0
        self.file_list=[]
        self.count = 0
        self.pic = False
        
        frame = cv2.imread('./image/temp.jpg',1) #??
        face = detector(frame)
        for f in face:
            # dlib으로 얼굴 검출
            cv2.rectangle(frame, (f.left() - 21, f.top() - 21), (f.right() + 21, f.bottom() + 21), (0, 0, 255), 1)
        if len(face) == 1:
            # 박스 크기만큼 크롭
            crop = frame[f.top() - 20:f.bottom() + 20, f.left() - 20:f.right() + 20]
            # 사이즈 조정
            crop = cv2.resize(crop, (224, 224))
            # train, validation data 구분
            if self.pic:
                if self.count not in a:
                    file_name_path = self.path_train + '/' + str(train_count) + '.jpg'
                    train_count += 1
                else:
                    file_name_path = self.path_test + '/' + str(test_count) + '.jpg'
                    test_count += 1
                # #gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)  # 흑백으로도 저장
                # cv2.imwrite(file_name_path_gray, gray)
                self.file_list.append([file_name_path,crop])
                self.count += 1
                self.pic = False
        '''
        frame = cv2.flip(frame, 1)
        cvt_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, c = cvt_frame.shape
        qImg = QtGui.QImage(cvt_frame.data, w, h, w * c, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        self.parent.ui.label.move(130,100)
        self.parent.ui.label.resize(round(width), round(height))
        self.parent.ui.label.setPixmap(pixmap)
        '''

class Take_pic():
    def __init__(self,main,db_name,db_password,db_birthdate,db_gender,db_phonenumber):
        self.main=main
        self.db_name=db_name
        self.db_password=db_password
        self.db_birthdate=db_birthdate
        self.db_gender=db_gender
        self.db_phonenumber=db_phonenumber
        self.ui.show()
        self.flow=0
        self.cnt = 0
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.sequence)
        self.db_check()
        self.start_cam()
        self.start_count()

    def regi_succ(self):
        self.worker.quit()
        user = [999, self.db_name, self.db_name, self.db_password, self.db_birthdate, self.db_gender, self.db_phonenumber]
        self.learning = learning.Learnig(self.main, user)
        self.ui.hide()

    def close_cam(self):
        self.working = False

    def start_count(self):
        self.timer.start()
        self.ask =True

    def db_check(self):
        try:
            self.conn = self.connectDB()
            self.curs = self.conn.cursor()
            sql1 = "Select max(memberID) from sho"
            self.curs.execute(sql1)
            result = self.curs.fetchone()
            self.user_num = result[0] + 1
        except:
            print("DB 연결 실패")

    def db_commit(self):
        sql = "INSERT INTO sho ( name, password, birthdate, gender, phonenumber) VALUES ( %s, %s, %s, '%s', %s)"
        var = (self.db_name, self.db_password, self.db_birthdate, self.db_gender, self.db_phonenumber)
        try:
            self.curs.execute(sql,var)
            self.conn.commit()
            for i in self.worker.file_list:
                cv2.imwrite(i[0], i[1])
            self.regi_succ()
        except:
            print("실패")

    def connectDB(self):
        host = "database-1.cb5pctivsgrb.us-east-1.rds.amazonaws.com"
        username = "root"
        port = 3306
        database = "log-in"
        password = "ksc2021583"

        conn = pymysql.connect(host=host, user=username, password=password, db=database, port=port)
        return (conn)

   
    