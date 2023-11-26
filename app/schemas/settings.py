from pydantic import BaseModel


class SettingsSchema(BaseModel):
    ninety_days_chat_limit: bool = None
    text_size: str = None
    display: str = None


class UpdateSettingsResponse(BaseModel):
    message: str
    status_code: int


class GetSettingsResponseData(BaseModel):
    ninety_days_chat_limit: bool
    text_size: str
    display: str


class GetSettingsResponse(BaseModel):
    message: str
    status_code: int
    data: GetSettingsResponseData
