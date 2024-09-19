from dataclasses import dataclass, fields
from enum import Enum
from http import HTTPMethod
from inspect import isclass
from pathlib import Path
from types import NoneType
from typing import Type, get_origin, get_args, Union

from typeguard import check_type

from edri.api.extensions.url_prefix import PrefixBase
from edri.config.constant import ApiType
from edri.dataclass.event import EventHandlingType, _event, Event
from edri.utility.function import camel2snake


class Cookie:
    def __init__(self, name: str):
        self.name = name


class Header:
    def __init__(self, name: str):
        self.name = name.lower()


class Scope:
    def __init__(self, name: str):
        self.name = name.lower()


@dataclass
class ApiEvent:
    url: str
    resource: str
    handling: EventHandlingType
    event: Type[Event]
    exclude: list[ApiType]
    cookies: dict[str, str]
    headers: dict[str, str]
    scope: dict[str, str]
    template: str | None


api_events: list[ApiEvent] = list()
allowed_types = (str, int, float, bool, Path)


def api(cls=None, /, *, init=True, repr=True, eq=True, order=False,
        unsafe_hash=False, frozen=False, match_args=True,
        kw_only=False, slots=False, weakref_slot=None, url=None, resource=None, handling=None, exclude=None, template=None,
        shareable=False):
    def wrapper(cls):
        cookies = {}
        headers = {}
        scope = {}
        url_prefix = url if url else f"/{camel2snake(cls.__name__)}"

        is_event_subclass = False
        prefixes = set()
        for base in reversed(cls.__bases__):
            if is_event_subclass or issubclass(base, Event):
                is_event_subclass = True

            if issubclass(base, PrefixBase):
                prefixes.add(base)
                url_prefix = base.prefix + url_prefix
        if not is_event_subclass:
            cls = type(cls.__name__, (Event, *tuple(base for base in cls.__bases__ if base not in prefixes)), dict(cls.__dict__))
        else:
            cls = type(cls.__name__, tuple(base for base in cls.__bases__ if base not in prefixes), dict(cls.__dict__))
        cls.__annotations__.pop('method', None)
        dataclass = _event(cls, init=init, repr=repr, eq=eq, order=order, unsafe_hash=unsafe_hash,
                           frozen=frozen, match_args=match_args, kw_only=kw_only, slots=slots,
                           weakref_slot=weakref_slot, shareable=shareable)

        for name, field in ((f.name, f) for f in fields(dataclass)):
            if name.startswith("_"):
                continue
            if name == "response" or name == "method":
                pass
            elif isinstance(field.default, Cookie):
                cookies[name] = field.default.name
            elif isinstance(field.default, Header):
                headers[name] = field.default.name
            elif isinstance(field.default, Scope):
                scope[name] = field.default.name
            elif field.type not in allowed_types and (isclass(field.type) and not issubclass(field.type, Enum)):
                item_type = get_origin(field.type)
                item_args = get_args(field.type)
                if item_type == Union:
                    position = 0 if item_args.index(NoneType) == 1 else 1
                    item_type = item_args[position]
                    if item_type in (list, tuple):
                        item_args = item_type.__args__
                if item_type in (list, tuple):
                    if len(item_args) > 1:
                        raise TypeError("Only one child type is allowed got %s" % len(item_args))
                    elif item_args[0] not in allowed_types and not hasattr(item_args[0], "fromisoformat"):
                        raise TypeError("%s cannot be used as a type for API event" % item_args[0])
                elif item_type not in allowed_types and not hasattr(field.type, "fromisoformat"):
                    raise TypeError("%s cannot be used as a type for API event" % field.type)

        if dataclass.method is None:
            if exclude is None or ApiType.REST not in exclude or ApiType.HTML not in exclude:
                raise ValueError("Any method is required")
        else:
            check_type(dataclass.method, HTTPMethod)

        if template is None and (exclude is None or ApiType.HTML not in exclude):
            raise ValueError("For HTML api template has to be specified")

        api_events.append(ApiEvent(
            url_prefix,
            resource if resource else camel2snake(dataclass.__name__).replace("_", "-"),
            handling if handling else EventHandlingType.SPECIFIC,
            dataclass,
            exclude if exclude is not None else [],
            cookies,
            headers,
            scope,
            template))

        return dataclass

    if cls is None:
        return wrapper

    return wrapper(cls)
