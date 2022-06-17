from typing import Optional
from pydantic import BaseModel, HttpUrl


class WebhookData(BaseModel):
    webhook_event: str
    tracking_number: Optional[str] = None
    title: Optional[str] = None
    tag: Optional[str] = None
    phone_numbers: list
    emails: Optional[list] = []
    courier_tracking_link: Optional[HttpUrl] = None

    raw_data: Optional[dict]
