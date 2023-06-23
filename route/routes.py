from fastapi import APIRouter,UploadFile,File
import firebase_admin
from firebase_admin import credentials, storage
import base64
from model.models import insert_base64
# import random

Router = APIRouter()

cred = credentials.Certificate("./firebase/chatbotnoipdf-firebase-adminsdk-kqkcv-6855ab9086.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'chatbotnoipdf.appspot.com'})
bucket = storage.bucket()

@Router.get("/")
def read_root():
    return  "Hello Welcome to my Chatbot PDF"


@Router.post("/Upload_PDF_base64", tags=["Upload PDF(base64)"])
async def create_upload_file(data: insert_base64):
    # ดีโค้ดไฟล์จาก base64 เป็นไฟล์ PDF
    file_base64 = data.base64
    file_data = base64.b64decode(file_base64)
    
    # อัปโหลดไฟล์ PDF เข้าสู่ Firebase Storage
    randoms = file_base64[11 : 21]
    # randoms = random.choices('abcdefghijklmnopqrstuvwxyz', k = 10)
    blob = bucket.blob(f"pdf/{randoms}.pdf")
    blob.upload_from_string(file_data, content_type='application/pdf')
    
    # กำหนดสิทธิ์ในการเข้าถึงไฟล์ใน Firebase Storage ให้เป็นสาธารณะ
    blob.make_public()
    url = blob.public_url
    
    return {'message': 'Upload successful', 'url': url}



#----------------------------------------------------------------------------------------------------------------------------

# @Router.post("/Upload_PDF_File", tags=["Upload PDF"]) 
# async def create_upload_file(file: UploadFile = File(media_type='application/pdf')):
#     bucket = storage.bucket()
#     blob = bucket.blob("pdf/"+file.filename)
#     blob.upload_from_file(file.file, content_type='application/pdf')
#     # กำหนดสิทธิ์ในการเข้าถึง file ที่อยู๋ใน firebase ให้เป็นสาธารณะ โดยไม่ต้องใช้ระบบการรับรองตัวตน (authentication) หรือ Access token
#     blob.make_public()
#     # รับ URL สำหรับไฟล์ที่อัปโหลด
#     url = blob.public_url

#     return {'message': 'Upload successful', 'url': url}



# @Router.post("/decode_to_PDF")
# async def create_upload_file(file_base64: str):
#     decoded_data = base64.b64decode(file_base64)  # ถอดรหัส Base64

#     with open("test.pdf", "wb") as file:
#         file.write(decoded_data)

#     return "Hello Welcome to my Chatbot PDF"



# @Router.post("/Upload_test")
# async def create_upload_file(file_base64: str):
#     # ดีโค้ดไฟล์จาก base64 เป็นไฟล์ PDF
#     file_data = base64.b64decode(file_base64)
    
#     # อัปโหลดไฟล์ PDF เข้าสู่ Firebase Storage
#     blob = bucket.blob("pdf/file.pdf")
#     blob.upload_from_string(file_data, content_type='application/pdf')
    
#     return {"message": "ไฟล์ PDF ถูกอัปโหลดสำเร็จ"}



