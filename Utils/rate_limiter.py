import time
import asyncio
from typing import Optional

class RateLimiter:
    def __init__(self, requests_per_second: float):
        self.rate = requests_per_second
        self.last_request = 0
        self.delay = 1.0 / requests_per_second

    async def wait(self):
        now = time.time()
        elapsed = now - self.last_request
        if elapsed < self.delay:
            await asyncio.sleep(self.delay - elapsed)
        self.last_request = time.time()