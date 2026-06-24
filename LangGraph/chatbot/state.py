from typing import TypedDict, TypedDict

class ChatState(TypedDict):
    message: str
    intent: str
    response: str