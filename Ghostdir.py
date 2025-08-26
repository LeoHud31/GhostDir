from Utils.wordlist_loader import load_wordlist
from core.fuzzing import fetch_url
import asyncio
from core.scanner import scan_url
from Utils.output import output
from typing import Optional, Dict, Any
import argparse

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


async def Fuzzing(Target: str, wordlist: str, rate: float) -> Dict[str, int]:
    wordlist_data =  load_wordlist(wordlist)
    status_filters = parse_status_filters(status_filters)

    print(f"\nStarting fuzzing on {Target} with {len(wordlist_data)} words...\n")
    print("=" * 50)

    results = await fetch_url(Target, wordlist, status_filters, requests_per_second=rate)

    print("\nFuzzing completed. Summary of results:")
    print("=" * 50)
    print(f"Total URLs found: {len(results)}")

    return results
    

async def Scanner(Target: str, rate: float, wordlist: str) -> Dict[str, Any]:
    print(f"\nStarting scan on {Target}...\n")
    print("=" * 50)

    if '/' in Target or ':' in Target or Target.startswith(('http://', 'https://', 'www.')):
        print("Please enter the domain name only (e.g., example.com)")
        return None
    
    wordlist_data = load_wordlist(wordlist)

    results = await scan_url(Target, requests_per_second=rate,
                             enable_subdomain_scan=True,
                             wordlist=wordlist_data)

    print("\nScan completed. Summary of results:")
    print("=" * 50)
    print(f"Total URLs found: {len(results)}")

    return results


async def main(args: argparse.Namespace) -> None:

    try: 
        if args.mode == 'scan':
            results = await Scanner(args.Target, args.rate, args.wordlist)
        elif args.mode == 'fuzz':
            results = await Fuzzing(args.Target, args.rate, args.wordlist, args.status_filters)
        else:
            print("Invalid choice. Please enter scan or fuzz.")
            return

        if results:
            if args.output:
                output.output_results(results, args.output)
            else:
                output.output_results(results)

    except Exception as e:
        print(f"An error occurred: {e}")

#main action driver
if __name__ == "GhostDir":
    parser = argparse.ArgumentParser(description="GhostDir: A tool for subdomain scanning and URL fuzzing.")

    parser.add_argument("--target", required=True, help="target URL for fuzzing (e.g., http://example.com) or domain for scanning (e.g., example.com)")
    parser.add_argument("--mode", required=True, choices=['scan', 'fuzz'], help="Operation mode: 'scan' for subdomain scanning, 'fuzz' for URL fuzzing")
    parser.add_argument("--wordlist", required=True, help="Path to the wordlist file")
    parser.add_argument("--rate", type=float, default=10, help="Requests per second (default: 10)")
    parser.add_argument("--status-filters", type=str, default="", help="Comma-separated HTTP status codes to filter (fuzzing only) (e.g., 200,301,404)")
    parser.add_argument("--output", type=str, help="Output file name (supports .txt, .csv, .json)")

    args = parser.parse_args()

    asyncio.run(main())
