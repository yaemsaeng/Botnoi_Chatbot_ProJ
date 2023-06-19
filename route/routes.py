from fastapi import APIRouter

Router = APIRouter()

@Router.get("/")
def read_root():
    return  "Hello Welcome to my Chatbot PDF"
