from Utils.wordlist_loader import load_wordlist
from core.fuzzing import fetch_url
import asyncio
from core.scanner import scan_url

async def Fuzzing(Target, rate=10):
    count = 0
    file_path = input("Enter the path to the wordlist file: ")
    wordlist =  load_wordlist(file_path)
    status_filters = input("Enter the status filters (leave blank for none)")

    if not status_filters:
        status_filters = None
    else:
        try:
            status_filters = [int(code) for code in status_filters.split(',')]
        except ValueError:
            print("No valid status codes given, proceeding without filters.")
            status_filters = None


    print(f"\nStarting fuzzing on {Target} with {len(wordlist)} words...\n")
    print("=" * 50)

    results = await fetch_url(Target, wordlist, status_filters)

    print("\nFuzzing completed. Summary of results:")
    print("=" * 50)
    print(f"Total URLs found: {len(results)}")


async def Scanner(Target, rate):
    print(f"\nStarting scan on {Target}...\n")
    print("=" * 50)

    results = await scan_url(Target, requests_per_second=rate)

    print("\nScan completed. Summary of results:")
    print("=" * 50)
    print(f"Total URLs found: {len(results)}")

async def main():
    Target = input("Enter the target URL (e.g., http://example.com): ")
    rate = float(input("Enter requests per second (Default: 10): ") or 10)
    choice = input("Choose operation - Scan (s) or Fuzz (f): ").strip().lower()

    if choice == 's':
        await Scanner(Target, rate)
    elif choice == 'f':
        await Fuzzing(Target, rate)
    else:
        print("Invalid choice. Please enter 's' for Scan or 'f' for Fuzz.")
        return
    

if __name__ == "__main__":
    asyncio.run(main())
