from typing import TypedDict
from typing import NotRequired


class ChatState(TypedDict):

    message: str

    task_type: NotRequired[str]

    confidence: NotRequired[float]

    response: NotRequired[str]

    metadata: NotRequired[dict]