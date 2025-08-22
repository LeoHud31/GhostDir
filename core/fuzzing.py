import httpx
import asyncio
from typing import List, Dict
from urllib.parse import urljoin

async def fetch_url(base_url: str, wordlist: List[str],status_filters: List[int] = None) -> Dict[str, int]:
    if not base_url.endswith('/'):
        base_url += '/'

    results = {}
    async with httpx.AsyncClient(follow_redirects=True) as client:
        for word in wordlist:
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
            
    return results