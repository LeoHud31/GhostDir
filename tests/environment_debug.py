import asyncio
import dns.resolver
import socket
import sys
import platform
from core.scanner import resolve_subdomain

async def environment_debug():
    """Test for environment-specific DNS issues"""
    
    print("🔧 ENVIRONMENT DEBUG")
    print("=" * 50)
    
    # System info
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"DNS resolver module: {dns.resolver.__file__}")
    
    # Test domain and subdomain
    domain = "testphp.vulnweb.com"
    subdomain = "www"  # Change to one of your known subdomains
    full_domain = f"{subdomain}.{domain}"
    
    print(f"\n🎯 Testing: {full_domain}")
    print("-" * 30)
    
    # Test 1: System DNS (what works)
    print("1️⃣ System DNS (socket):")
    try:
        ip = socket.gethostbyname(full_domain)
        print(f"   ✅ {full_domain} -> {ip}")
    except Exception as e:
        print(f"   ❌ {full_domain} -> {e}")
    
    # Test 2: Default DNS resolver
    print("\n2️⃣ Default DNS resolver:")
    try:
        resolver = dns.resolver.Resolver()
        print(f"   Default nameservers: {resolver.nameservers}")
        answers = resolver.resolve(full_domain, 'A')
        ips = [str(answer) for answer in answers]
        print(f"   ✅ {full_domain} -> {ips}")
    except Exception as e:
        print(f"   ❌ {full_domain} -> {e}")
    
    # Test 3: Your scanner's DNS setup (what might be failing)
    print("\n3️⃣ Scanner DNS setup (Google DNS):")
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ['8.8.8.8', '1.1.1.1', '8.8.4.4', '1.0.0.1']
        resolver.timeout = 5
        resolver.lifetime = 5
        print(f"   Using nameservers: {resolver.nameservers}")
        print(f"   Timeout: {resolver.timeout}s")
        
        answers = resolver.resolve(full_domain, 'A')
        ips = [str(answer) for answer in answers]
        print(f"   ✅ {full_domain} -> {ips}")
    except dns.exception.Timeout:
        print(f"   ⏰ TIMEOUT: {full_domain}")
        print("   ^ This might be your issue!")
    except dns.resolver.NXDOMAIN:
        print(f"   ❌ NXDOMAIN: {full_domain}")
    except Exception as e:
        print(f"   ❌ {full_domain} -> {type(e).__name__}: {e}")
    
    # Test 4: Your actual resolve_subdomain function
    print("\n4️⃣ Your resolve_subdomain function:")
    try:
        result = await resolve_subdomain(subdomain, domain)
        if result:
            print(f"   ✅ {result['domain']} -> {result['ips']}")
        else:
            print(f"   ❌ {subdomain}.{domain} -> None")
            print("   ^ Your function returned None!")
    except Exception as e:
        print(f"   ❌ {subdomain}.{domain} -> {type(e).__name__}: {e}")
    
    # Test 5: Network connectivity to DNS servers
    print("\n5️⃣ DNS server connectivity:")
    dns_servers = ['8.8.8.8', '1.1.1.1', '8.8.4.4']
    for dns_server in dns_servers:
        try:
            sock = socket.create_connection((dns_server, 53), timeout=3)
            sock.close()
            print(f"   ✅ Can connect to {dns_server}:53")
        except Exception as e:
            print(f"   ❌ Cannot connect to {dns_server}:53 -> {e}")
    
    print("\n" + "=" * 50)
    print("🔍 DIAGNOSIS:")
    print("If tests 1-2 work but 3-4 fail, it's likely:")
    print("• Firewall blocking external DNS servers")
    print("• Corporate network filtering")
    print("• DNS timeout issues")
    print("• VPN interference")

if __name__ == "__main__":
    asyncio.run(environment_debug())