import time
import asyncio

def RateLimiter(self):
    now = time.time()
    elapsed = now - self.last_request
    if elapsed < self.delay:
        asyncio.sleep(self.delay - elapsed)
    self.last_request = time.time()