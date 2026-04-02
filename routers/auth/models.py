from pydantic import BaseModel


class UserModel(BaseModel):
    username: str
    password: str


class responseTokenModel(BaseModel):
    access_token: str
    token_type: str
