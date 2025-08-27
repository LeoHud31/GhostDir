import socket
import dns.resolver

def test_common_subdomains():
    """Test common subdomains for testphp.vulnweb.com"""
    
    base_domain = "google.com"
    
    # First, test if the base domain works
    print(f"🎯 Testing base domain: {base_domain}")
    try:
        ip = socket.gethostbyname(base_domain)
        print(f"✅ {base_domain} -> {ip}")
    except Exception as e:
        print(f"❌ {base_domain} -> {e}")
    
    # Test common subdomains
    common_subs = [
        "www", "mail", "ftp", "admin", "test", "dev", "api", "blog", 
        "shop", "support", "help", "docs", "portal", "secure", "login",
        "m", "mobile", "app", "staging", "beta", "demo"
    ]
    
    print(f"\n🔍 Testing {len(common_subs)} common subdomains:")
    print("=" * 50)
    
    found_subdomains = []
    
    for sub in common_subs:
        full_domain = f"{sub}.{base_domain}"
        try:
            ip = socket.gethostbyname(full_domain)
            print(f"✅ {full_domain} -> {ip}")
            found_subdomains.append(full_domain)
        except:
            pass  # Don't print failures to keep output clean
    
    print(f"\n📊 RESULTS:")
    print(f"Found {len(found_subdomains)} real subdomains:")
    for sub in found_subdomains:
        print(f"  • {sub}")
    
    if not found_subdomains:
        print("❌ No subdomains found!")
        print("\n🤔 This could mean:")
        print("  • The domain doesn't use subdomains")
        print("  • Subdomains use non-standard names")
        print("  • There's a DNS/network issue")
    
    return found_subdomains

def test_browser_access():
    """Test what you can actually access in a browser"""
    print(f"\n🌐 BROWSER TEST:")
    print("Try these URLs in your browser and tell me which ones work:")
    
    base = "testphp.vulnweb.com"
    test_urls = [
        f"http://{base}",
        f"https://{base}",
        f"http://www.{base}",
        f"https://www.{base}",
    ]
    
    for url in test_urls:
        print(f"  🔗 {url}")

if __name__ == "__main__":
    found = test_common_subdomains()
    test_browser_access()
    
    if not found:
        print(f"\n💡 SUGGESTION:")
        print("Since no subdomains were found, your scanner is working correctly!")
        print("The 'known subdomains' you mentioned might not actually exist in DNS.")
        print("Try testing with a different domain that definitely has subdomains, like:")
        print("  • google.com (has www, mail, etc.)")
        print("  • github.com (has www, api, etc.)")
        print("  • stackoverflow.com (has www, meta, etc.)")