from fastapi import FastAPI
from backend.routes import chat, login
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(login.router)
app.include_router(chat.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
