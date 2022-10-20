import dlib,cv2
import numpy as np
from keras.models import load_model
import pymysql

load_model = load_model('tl_20_cropped_e20_b200.h5')
#load_model = load_model('face_model.h5')

class flasklogin():    # 구 Thread 현 flasklogin
    def __init__(self):
        print("hello")
        
    def login(self):  # 구 run 현
        
        detector = dlib.get_frontal_face_detector()
        #cam = cv2.VideoCapture(0, cv2.CAP_DSHOW) 삭제?
        
        count = 0
        #user_list = np.empty(shape=self.user_num)
        self.l = [0 for i in range(4)]
        #while self.working:
        frame = cv2.imread('./image/temp.jpg',1)
        #cv2.imshow('VideoFrame', frame) #사진 보이기 테스트
        #cv2.waitKey(1000)
        face = detector(frame)
        user_list = np.empty(shape=self.user_num)
        print("hell")
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
            print(image.shape)
            a = load_model.predict(image)
            # print(a[0][np.argmax(a)])
            if count < 100:
                count += 1
                user_list += a[0]
                print(count)
        else:
            print("얼굴이 없습니다.")
                  
        frame = cv2.flip(frame, 1) #좌우반전
        cvt_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #색상공간변환함수
        h, w, c = cvt_frame.shape
        
        if count > 50:
            a = np.sort(user_list)[::-1]
            for i in range(4):
                self.l[i] = np.where(user_list==a[i])[0][0]
            return 
        
    def db_check(self):
        try:
            self.conn = self.connectDB()
            self.curs = self.conn.cursor()
            sql1 = "Select max(memberID) from sho"
            self.curs.execute(sql1)
            result = self.curs.fetchone()
            self.user_num = result[0] + 1
            print(self.user_num)
        except:
            print("DB 연결 실패")
            
    def connectDB(self):
        host = "database-1.cb5pctivsgrb.us-east-1.rds.amazonaws.com"
        username = "root"
        port = 3306
        database = "log-in"
        password = "ksc2021583"

        conn = pymysql.connect(host=host, user=username, password=password, db=database, port=port)
        return (conn)


class Login():
    def __init__(self, main):
        self.main = main
        try:
            conn = connectDB()
            self.curs = conn.cursor()
            self.curs.execute("select count(*) from sho")
            result = self.curs.fetchone()
            self.user_num = result[0]
            print(self.user_num)
        except:
            print("db연결 실패")
            conn.close()
            self.close()


    def start_check(self):
        if(self.worker.working):
            self.predict_list = []
            print(self.worker.l)
            sql = "select * from sho where memberID =" + str(self.worker.l[0]+1)
            self.curs.execute(sql)
            self.predict_list.append(self.curs.fetchone())
            sql = "select * from sho where memberID in ("+str(self.worker.l[1]+1)+"," + str(self.worker.l[2]+1)+"," + str(self.worker.l[3]+1)+")"
            self.curs.execute(sql)
            self.predict_list.append(self.curs.fetchall())
            print(self.predict_list)
            self.check =check_login.Check(self.predict_list, self)

    def succ(self, user):
        self.close()
        self.main.toMenu(user)
