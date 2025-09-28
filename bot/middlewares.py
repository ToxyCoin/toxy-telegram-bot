from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable

class ConfigMiddleware(BaseMiddleware):
    def __init__(self, config):
        super().__init__()
        self.config = config

    async def __call__(
        self,
        handler: Callable[[Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any]
    ) -> Any:
        data["config"] = self.config
        return await handler(event, data)
