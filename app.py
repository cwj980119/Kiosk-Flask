from sre_parse import FLAGS
from flask import Flask, jsonify, request
from s3 import s3_connection, s3_put_object, s3_get_object
import os
import boto3
from dotenv import load_dotenv
from newlogin import flasklogin

app = Flask(__name__)

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
    '''
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
    file_path="./image/temp.jpg"
    
    if os.path.exists(file_path):
        os.remove(file_path)
    '''원래코드 
    object_name=request.args.get('object_name')
    # 파일 다운로드하면서 바로 가능한가?
    tempjpg=s3_get_object(s3, AWS_S3_BUCKET_NAME, object_name, file_path)
    login.flasklogin.run(tempjpg)
    return "Hello, World!"
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
    return "new image.jpg"
    
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
