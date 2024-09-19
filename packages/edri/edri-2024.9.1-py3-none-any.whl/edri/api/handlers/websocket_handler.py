from dataclasses import asdict
from http import HTTPStatus
from json import loads, JSONDecodeError, dumps
from typing import Callable, Type, Unpack, TypedDict

from edri.api import Headers
from edri.api.dataclass.api_event import api_events
from edri.api.handlers import BaseHandler
from edri.config.constant import ApiType
from edri.dataclass.event import Event
from edri.utility.function import camel2snake, snake2camel


class ResponseKW(TypedDict):
    headers: Headers


class WebsocketHandler(BaseHandler):

    def __init__(self, scope: dict, receive: Callable, send: Callable, headers: Headers):
        super().__init__(scope, receive, send, headers)
        self.events = {event.resource: event.event for event in api_events if ApiType.WS not in event.exclude}
        self.commands = {event.event: event.resource for event in api_events if ApiType.WS not in event.exclude}
        self.command: str | None = None

    @classmethod
    @property
    def type(cls) -> ApiType:
        return ApiType.WS

    # noinspection PyPropertyDefinition
    async def accept_client(self):
        data = await self.receive()
        if "type" in data and data["type"] == "websocket.connect":
            await self.send({"type": "websocket.accept"})

    async def parse_body(self):
        data = await self.receive()
        if data["type"] == "websocket.receive":
            if data["text"] is not None:
                received_data = data["text"]
            else:
                received_data = data["bytes"].decode("utf-8", errors="replace")
        else:
            self.logger.error("Parse body failed")
            return await self.response_error(HTTPStatus.BAD_REQUEST)
        try:
            self.parameters.update({camel2snake(key): value for key, value in loads(received_data).items()})
        except JSONDecodeError as e:
            self.logger.warning("Cannot process json data", exc_info=e)
            return await self.response_error(HTTPStatus.BAD_REQUEST)
        except Exception as e:
            self.logger.error("Unknown error", exc_info=e)
            return await self.response_error(HTTPStatus.BAD_REQUEST)

    async def get_event_constructor(self) -> tuple[Type[Event], dict] | tuple[None, dict]:
        self.command = self.parameters.pop("command", None)
        if self.command is None:
            raise ResourceWarning("Missing command")
        return self.events.get(self.command, None), self.parameters

    async def response(self, status, data, *args, **kwargs: Unpack[ResponseKW]):
        respond_data = {
            "command": self.commands[data.__class__],

        }
        respond_data.update(asdict(data))
        respond_data.pop("_key")
        respond_data.pop("_switch")
        respond_data.pop("_stream")
        respond_data.pop("methods", None)
        respond_data.pop("_headers", None)
        respond_data.pop("_cookies", None)
        respond_data.pop("_worker", None)
        respond_data.pop("_template", None)
        if respond_data["response"]:
            respond_data["response"]["event_status"] = status
            respond_data["response"].pop("_status")
            respond_data["response"].pop("_error")
            respond_data["response"].pop("_changed")
            respond_data["response"] = {snake2camel(key): value for key, value in respond_data["response"].items() if
                                        not key.startswith("_")}
        else:
            respond_data.pop("response")
        await self.send({"type": "websocket.send", "text": dumps(respond_data)})

    async def response_error(self, status, response: bytes | None = None, *args, **kwargs) -> None:
        pass
