from Utils.wordlist_loader import load_wordlist
from core.fuzzing import fetch_url
import asyncio


async def main():
    Target = input("Enter the target URL (e.g., http://example.com): ")
    file_path = input("Enter the path to the wordlist file: ")
    try:
        count = 0
        wordlist =  load_wordlist(file_path)
        status_filters = [200, 301, 302, 403, 500] 

        print(f"\nStarting fuzzing on {Target} with {len(wordlist)} words...\n")
        print("=" * 50)

        results = await fetch_url(Target, wordlist, status_filters)

        print("\nFuzzing completed. Summary of results:")
        print("=" * 50)
        print(f"Total URLs found: {len(results)}")

    except FileNotFoundError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
