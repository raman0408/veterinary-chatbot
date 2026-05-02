from fastapi import APIRouter
from backend.services.memory import load_history

router = APIRouter()

@router.post("/login")
def login(data: dict):
    phone = data.get("phone")

    history = load_history(phone)

    return {
        "history": history
    }