from sre_parse import FLAGS
from flask import Flask, jsonify, request
from s3 import s3_connection, s3_put_object, s3_get_object,s3_get_alldataset,s3_get_signupuser_dataset
import os
import boto3
from dotenv import load_dotenv
from newlogin import flasklogin
from newregister import flaskRegister
from faceCheck import check
import cv2
from learning import Learnig
import redis
import time
import json
from celery import Celery

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
celery = Celery('app', broker=BROKER_URL, backend=CELERY_RESULT_BACKEND)


load_dotenv(verbose=True)
AWS_S3_BUCKET_REGION=os.getenv('AWS_S3_BUCKET_REGION')
AWS_S3_BUCKET_NAME=os.getenv('AWS_S3_BUCKET_NAME')
AWS_ACCESS_KEY=os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY=os.getenv('AWS_SECRET_ACCESS_KEY')

s3 = s3_connection()

@celery.task()
def celery_make_model(name,passoword,birthdate,gender,phonenumber):
    ml=Learnig()
    FL=flasklogin()
    ml.init_model()  
    FL.signupDB(name,passoword,birthdate,gender,phonenumber)
    FL.signupmenuDB()
    return ("celery_model complete")

@celery.task()
def addface_make_model():
    ml=Learnig()
    ml.init_model()  
    return ("celery_model complete")
    

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/home/<lang>')
def home(lang):
    page = request.args.get('page')
    return jsonify({"lang":lang,
                    "page": page})

@app.route('/route/<lang>')
def route(lang):
    return jsonify({"lang":lang})

@app.route('/faceCheck', methods=['GET','POST'])
def faceCheck():
    file_path = "./image/check.jpg"
    if os.path.exists(file_path):
        os.remove(file_path)

    object_name = "image/check.jpg"
    # 파일 다운로드하면서 바로 가능한가?
    s3_get_object(s3, AWS_S3_BUCKET_NAME, object_name, file_path)
    result = check();
    return jsonify({"result": result})


@app.route('/fileUpload', methods=['POST'])
def upload():
    f = request.files['file']
    f.save("./temp")
    
    ret = s3_put_object(s3, AWS_S3_BUCKET_NAME, "./temp", ".temp")
    if ret :
        print("파일 저장 성공")
    else:
        print("파일 저장 실패")
        
#fildedownload에서 login으로 이름변경
@app.route('/login', methods=['GET','POST'])
def download():
    FL=flasklogin()   
    file_path="./image/temp.jpg"
    if os.path.exists(file_path):
        os.remove(file_path)
            
    # electron연결용
    object_name=request.args.get('object_name')
    s3_get_object(s3, AWS_S3_BUCKET_NAME, object_name, file_path)
    FL.db_check()
    FL.login()
    return FL.loginDB()

@app.route('/loginmenu', methods=['GET','POST'])
def loginmenu(): 
    FL=flasklogin() 
    #memberID받아서 menu출력
    memberID=request.args.get('memberID')
    
    return FL.signuomenuprint(memberID)

@app.route('/loginmenudata_update', methods=['GET','POST'])
def loginmenudata_update(): 
    #로그인한 사람이 주문한 데이터를 다시 저장
    FL=flasklogin() 
    count=request.args.get('count')
    memberID=request.args.get('memberID')
    for i in range(count):
        menuID=request.args.get('menuID['+str(i)+']')
        menucount=request.args.get('menucount['+str(i)+']')
        FL.loginmenudata_update(memberID, menuID, menucount)

    
    return FL.menuprint(memberID)
'''
@app.route('/signupmenu', methods=['GET','POST'])
def signupmenu(): 
    FL=flasklogin() 
    object_name=request.args.get('object_name')
    memberID=FL.loginmenu_check(object_name)
    
    return FL.menuprint(memberID)
'''

@app.route('/addface', methods=['GET','POST'])
def addface(): 
    object_name=request.args.get('object_name')
    file_path=object_name.replace('signup','./image')
    s3_get_object(s3, AWS_S3_BUCKET_NAME, object_name, file_path)
    task=addface_make_model()
    return("hello")


@app.route('/test', methods=['GET','POST'])
def test():
    '''
    object_name=request.args.get('object_name')
    for i in range(object_name):
        print(object_name[i])
    jsonify({"result": "list possible"})
    '''
    FL=flasklogin()
    
    FL.signupmenuDB()
    return("done")

@app.route('/signupdownload', methods=['GET','POST'])
def signupdownload():
    for i in range(11):
        object_name=request.args.get('object_name['+str(i)+']')
        file_path=object_name.replace('signup','./image')
        s3_get_object(s3, AWS_S3_BUCKET_NAME, object_name, file_path)
    return True

@app.route('/alldataset_model', methods=['GET','POST'])
def alldatasetmodel():
    s3_get_alldataset(s3,AWS_S3_BUCKET_NAME)
    task=celery_make_model()
    
    return "alldatasetmodel complete"


@app.route('/signup_dataset_model', methods=['GET','POST'])
def signupdatasetmodel():
    for i in range(11):
        object_name=request.args.get('object_name['+str(i)+']')
        file_path=object_name.replace('signup','./image')
        s3_get_object(s3, AWS_S3_BUCKET_NAME, object_name, file_path)
    
    name = request.args.get('fullname') 
    password = request.args.get('password')
    birthdate = request.args.get('birthdate')
    gender = request.args.get('gender')
    phonenumber = request.args.get('phonumber')
    
    task = celery_make_model(name,password,birthdate,gender,phonenumber)
    
    return "signup user datasetmodel complete"


@app.route('/age_gender', methods=['GET','POST'])
def age_gender():
    FL=flasklogin()
    return FL.age_gendercheck()

@app.route('/nonloginmenu', methods=['GET','POST'])
def nonloginmenu():
    FL=flasklogin()
    return FL.age_gendercheck()
    

@app.route('/RfileDownload', methods=['GET','POST'])
def Rdownload():
    #회원가입용 사진 10장 받기
    FR=flaskRegister()
    #10장 컴퓨터에 저장
    for i in range(10):
        file_path="./image/temp"+str(i)+".jpg"
        if os.path.exists(file_path):
            os.remove(file_path)
            
        # electron연결용
        #object_name=request.args.get('object_name')
        #테스트용
        object_name="signup/10/"+str(i)+".jpg"
        s3_get_object(s3, AWS_S3_BUCKET_NAME, object_name, file_path)
    #사진 당 얼굴 수 출력
    FR.flaskframenumber()
    return "Hello, World!"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
