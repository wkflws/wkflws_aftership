from typing import Any, Optional

import json

from wkflws.events import Event
from wkflws.http import http_method, Request, Response
from wkflws.logging import getLogger
from wkflws.triggers.webhook import WebhookTrigger
from .schemas.webhook import WebhookData

from . import __identifier__, __version__

logger = getLogger("wkflws_aftership.trigger")
logger.setLevel(10)


async def process_webhook_request(
    request: Request, response: Response
) -> Optional[Event]:
    """Accept and process an HTTP request returning a event for the bus."""
    try:
        identifier = request.headers["aftership-hmac-sha256"]
    except KeyError:
        raise ValueError("'aftership-hmac-sha256' undefined!") from None

    data = json.loads(request.body)
    tracking_data = data.get("msg")

    webhook_data = WebhookData(
        webhook_event=data.get("event"),
        tracking_number=tracking_data.get("tracking_number", None),
        title=tracking_data.get("title", None),
        tag=tracking_data.get("tag", None),
        phone_numbers=tracking_data.get("smses", []),
        emails=tracking_data.get("emails", []),
        courier_tracking_link=tracking_data.get("courier_tracking_link", None),
        raw_data=data,
    )

    logger.info(f"Received Aftership webhook request: {identifier}")

    return Event(identifier, request.headers, webhook_data.dict())


async def accept_event(event: Event) -> tuple[Optional[str], dict[str, Any]]:
    """Accept and process data from the event bus."""

    data = event.data

    data["aftership-hmac-sha256"] = event.metadata["aftership-hmac-sha256"]
    event_type = data.get("webhook_event")
    event_tag = data.get("tag")

    logger.info(
        f"Processing Aftership webhook as '{event_type}' event and tag '{event_tag}'"
    )

    match event_type:
        case "tracking_update":
            return "wkflws_aftership.tracking_update", event.data
        case _:
            logger.error(
                f"Received unsupported Aftership event type '{event_type}' "
                f"(id:{event.identifier})"
            )
            return None, {}


my_webhook_trigger = WebhookTrigger(
    client_identifier=__identifier__,
    client_version=__version__,
    process_func=accept_event,
    routes=(
        (
            (http_method.POST,),
            "/webhook/",
            process_webhook_request,
        ),
    ),
)
