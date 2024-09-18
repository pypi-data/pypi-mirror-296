from typing import Type

from injector import Injector, Binder, singleton

from griff.appli.event.event_bus import EventBus
from griff.appli.message.message_bus import ListMiddlewares
from griff.appli.message.message_middleware import MessageMiddleware
from griff.infra.registry.meta_registry import MetaEventHandlerRegistry
from griff.runtime.components.abstract_runtime_component import (
    RuntimeComponent,
    Runnable,
    InjectBindable,
    import_handlers,
)
from griff.settings.griff_settings import GriffSettings


class EventBusRuntimeComponent(Runnable, InjectBindable, RuntimeComponent):
    def __init__(
        self, settings: GriffSettings, middlewares: list[Type[MessageMiddleware]]
    ):
        self._settings = settings
        self._middlewares = middlewares

    def configure(self, binder: Binder) -> None:
        binder.bind(EventBus, to=EventBus, scope=singleton)

    def initialize(self, injector: Injector):
        event_bus = injector.get(EventBus)
        middlewares: ListMiddlewares = [injector.get(m) for m in self._middlewares]
        for context in self._settings.bounded_contexts:
            import_handlers(
                self._settings.project_dir,
                self._settings.get_event_handlers_path(context),
            )
        handlers = [injector.get(h) for h in MetaEventHandlerRegistry.list_types()]
        event_bus.initialize(handlers, middlewares)

    def clean(self, injector: Injector):
        pass

    def start(self, injector: Injector):
        pass

    def stop(self, injector: Injector):
        pass
