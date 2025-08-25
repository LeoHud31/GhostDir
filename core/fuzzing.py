import httpx 
from typing import List, Dict 
from urllib.parse import urljoin 
from Utils.rate_limiter import RateLimiter

async def fetch_url(base_url: str, wordlist: List[str],status_filters: List[int] = None, requests_per_second: float = 10) -> Dict[str, int]:
    base_url = base_url.split('#')[0]
    if not base_url.endswith('/'):
        base_url += '/'

    results = {}
    rate_limiter = RateLimiter(requests_per_second)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }

    limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
    timeout = httpx.Timeout(timeout=10.0)

    async with httpx.AsyncClient(
        follow_redirects=True, 
        headers=headers, 
        limits=limits, 
        timeout=timeout
    ) as client:
        for word in wordlist:
            await rate_limiter.wait()

            target_url = urljoin(base_url, word)

            try:
                response = await client.get(target_url)
                status_code = response.status_code

                if status_filters is None or status_code in status_filters:
                    results[target_url] = status_code
                    print(f"Found: {target_url} (Status: {status_code})")

            except httpx.RequestError as e:
                print(f"Request error for {target_url}: {str(e)}")
                continue
            except httpx.TimeoutException:
                print(f"Timeout error for {target_url}")
                continue
            except httpx.ConnectError:
                print(f"Connection error for {target_url}")
                continue
            except Exception as e:
                print(f"Unexpected error for {target_url}: {str(e)}")
                continue

    return results