from fastapi import FastAPI
from route.routes import Router
from fastapi.middleware.cors import CORSMiddleware
from route.routes_login_Google import app

from route.routes_login_Google import app as google_app
app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(Router)
app.include_router(google_app)