from http.cookies import SimpleCookie

from .middleware import Middleware
from .broker import Broker

Headers = dict[str, list[str] | SimpleCookie]
