from pydantic import BaseModel, field_validator, field_serializer
from uuid import UUID


class MonitoringInputRequest(BaseModel):
    user_id: str
    input_text: str

    @field_validator("user_id", mode="before")
    def transform_id_to_str(cls, value) -> str:
        return str(value)


class MonitoringInputResponse(BaseModel):
    mode: str
    request_id: UUID

    @field_serializer("request_id")
    def request_id_serialize(request_id: UUID):
        return str(request_id)


class MonitoringOutputRequest(BaseModel):
    request_id: UUID
    output_text: str

    @field_serializer("request_id")
    def request_id_serialize(request_id: UUID):
        return str(request_id)


class MonitoringOutputResponse(BaseModel):
    reject_flg: bool | None
