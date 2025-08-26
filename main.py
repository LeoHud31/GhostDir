from Utils.wordlist_loader import load_wordlist
from core.fuzzing import fetch_url
import asyncio
from core.scanner import scan_url
from Utils.output import output
from typing import Optional, Dict, Any

def parse_status_filters(user_input: str) -> Optional[list[int]]:
    if not user_input:
        return None
    try:
        return [int(code.strip()) for code in user_input.split(',')]
    except ValueError:
        print("No valid status codes given, proceeding without filters.")
        return None

def print_summary(results: Dict[str, Any]) -> None:
    print("\nOperation completed. Summary of results:")
    print("=" * 50)
    print(f"Total URLs found: {len(results)}")


#fuzzing function this takes in target, file path and status filters to fuzzing a website URL
async def Fuzzing(Target: str, rate: float) -> Dict[str, int]:
    #asks user for further inputs if fuzzing is selected
    file_path = input("Enter the path to the wordlist file: ")
    wordlist =  load_wordlist(file_path)
    status_filters = input("Enter the status filters with commas (eg: 200,301)(leave blank for none)")

    status_filters = parse_status_filters(status_filters)

    print(f"\nStarting fuzzing on {Target} with {len(wordlist)} words...\n")
    print("=" * 50)

    results = await fetch_url(Target, wordlist, status_filters)

    print("\nFuzzing completed. Summary of results:")
    print("=" * 50)
    print(f"Total URLs found: {len(results)}")

    return results
    
# takes in target, rate and file path to scan a domain for any subdomains
async def Scanner(Target: str, rate: float) -> Dict[str, Any]:
    print(f"\nStarting scan on {Target}...\n")
    print("=" * 50)

    #checks to see if valid input
    if '/' in Target or ':' in Target or Target.startswith(('http://', 'https://', 'www.')):
        print("Please enter the domain name only (e.g., vulnweb.com)")
        return None
    
    file_path = input("Enter path to subdomain wordlist file: ")
    wordlist = load_wordlist(file_path)

    results = await scan_url(Target, requests_per_second=rate,
                             enable_subdomain_scan=True,
                             wordlist=wordlist)

    print("\nScan completed. Summary of results:")
    print("=" * 50)
    print(f"Total URLs found: {len(results)}")

    return results

#main fucntion to run the program
async def main():
    #inital user inputs
    try: 
        Target = input("For Fuzzing enter the target URL (e.g., http://example.com), for scanning Enter domain (example.com): ")
        rate = float(input("Enter requests per second (Default: 10): ") or 10)
        choice = input("Choose operation - Scan (s) or Fuzz (f): ").strip().lower()
    
        #decides the choice of operation
        if choice == 's':
            results = await Scanner(Target, rate)
        elif choice == 'f':
            results = await Fuzzing(Target, rate)
        else:
            print("Invalid choice. Please enter 's' for Scan or 'f' for Fuzz.")
            return

        #if results are found, ask user if they want to save them
        if results:
            if input("Do you want to save results to a file? (y/n): ").lower() == 'y':
                file_name = input("Enter filename with extension (e.g., results.txt): ")
                output.output_results(results, file_name)
            else:
                output.output_results(results)

    except Exception as e:
        print(f"An error occurred: {e}")

#main action driver
if __name__ == "__main__":
    asyncio.run(main())
