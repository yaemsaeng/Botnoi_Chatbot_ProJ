from fastapi import APIRouter
from config.db import collection
import firebase_admin
from firebase_admin import credentials, storage
import base64
from model.models import insert_base64,insert_chat_name,update_chat_name
import requests
from datetime import datetime

Router = APIRouter()

cred = credentials.Certificate("./firebase/chatbotnoipdf-firebase-adminsdk-kqkcv-6855ab9086.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'chatbotnoipdf.appspot.com'})
bucket = storage.bucket()

# @Router.get("/")
# def read_root():
#     return  "Hello Welcome to my Chatbot PDF"

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
async def get_chat_response(query: str, customer_id: str):
    url = f"https://mekhav-2e2xbtpg2q-uc.a.run.app/chatgptresponse?query={query}&customer_id={customer_id}"
    response = requests.get(url)
    json_data = response.json()
    return json_data

@Router.get("/all_chat_name", tags=["all_chat_name"])
async def all_chat_histoy(customer_id: str):
    # ดึงข้อมูลทั้งหมดจากเอกสารที่มี customer_id เป็น "1234"
    result = collection.find({"customer_id": customer_id}, {"chat_name": 1})

    # สร้างรายการว่างเพื่อเก็บ chat_history
    all_chat_name = []

    # วนลูปผลลัพธ์และเพิ่ม chat_history เข้าไปในรายการ
    for doc in result:
        chat_history = doc.get("chat_name")
        all_chat_name.append(chat_history)

    return {"all_chat_name": all_chat_name}


@Router.get("/show_chat_history", tags=["show_chat_history"])
async def all_chat_histoy(customer_id: str,chat_name:str):
    result = collection.find({"customer_id": customer_id, "chat_name": chat_name})

    show_chat_history = []

    for doc in result:
        chat_history = doc.get("chat_history")
        show_chat_history.append(chat_history)

    return show_chat_history

@Router.post("/upload_NewChat", tags=["upload_NewChat"])
async def upload_data(data: insert_chat_name):
    collection.insert_one(dict(data))
    

@Router.post("/insert_Chat_history", tags=["insert_Chat_history"])
async def insert_Chat_history(chat_name:str,message_user:str,message_bot) :

    # สร้างเวลาปัจจุบัน
    current_timestamp = datetime.now().isoformat()
    # ส่วนที่ต้องการเพิ่ม
    chat_history_update = {
        "message_user": message_user,
        "message_bot": message_bot,
         "timestamp": current_timestamp
    }
    document = collection.find_one({"chat_name": chat_name})
    if document:#ถ้ามีข้อมูล
        # หาดัชนีใหม่ที่ต้องการสร้าง
        new_index = str(len(document.get("chat_history", {})))

        # อัปเดตเอกสาร
        result = collection.update_one(
            {"chat_name": chat_name},
            {"$set": {"chat_history." + new_index: chat_history_update}}
        )

    # ตรวจสอบว่ามีการอัปเดตสำเร็จหรือไม่
    if result.modified_count == 1:
        return {"message": "Chat history updated"}
    else:
        return {"message": "Chat not found"}


@Router.put("/update_chat_name", tags=["data_update"])
async def update_chat_name(data:update_chat_name,customer_id: str,chat_name:str):
    collection.find_one_and_update(
        {
          "customer_id": customer_id, 
           "chat_name": chat_name
        }, 
        {
         "$set": dict(data)
        })

@Router.delete("/delete" ,tags=["data_delete"])
async def delete(customer_id: str,chat_name:str):
    collection.find_one_and_delete({"customer_id": customer_id, "chat_name": chat_name})
    

