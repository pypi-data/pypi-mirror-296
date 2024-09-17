from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class LytixProxyResponse(BaseModel):
    modelName: str
    messages: List[Dict[str, str]]
    maxTokens: Optional[int] = None
    temperature: Optional[float] = None
    inputTokens: Optional[int] = None
    outputTokens: Optional[int] = None
    totalTokens: Optional[int] = None
