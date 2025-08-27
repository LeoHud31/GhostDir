import asyncio
from core.scanner import resolve_subdomain, clean_domain

async def test_your_known_subdomains():
    """Test your exact scanner function with your known subdomains"""
    
    # Enter your target domain and known subdomains here
    target_domain = input("Enter your target domain (e.g., testphp.vulnweb.com): ").strip()
    if not target_domain:
        target_domain = "vulnweb.com"
    
    known_subs = input("Enter your 2 known subdomains (comma-separated, e.g., www,mail): ").strip()
    if not known_subs:
        known_subs = "testphp,www"
    
    subdomains_to_test = [s.strip() for s in known_subs.split(',')]
    
    print(f"\n🎯 Testing {len(subdomains_to_test)} known subdomains for {target_domain}")
    print("=" * 60)
    
    # Clean the domain the same way your scanner does
    cleaned_domain = clean_domain(f"http://{target_domain}")
    print(f"Cleaned domain: {target_domain} -> {cleaned_domain}")
    
    found_count = 0
    
    for subdomain in subdomains_to_test:
        print(f"\n🔍 Testing: {subdomain}.{cleaned_domain}")
        
        try:
            result = await resolve_subdomain(subdomain, cleaned_domain)
            
            if result:
                print(f"✅ FOUND: {result['domain']}")
                print(f"   IPs: {', '.join(result['ips'])}")
                print(f"   Record Types: {result.get('record_types', 'Unknown')}")
                found_count += 1
            else:
                print(f"❌ NOT FOUND: {subdomain}.{cleaned_domain}")
                
        except Exception as e:
            print(f"💥 ERROR: {subdomain}.{cleaned_domain} - {e}")
    
    print(f"\n📊 RESULTS: Found {found_count} out of {len(subdomains_to_test)} known subdomains")
    
    if found_count == 0:
        print("\n🤔 No subdomains found. Let's try some diagnostics...")
        
        # Test with a known good subdomain
        print("\n🧪 Testing www.google.com (should work)...")
        try:
            result = await resolve_subdomain("www", "google.com")
            if result:
                print(f"✅ Google test worked: {result['domain']} -> {result['ips']}")
            else:
                print("❌ Google test failed - DNS resolution not working")
        except Exception as e:
            print(f"💥 Google test error: {e}")

if __name__ == "__main__":
    asyncio.run(test_your_known_subdomains())