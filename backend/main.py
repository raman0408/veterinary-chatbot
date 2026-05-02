from fastapi import FastAPI
from backend.routes import chat, login

app = FastAPI()

app.include_router(login.router)
app.include_router(chat.router)

