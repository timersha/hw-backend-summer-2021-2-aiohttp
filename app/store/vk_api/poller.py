import asyncio
from asyncio import Task

from app.store.store import Store


class Poller:
    def __init__(self, store: Store) -> None:
        self.store = store
        self.is_running = False
        self.poll_task: Task | None = None

    async def start(self) -> None:
        self.is_running = True
        self.poll_task = asyncio.create_task(self.poll())

    async def stop(self) -> None:
        if not self.poll_task:
            return
        self.is_running = False
        self.poll_task.cancel()
        await asyncio.gather(self.poll_task, return_exceptions=True)

    async def poll(self) -> None:
        while self.is_running:
            await self.store.vk_api.poll()
