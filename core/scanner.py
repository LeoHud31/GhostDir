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

async def resolve_subdomain(subdomain: str, domain: str) -> Dict[str, Union[str, List[str]]]:
    full_domain = f"{subdomain}.{domain}"
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ['8.8.8.8', '1.1.1.1', '8.8.4.4', '1.0.0.1']
        resolver.timeout = 10
        resolver.lifetime = 10


        ips = []
        record_types = []
        
        try:
            answers = resolver.resolve(full_domain, 'A')
            ips.extend([answer.to_text() for answer in answers])
            record_types.append('A')
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
            pass
        
        try:
            answers = resolver.resolve(full_domain, 'AAAA')
            ips.extend([answer.to_text() for answer in answers])
            record_types.append('AAAA')
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
            pass
            
        try:
            answers = resolver.resolve(full_domain, 'CNAME')
            cnames = [answer.to_text() for answer in answers]
            record_types.append('CNAME')
            
            for cname in cnames:
                try:
                    cname_answers = resolver.resolve(cname.rstrip('.'), 'A')
                    ips.extend([answer.to_text() for answer in cname_answers])
                except:
                    ips.append(f"CNAME -> {cname}")
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
            pass

        if ips:
            return {
                'domain': full_domain, 
                'ips': ips,
                'record_types': record_types
            }
        else:
            return None
    
    except dns.resolver.NXDOMAIN:
        print(f"DEBUG: NXDOMAIN for {full_domain}")
        return None
    except dns.exception.Timeout:
        print(f"DNS timeout for {full_domain}")
        return None
    except Exception as e:
        print(f"DNS resolution error for {full_domain}: {str(e)}")
        return None


async def scan_url(base_url: str, 
                    method: str = 'GET', 
                    response_filters: List[str] = None,
                    enable_subdomain_scan: bool = False, 
                    requests_per_second: float = 10,
                    wordlist: List[str] = None)-> Dict[str, Dict[str, Union[int, float, str]]]:
    
    domain = clean_domain(base_url)
    if not domain or '.' not in domain:
        print("Invalid domain name provided.")
    

    results = {}
    rate_limiter = RateLimiter(requests_per_second)

    if enable_subdomain_scan and wordlist:
        print(f"Starting subdomain scan for {domain}...")
        print("=" * 50)

        subdomain_tasks = []
        total = len(wordlist)

        for i, word in enumerate(wordlist, 1):
            await rate_limiter.wait()
            try:
                result = await resolve_subdomain(word, domain)
                if result:
                    subdomain_tasks.append(result)
                    print(f"Found: {result['domain']} -> {', '.join(result['ips'])}")
            except Exception as e:
                print(f"Error resolving {word}.{domain}: {str(e)}")

            if i % 10 == 0:
                print(f"Progress: {i}/{total} ({i/total*100:.2f}%)")

        if subdomain_tasks:
            results['subdomains'] = subdomain_tasks
            print(f"Found {len(subdomain_tasks)} valid subdomains.")
            for sub in subdomain_tasks:
                print(f"{sub['domain']}: {', '.join(sub['ips'])}")
        else:
            print("No valid subdomains found.")

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
                    'response_time': response_time
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

    return results