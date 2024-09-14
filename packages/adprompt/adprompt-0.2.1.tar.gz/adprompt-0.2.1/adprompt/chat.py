from typing import Union

from openai.types.chat import ChatCompletion
from pydantic import BaseModel


class ChatResponse(BaseModel):
    result: Union[dict, list] = None
    content: str = None
    completion: ChatCompletion = None
    error_message: str = None
