from loguru import logger

from griff.appli.event.event import Event
from griff.appli.event.event_middleware import EventMiddleware
from griff.appli.message.message_middleware import MessageContext


class AppEventLoggerMiddleware(EventMiddleware):
    async def dispatch(
        self, message: Event, context: MessageContext | None = None
    ) -> None:
        logger.info(f"dispatch app event: {message.short_classname()}")
        logger.debug(message.model_dump())
        await self._next.dispatch(message, context)
