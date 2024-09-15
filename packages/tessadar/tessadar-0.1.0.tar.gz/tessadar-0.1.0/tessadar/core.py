from __future__ import annotations

import abc
import asyncio
import threading
from concurrent.futures import Future
from typing import Any, Iterable, TypeVar, Generic

T = TypeVar("T")

U = TypeVar("U")


class Proxy(Generic[T, U], abc.ABC):
    def __init__(self, batch_size: int = 64):
        self.coordinator = Coordinator(proxy=self, batch_size=batch_size)

    @abc.abstractmethod
    async def _inference(self, arguments: Iterable[T]) -> Iterable[U]:
        pass

    async def inference(self, argument: T) -> U:
        return await self.coordinator.schedule(argument)


class Engine:

    def __init__(self, scheduler: Scheduler, proxy: Proxy):
        self.scheduler = scheduler
        self.proxy = proxy

    async def run(self):
        while True:
            batch = await self.scheduler.join()
            if not batch:
                continue

            futures, arguments = list(zip(*batch))
            results = await self.proxy._inference(arguments=arguments)
            for future, result in zip(futures, results):
                future.set_result(result)


class Scheduler:

    def __init__(self, batch_size: int = 64):
        if batch_size < 1:
            raise ValueError("Not allowed batch size under 1.")

        self.batch_size = batch_size
        self.queue = asyncio.Queue()

    async def schedule(self, future: asyncio.Future, argument: Any):
        await self.queue.put((future, argument))

    async def join(self) -> list[tuple[asyncio.Future, Any]]:
        argument = await self.queue.get()
        batch = [argument]
        for _ in range(self.batch_size - 1):
            if self.queue.empty():
                break
            args = self.queue.get_nowait()
            batch.append(args)
        return batch


class Coordinator:

    def __init__(self, proxy: Proxy, batch_size: int = 64):
        self.proxy = proxy

        self.scheduler = Scheduler(batch_size=batch_size)
        self.engine = Engine(scheduler=self.scheduler, proxy=self.proxy)

        self.engine_event_loop = asyncio.new_event_loop()
        self.engine_thread = threading.Thread(target=self.run_engine, daemon=True)
        self.engine_thread.start()

    def run_engine(self):
        if threading.current_thread() is threading.main_thread():
            raise Exception("run_engine must not be called from the main thread")
        asyncio.set_event_loop(self.engine_event_loop)
        self.engine_event_loop.create_task(self.engine.run())
        self.engine_event_loop.run_forever()

    async def schedule(self, argument: Any) -> Any:
        # Use concurrent.futures.Future for thread-safe communication
        future = Future()
        # Schedule the coroutine in the engine's event loop
        coro = self.scheduler.schedule(future, argument)
        asyncio.run_coroutine_threadsafe(coro, self.engine_event_loop)
        # Wrap the concurrent.futures.Future to an asyncio.Future
        wrapped_future = asyncio.wrap_future(future)
        # Await the result in the main event loop
        result = await wrapped_future
        return result
