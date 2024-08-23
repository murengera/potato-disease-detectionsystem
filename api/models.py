
from pydantic import BaseModel

class SignUpSchema(BaseModel):
    email:str
    password:str
    class Config:
        schema_extra={
            "example":{
                "email":"sample@gmail.com",
                "password":"sample"
            }
        }

class LoginSchema(BaseModel):
    email:str
    password:str

    class Config:
        schema_extra = {
            "example": {
                "email": "sample@gmail.com",
                "password": "sample"
            }
        }