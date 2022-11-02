from sre_parse import FLAGS
from flask import Flask, jsonify, request
from s3 import s3_connection, s3_put_object, s3_get_object, s3_get_folder
import os
import boto3
from dotenv import load_dotenv
from newlogin import flasklogin
from newregister import flaskRegister
from faceCheck import check
import cv2
from learning import Learnig

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

load_dotenv(verbose=True)
AWS_S3_BUCKET_REGION=os.getenv('AWS_S3_BUCKET_REGION')
AWS_S3_BUCKET_NAME=os.getenv('AWS_S3_BUCKET_NAME')
AWS_ACCESS_KEY=os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY=os.getenv('AWS_SECRET_ACCESS_KEY')

s3 = s3_connection()

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
        
        
@app.route('/fileDownload', methods=['GET','POST'])
def download():
    FL=flasklogin()
   
    file_path="./image/temp.jpg"
    
    if os.path.exists(file_path):
        os.remove(file_path)
        

        
    # electron연결용
    object_name=request.args.get('object_name')
    #print(object_name)
    #테스트용
    #object_name="image/img2.jpg"
    # 파일 다운로드하면서 바로 가능한가?
    s3_get_object(s3, AWS_S3_BUCKET_NAME, object_name, file_path)
    print("1")
    FL.db_check()
    print("2")
    FL.login()
    return FL.loginDB()


    
    '''
    #테스트용
    object_name="image/img2.jpg"
    # 파일 다운로드하면서 바로 가능한가?
    s3_get_object(s3, AWS_S3_BUCKET_NAME, object_name, file_path)
    print("1")
    FL.db_check()
    print("2")
    FL.login()
    print("3")
    FL.loginDB()
    print(FL.predict_list)
    return "new image.jpg"
    '''
    ''' 
    테스트용
    object_name=request.args.get('object_name')
    file_path="./uploads/"
    files=os.listdir("./uploads")
    for x in files:
        if(x==object_name):
            sw=1
            s3.download_file(AWS_S3_BUCKET_NAME, object_name, file_path)
        else:   
            print("파일이 없습니다")         
    '''

@app.route('/login', methods=['GET','POST'])
def loginandupload():
    fullname=request.args.get('fullname')
    
    
@app.route('/register', methods=['GET','POST'])
def register():
    FR=flaskRegister()
    #회원가입용 사진을 test/train으로 분리
    #FR.flasklearning()
    
    
    return "register"

@app.route('/test', methods=['GET','POST'])
def test():
    #ML=Learnig()
    #ML.init_model()
    s3_get_folder(s3, AWS_S3_BUCKET_NAME)
    
    return "test"

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
    
    
    
    '''  
    # electron연결용
    object_name=request.args.get('object_name')
    #테스트용
    #object_name="image/img2.jpg"
    # 파일 다운로드하면서 바로 가능한가?
    s3_get_object(s3, AWS_S3_BUCKET_NAME, object_name, file_path)
    print("1")
    FL.db_check()
    print("2")
    FL.login()
    FL.loginDB()
    '''
    return "Hello, World!"
