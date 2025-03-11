from pydantic import BaseModel, EmailStr
from datetime import date

class MessageScheme(BaseModel):
    message: str