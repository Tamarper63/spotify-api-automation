from pydantic import BaseModel


class ErrorObject(BaseModel):
    status: int
    message: str


class ErrorResponse(BaseModel):
    error: ErrorObject
