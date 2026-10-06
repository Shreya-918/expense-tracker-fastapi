from pydantic import BaseModel

class ApiResponse(BaseModel):
    status: str
    message: str
    success: bool
    data: dict | None = None
