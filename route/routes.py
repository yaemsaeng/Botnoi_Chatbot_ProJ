from fastapi import APIRouter,UploadFile,File
import firebase_admin
from firebase_admin import credentials, storage
import base64
from model.models import insert_base64
import requests

Router = APIRouter()

cred = credentials.Certificate("./firebase/chatbotnoipdf-firebase-adminsdk-kqkcv-6855ab9086.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'chatbotnoipdf.appspot.com'})
bucket = storage.bucket()

@Router.get("/")
def read_root():
    return  "Hello Welcome to my Chatbot PDF"

@Router.post("/Upload_PDF_base64", tags=["Upload PDF"])
async def create_upload_file(data: insert_base64):
    # ดีโค้ดไฟล์จาก base64 เป็นไฟล์ PDF
    file_base64 = data.base64
    file_data = base64.b64decode(file_base64)
    
    # อัปโหลดไฟล์ PDF เข้าสู่ Firebase Storage
    randoms = file_base64[11 : 21]
    
    blob = bucket.blob(f"pdf/{randoms}.pdf")  #f" " คือ วิธีการสร้างสตริงที่อนุญาตให้แทรกค่าของตัวแปรหรือนิพจน์ลงในสตริงได้อย่างสะดวก ด้วยการใช้เครื่องหมาย {}
    blob.upload_from_string(file_data, content_type='application/pdf')
    
    # กำหนดสิทธิ์ในการเข้าถึงไฟล์ใน Firebase Storage ให้เป็นสาธารณะ
    blob.make_public()
    url = blob.public_url
    
    return {'message': 'Upload successful', 'url': url}

@Router.get("/chatgptresponse", tags=["ChatBot"])
def get_chat_response(query: str, customer_id: str):
    url = f"https://mekhav-2e2xbtpg2q-uc.a.run.app/chatgptresponse?query={query}&customer_id={customer_id}"
    response = requests.get(url)
    json_data = response.json()
    return json_data



