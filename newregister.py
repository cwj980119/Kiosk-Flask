import os
import random
import dlib,cv2
import numpy as np
from keras.models import load_model
import pymysql
from dotenv import load_dotenv


class flaskRegister():
    
    def __init__(self):
        '''
        self.path_train = './dataset/train/'+str(self.user_num)
        self.path_test = './dataset/test/'+str(self.user_num)
        if not os.path.exists(self.path_train):
            os.makedirs(self.path_train)
            os.makedirs(self.path_test)
        '''
            
    def flaskframenumber(self):
        detector = dlib.get_frontal_face_detector()
        for i in range(10):
            file_name='./image/temp'+str(i)+'.jpg'
            frame = cv2.imread(file_name,1) 
            face = detector(frame)
            for f in face:
                # dlib으로 얼굴 검출
                cv2.rectangle(frame, (f.left() - 21, f.top() - 21), (f.right() + 21, f.bottom() + 21), (0, 0, 255), 1)
            if len(face)>1:
                print(len(face))
            elif len(face)==1:
                print(len(face))
            elif len(face)==0:
                print("zero")
        
        return
    
    def flasklearning(self):
        
        detector = dlib.get_frontal_face_detector()
        a = random.sample(range(0, 12), 3)
        train_count = test_count = 0
        self.file_list=[]
        self.count = 0
        self.path_train = './image/train/'
        self.path_test = './image/test/'
        # train과 test로 랜덤하게 나누기
        for i in range(11):
            self.title="./image/temp" + str(i) + ".jpg"
            frame = cv2.imread(self.title,1)
            for f in frame:
                # dlib으로 얼굴 검출
                cv2.rectangle(frame, (f.left() - 21, f.top() - 21), (f.right() + 21, f.bottom() + 21), (0, 0, 255), 1)
            if len(frame) == 1:
                # 박스 크기만큼 크롭
                crop = frame[f.top() - 20:f.bottom() + 20, f.left() - 20:f.right() + 20]
                # 사이즈 조정
                if self.count not in a:
                    file_name_path = self.path_train + '/' + str(train_count) + '.jpg'
                    train_count += 1
                else:
                    file_name_path = self.path_test + '/' + str(test_count) + '.jpg'
                    test_count += 1
                self.file_list.append([file_name_path,crop])
                self.count += 1      
            '''      
            frame = cv2.flip(frame, 1)
            cvt_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, c = cvt_frame.shape
            '''
            
        
                
            
    '''   
    def flaskframe(self):
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
        
        frame = cv2.flip(frame, 1)
        cvt_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, c = cvt_frame.shape
        qImg = QtGui.QImage(cvt_frame.data, w, h, w * c, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        self.parent.ui.label.move(130,100)
        self.parent.ui.label.resize(round(width), round(height))
        self.parent.ui.label.setPixmap(pixmap)
        
        return 
    '''
    
    def createFolder(directory):
        try:
            if not os.path.exists(directory):
            os.makedirs(directory+'/train')
            os.makedirs(directory+'/test')
        except OSError:
            print('Error: Creating directory. ' + directory)
        