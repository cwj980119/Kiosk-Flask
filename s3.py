# import module
import boto3
import os
#from cloudpathlib import CloudPath
from dotenv import load_dotenv
from newlogin import flasklogin


load_dotenv(verbose=True)
AWS_S3_BUCKET_REGION=os.getenv('AWS_S3_BUCKET_REGION')
AWS_S3_BUCKET_NAME=os.getenv('AWS_S3_BUCKET_NAME')
AWS_ACCESS_KEY=os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY=os.getenv('AWS_SECRET_ACCESS_KEY')

def s3_connection():
    '''
    s3 bucket에 연결
    :return: 연결된 s3 객체
    '''
    try:
        s3 = boto3.client(
            service_name='s3',
            region_name=AWS_S3_BUCKET_REGION,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
    except Exception as e:
        print(e)
        exit(ERROR_S3_CONNECTION_FAILED)
    else:
        print("s3 bucket connected!")
        return s3

def s3_put_object(s3, bucket, filepath, access_key):
    '''
    s3 bucket에 지정 파일 업로드
    :param s3: 연결된 s3 객체(boto3 client)
    :param bucket: 버킷명
    :param filepath: 파일 위치
    :param access_key: 저장 파일명
    :return: 성공 시 True, 실패 시 False 반환
    '''
    try:
        s3.upload_file(filepath, bucket, access_key)
    except Exception as e:
        print(e)
        return False
    return True
    
def s3_get_object(s3, bucket, object_name, file_name):
    '''
    s3 bucket에서 지정 파일 다운로드
    :param s3: 연결된 s3 객체(boto3 client)
    :param bucket: 버킷명
    :param object_name: s3에 저장된 object 명
    :param file_name: 저장할 파일 명(path)
    :return: 성공 시 True, 실패 시 False 반환
    '''
    try:
        s3.download_file(bucket, object_name, file_name)
        print("done")
    except Exception as e:
        print(e)
        return False
    
    return True

def s3_get_alldataset(s3,bucket):
    #모든 훈련용 데이터 다운
    FL=flasklogin()
    #db연결해서 사람 수 받아야됨
    usernumber=FL.usernum_check()-1
    print(usernumber)
    for i in range(usernumber):
        
        objectdir1="./image/dataset/test/"+str(i)
        if not os.path.exists(objectdir1):
            os.makedirs(objectdir1)
        for j in range(3):
            object_test_name="signup/dataset/test/"+str(i)+"/"+str(j)+".jpg"
            file_test_name="./image/dataset/test/"+str(i)+"/"+str(j)+".jpg"
            if os.path.exists(file_test_name):
                os.remove(file_test_name)
            try:
                s3.download_file(bucket, object_test_name, file_test_name)
                print(str(i)+" "+str(j)+" done")
            except Exception as e:
                print(str(i)+str(j)+e)
                return False
            
        objectdir2="./image/dataset/train/"+str(i)
        if not os.path.exists(objectdir2):
            os.makedirs(objectdir2)
        for q in range(7):
            object_train_name="signup/dataset/train/"+str(i)+"/"+str(q)+".jpg"
            file_train_name="./image/dataset/train/"+str(i)+"/"+str(q)+".jpg"
            if os.path.exists(file_train_name):
                os.remove(file_train_name)
            try:
                s3.download_file(bucket, object_train_name, file_train_name)
                print(str(i)+" "+str(q)+" done")
            except Exception as e:
                print(str(i)+" "+str(q))
                return False    
     
    return True

def s3_get_signupuser_dataset(s3,bucket):
    #이제 회원가입할 사람 1명만 s3에서 사진 받기
    FL=flasklogin()
    #db연결해서 사람 수 받아야됨, 마지막 사람+1이 회원가입자리
    usernumber=FL.usernum_check()
    
        
    objectdir1="./image/dataset/test/"+str(usernumber)
    if not os.path.exists(objectdir1):
        os.makedirs(objectdir1)
    for j in range(3):
        object_test_name="signup/dataset/test/"+str(usernumber)+"/"+str(j)+".jpg"
        file_test_name="./image/dataset/test/"+str(usernumber)+"/"+str(j)+".jpg"
        if os.path.exists(file_test_name):
            os.remove(file_test_name)
        try:
            s3.download_file(bucket, object_test_name, file_test_name)
            print(str(usernumber)+" "+str(j)+" done")
        except Exception as e:
            print(str(usernumber)+str(j)+e)
            return False
            
    objectdir2="./image/dataset/train/"+str(i)
    if not os.path.exists(objectdir2):
        os.makedirs(objectdir2)
    for q in range(7):
        object_train_name="signup/dataset/train/"+str(usernumber)+"/"+str(q)+".jpg"
        file_train_name="./image/dataset/train/"+str(usernumber)+"/"+str(q)+".jpg"
        if os.path.exists(file_train_name):
            os.remove(file_train_name)
        try:
            s3.download_file(bucket, object_train_name, file_train_name)
            print(str(usernumber)+" "+str(q)+" done")
        except Exception as e:
            print(str(usernumber)+" "str(q)+e)
            return False    
     
    return True