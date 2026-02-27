from pydantic import BaseModel
from typing import List

class ScriptOutput(BaseModel):
    hook: str
    body: str
    visuals: List[str]
    cta: str