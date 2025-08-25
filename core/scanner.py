import httpx
from typing import List, Dict, Union
from Utils.rate_limiter import RateLimiter


async def scan_url(base_url: str, method: str = 'GET', 
                    response_filters: List[str] = None, 
                    requests_per_second: float = 10) -> Dict[str, Dict[str, Union[int, float, str]]]:
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
        await rate_limiter.wait()

        try:
            if method.upper() == 'GET':
                response = await client.get(base_url)
            elif method.upper() == 'HEAD':
                response = await client.head(base_url)
            else:
                raise ValueError("Unsupported HTTP method. Use 'GET' or 'HEAD'.")

            status_code = response.status_code
            content_length = len(response.content)
            response_time = response.elapsed.total_seconds()

            if response_filters is None or str(status_code) in response_filters or str(content_length) in response_filters:
                results[base_url] = {
                    'status_code': status_code,
                    'content_length': content_length,
                    'response_time': response_time
                }
                print(f"Found: {base_url} (Status: {status_code}, Length: {content_length}, Time: {response_time:.2f}s)")

        except httpx.RequestError as e:
            print(f"Request error for {base_url}: {str(e)}")
        except httpx.TimeoutException:
            print(f"Timeout error for {base_url}")
        except httpx.ConnectError:
            print(f"Connection error for {base_url}")
        except Exception as e:
            print(f"Unexpected error for {base_url}: {str(e)}")

    return results