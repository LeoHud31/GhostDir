import httpx
from typing import List, Dict, Union
import asyncio
from Utils.rate_limiter import RateLimiter
import dns.resolver


def clean_domain(domain: str) -> str:
    domain = domain.replace('http://', '').replace('https://', '')
    domain = domain.replace('www.', '')
    domain = domain.split('/')[0]
    domain = domain.split(':')[0]
    return domain.strip()


async def scan_url(base_url: str, 
                    method: str = 'GET', 
                    response_filters: List[str] = None,
                    enable_subdomain_scan: bool = False, 
                    requests_per_second: float = 10,
                    wordlist: List[str] = None)-> Dict[str, Dict[str, Union[int, float, str]]]:
    
    domain = clean_domain(base_url)
    if not domain or '.' not in domain:
        print("Invalid domain name provided.")
        return {}
    

    results = {}
    rate_limiter = RateLimiter(requests_per_second)

    limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
    timeout = httpx.Timeout(timeout=10.0)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }

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
                    'response_time': response_time,

                }
                print(f"Found: {domain} (Status: {status_code}, Length: {content_length}, Time: {response_time:.2f}s)")

        except httpx.RequestError as e:
            print(f"Request error for {base_url}: {str(e)}")
        except httpx.TimeoutException:
            print(f"Timeout error for {base_url}")
        except httpx.ConnectError:
            print(f"Connection error for {base_url}")
        except Exception as e:
            print(f"Unexpected error for {base_url}: {str(e)}")

        if enable_subdomain_scan and wordlist:
            print(f"Starting subdomain scan for {domain}...")
            print("=" * 50)

            total = len(wordlist)
            found_count = 0

            for i, word in enumerate(wordlist, 1):
                await rate_limiter.wait()
                
                try:
                    full_domain = f"{word}.{domain}"
                    
                    test_url = f"https://{full_domain}"
                        
                    try:
                        if method.upper() == 'GET':
                            response = await client.get(test_url)
                        elif method.upper() == 'HEAD':
                            response = await client.head(test_url)
                        else:
                            print("Unsupported HTTP method. Use 'GET' or 'HEAD'.")

                        status_code = response.status_code
                        content_length = len(response.content)
                        response_time = response.elapsed.total_seconds()

                        if response_filters is None or str(status_code) in response_filters or str(content_length) in response_filters:
                            results[test_url] = {
                                'status_code': status_code,
                                'content_length': content_length,
                                'response_time': response_time,
                            }
                            found_count += 1
                            print(f"Found: {full_domain} (Status: {status_code}, Length: {content_length}, Time: {response_time:.2f}s)")

                    except:
                        try:
                            test_url = f"http://{full_domain}"
                            if method.upper() == 'GET':
                                response = await client.get(test_url)
                            elif method.upper() == 'HEAD':
                                response = await client.head(test_url)
                            else:
                                print("Unsupported HTTP method. Use 'GET' or 'HEAD'.")

                            status_code = response.status_code
                            content_length = len(response.content)
                            response_time = response.elapsed.total_seconds()

                            
                            if response_filters is None or str(status_code) in response_filters or str(content_length) in response_filters:
                                results[test_url] = {
                                    'status_code': status_code,
                                    'content_length': content_length,
                                    'response_time': response_time,
                                }
                                found_count += 1
                                print(f"Found: {full_domain} (Status: {status_code}, Length: {content_length}, Time: {response_time:.2f}s)")
                        except:
                            pass
                except Exception as e:
                    print(f"Error scanning {word}.{domain}: {str(e)}")

            print(f"Subdomain scan completed. Found {found_count} active subdomains out of {total} tested.")
            print("=" * 50)

    return results