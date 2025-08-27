from Utils.wordlist_loader import load_wordlist

def check_wordlist():
    wordlist_path = "subdomains.txt"  # Update if different
    known_subs = ["www", "testhtml5", "testphp"]  # Update with your known subdomains
    
    print(f"🔍 Checking wordlist: {wordlist_path}")
    print("=" * 40)
    
    try:
        wordlist = load_wordlist(wordlist_path)
        print(f"✅ Loaded {len(wordlist)} words")
        
        # Show first 10 words with their representation
        print(f"\n📋 First 10 words in wordlist:")
        for i, word in enumerate(wordlist[:10]):
            print(f"  {i+1}. '{word}' (length: {len(word)})")
        
        # Check if known subdomains are in the list
        print(f"\n🎯 Checking for known subdomains:")
        for sub in known_subs:
            if sub in wordlist:
                index = wordlist.index(sub)
                print(f"  ✅ '{sub}' found at position {index+1}")
            else:
                print(f"  ❌ '{sub}' NOT FOUND in wordlist")
                
                # Check for variations
                variations = [
                    sub.strip(),
                    sub.upper(),
                    sub.lower(),
                    f" {sub}",
                    f"{sub} ",
                    f" {sub} "
                ]
                
                print(f"     Checking variations:")
                for var in variations:
                    if var in wordlist:
                        print(f"       ✅ Found variation: '{var}' (with spaces/case)")
                
        # Show all words that contain your known subdomains
        print(f"\n🔍 Words containing your known subdomains:")
        for sub in known_subs:
            matches = [word for word in wordlist if sub in word.lower()]
            if matches:
                print(f"  Words containing '{sub}': {matches[:5]}...")  # Show first 5
            else:
                print(f"  No words containing '{sub}'")
                
    except Exception as e:
        print(f"❌ Error loading wordlist: {e}")

if __name__ == "__main__":
    check_wordlist()