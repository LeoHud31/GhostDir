import time
import asyncio

class RateLimiter:
    def __init__(self, requests_per_second: float):
        self.delay = 1.0 / requests_per_second
        self.last_request = time.time()

    async def wait(self):
        now = time.time()
        elapsed = now - self.last_request
        if elapsed < self.delay:
            asyncio.sleep(self.delay - elapsed)
        self.last_request = time.time()