from pydantic import BaseModel, Field


class user(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
