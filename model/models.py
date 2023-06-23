from typing import Optional
from pydantic import BaseModel

class insert_base64(BaseModel):
    base64 : Optional[str]

    class Config:
        schema_extra = {
            "example" : {
                "base64":"base64_text",
            }
        }