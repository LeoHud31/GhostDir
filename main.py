from Utils.wordlist_loader import load_wordlist
from core.fuzzing import fetch_url
import asyncio
from core.scanner import scan_url
from Utils.output import output

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

    return results
    

async def Scanner(Target, rate):
    print(f"\nStarting scan on {Target}...\n")
    print("=" * 50)

    if '/' in Target or ':' in Target or Target.startswith(('http://', 'https://', 'www.')):
        print("Please enter the domain name only (e.g., vulnweb.com)")
        return None
    
    do_subdomain = input("Do you want to perform a subdomain scan? (y/n): ").strip().lower() == 'y'
    wordlist = None

    if do_subdomain:
        file_path = input("Enter path to subdomain wordlist file: ")
        wordlist = load_wordlist(file_path)

    results = await scan_url(Target, requests_per_second=rate,
                             enable_subdomain_scan=do_subdomain,
                             wordlist=wordlist)

    print("\nScan completed. Summary of results:")
    print("=" * 50)
    print(f"Total URLs found: {len(results)}")

    return results

async def main():
    try: 
        Target = input("For Fuzzing enter the target URL (e.g., http://example.com), for scanning Enter domain (example.com): ")
        rate = float(input("Enter requests per second (Default: 10): ") or 10)
        choice = input("Choose operation - Scan (s) or Fuzz (f): ").strip().lower()
    

        if choice == 's':
            results = await Scanner(Target, rate)
        elif choice == 'f':
            results = await Fuzzing(Target, rate)
        else:
            print("Invalid choice. Please enter 's' for Scan or 'f' for Fuzz.")
            return
    
        if results:
            if input("Do you want to save results to a file? (y/n): ").lower() == 'y':
                file_name = input("Enter filename with extension (e.g., results.txt): ")
                output.output_results(results, file_name)
            else:
                output.output_results(results)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())
