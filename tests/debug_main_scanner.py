import asyncio
from core.scanner import resolve_subdomain, clean_domain
import socket

async def debug_scanner_vs_simple():
    """Compare simple socket test vs your scanner's resolve_subdomain function"""
    
    target = "vulnweb.com"
    known_subdomains = ["www", "testphp", "testhtml5"]  # Update these to your actual known ones
    
    print(f"🔍 DEBUGGING: Why scanner doesn't find known subdomains")
    print("=" * 60)
    
    # Clean domain like your scanner does
    cleaned_domain = clean_domain(f"http://{target}")
    print(f"1. Domain cleaning: {target} -> {cleaned_domain}")
    
    for subdomain in known_subdomains:
        full_domain = f"{subdomain}.{cleaned_domain}"
        
        print(f"\n--- Testing: {subdomain}.{cleaned_domain} ---")
        
        # Test 1: Simple socket method (like our working test)
        print("🧪 Simple socket test:")
        try:
            ip = socket.gethostbyname(full_domain)
            print(f"   ✅ Socket: {full_domain} -> {ip}")
            socket_works = True
        except Exception as e:
            print(f"   ❌ Socket: {full_domain} -> {e}")
            socket_works = False
        
        # Test 2: Your scanner's resolve_subdomain function
        print("🧪 Scanner resolve_subdomain test:")
        try:
            result = await resolve_subdomain(subdomain, cleaned_domain)
            if result:
                print(f"   ✅ Scanner: {result['domain']} -> {result['ips']}")
                print(f"   📋 Record types: {result.get('record_types', 'None')}")
                scanner_works = True
            else:
                print(f"   ❌ Scanner: {full_domain} -> None returned")
                scanner_works = False
        except Exception as e:
            print(f"   💥 Scanner: {full_domain} -> ERROR: {e}")
            scanner_works = False
        
        # Compare results
        if socket_works and not scanner_works:
            print("   🚨 MISMATCH: Socket works but scanner fails!")
        elif socket_works and scanner_works:
            print("   ✅ BOTH WORK: This subdomain should be detected")
        elif not socket_works and not scanner_works:
            print("   ℹ️  BOTH FAIL: Subdomain doesn't exist")
        else:
            print("   🤔 WEIRD: Scanner works but socket fails")

if __name__ == "__main__":
    asyncio.run(debug_scanner_vs_simple())