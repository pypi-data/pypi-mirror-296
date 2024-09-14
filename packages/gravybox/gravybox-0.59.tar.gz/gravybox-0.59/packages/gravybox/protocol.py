from pydantic import BaseModel


class GravyboxRequest(BaseModel):
    pass


class GravyboxResponse(BaseModel):
    success: bool
    error: str = ""
    content: dict | None = None


class LinkRequest(GravyboxRequest):
    trace_id: str


class LinkResponse(GravyboxResponse):
    pass
