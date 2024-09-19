from multiprocessing import Queue
from uuid import UUID

from edri.api import Middleware
from edri.api.broker import Broker
from edri.api.listener import Listener
from edri.abstract import ManagerBase
from edri.config.setting import TOKEN_LENGTH
from edri.dataclass.event import Event
from edri.router import Router
from edri.router.connector import Connector
from edri.utility.manager import Store
from edri.utility.manager.scheduler import Scheduler, Job


class EDRI:
    def __init__(self) -> None:
        self.router_queue: "Queue[Event]" = Queue()
        self.components: set[ManagerBase] = set()
        self.store: Store
        self.scheduler: Scheduler
        self.api: Listener
        self.api_broker: Broker
        self.connector: Connector
        self.router: Router

    def add_component(self, component: ManagerBase) -> None:
        self.components.add(component)

    def start_store(self) -> None:
        self.store = Store(self.router_queue)
        self.store.start()

    def start_scheduler(self, jobs: list[Job] | None = None) -> None:
        if not jobs:
            jobs = []
        self.scheduler = Scheduler(self.router_queue, jobs)
        self.scheduler.start()

    def api_broker_start(self, middlewares: list[Middleware] = None) -> None:
        if middlewares is None:
            middlewares = []
        self.api_broker = Broker(self.router_queue, Queue(), middlewares)
        self.api_broker.start()

    def start_api(self, middlewares: list[Middleware] | None = None) -> None:
        if middlewares is None:
            middlewares = []
        if not hasattr(self, "api_broker"):
            self.api_broker_start(middlewares=middlewares)
        else:
            self.api_broker.middlewares = middlewares
        self.api = Listener(self.api_broker.api_broker_queue, middlewares)
        self.api.start()

    def start_connector(self, router_id: UUID | None = None) -> None:
        self.connector = Connector(self.router_queue, router_id)
        self.connector.start()

    def run(self) -> None:
        self.router = Router(self.router_queue, self.components)
        for component in self.components:
            component.start(self.router_queue)
        try:
            self.router.run()
        except KeyboardInterrupt:
            self.router.quit()
            if hasattr(self, "connector") and self.connector:
                self.connector.quit()

__all__ = ["EDRI"]