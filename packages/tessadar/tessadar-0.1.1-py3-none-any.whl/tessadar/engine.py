from __future__ import annotations

import tessadar


class Engine:

    def __init__(self, proxy: tessadar.Proxy, scheduler: tessadar.Scheduler):
        self.proxy = proxy
        self.scheduler = scheduler
        self.callbacks = self.proxy.callbacks

    async def run(self):
        for callback in self.callbacks:
            callback.on_start()

        while True:
            batch = await self.scheduler.join()
            if not batch:
                continue

            for callback in self.callbacks:
                callback.on_batch_start(batch)

            futures, arguments = list(zip(*batch))
            try:
                results = await self.proxy._inference(arguments=arguments)
                for future, result in zip(futures, results):
                    future.set_result(result)

                for callback in self.callbacks:
                    callback.on_batch_complete(batch, results)
            except Exception as e:
                for future in futures:
                    future.set_exception(e)

                for callback in self.callbacks:
                    callback.on_exception(e)
