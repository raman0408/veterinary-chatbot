from typing import TypedDict, List

class ChatState(TypedDict):
    phone: str
    message: str
    history: List[dict]

    contexts: List[str]
    best_q: float
    best_hq: float

    rewritten_query: str
    is_vague: bool

    response: str
    summary: str