# Contents
Setup
File path
File functions
Syntax of inputs
Example commands

# Setup
Use terminal to cd into file location eg: cd documents/GhostDir
Run python main.py
enter command (see example commands for direction of use)


# File Paths

GhostDir
|
|-- core/
|   |- fuzzing.py <--logic for fuzzing using a wordlist
|   |- scanner.py <-- core scanner logic (GET/POST support, filters)
|
|-- utils/
|   |- output.py <-- JSON, TXT, CSV export
|   |- wordlist_loader.py <-- wordlist loading logic 
|   |- rate_limiter.py <-- smart throttling logic
|
|-- wordlists/ <--pulls from a TXT wordlist, file selected by user
|   |-common.txt
|
|
|-- main.py <-- CLI entrypoint main driver
|
|-- readme.md

# File functions

main.py
runs the program:
parse_satus_filters - checks and cleans valid status filters
Fuzzing - runs the fuzzing function
Scanner - runs the scanner function
Main - runs the rest of the file, runs the parse_status_filters and waits for user entering 'scan' or 'fuzz'
name = main - runs the parser for the user input

# Utils/

output.py
output_results - drives the other functions
write_txt - writes to a text file 
write_csv - writes to a csv file
write_json - writes to a json file

wordlist_loader.py
load_wordlist - opens the file thats selected

rate_limiter.py
init - delays 1/requests_per_second
wait - times how long since last request for throttling

init.py - used for caching

# Core/
init.py - used for caching

fuzzing.py
fetch_url - adds the words to the end of the url and tests it

scanner.py
clean_domain - santises the domain thats been entered
scan_url - adds the subdomain to the front and runs them

# Syntax of inputs 
--target - selects the targert
--mode - scan or fuzz
--wordlist - selects what input file would be used
--rate - requests per second
--status-filters - http status codes that are filtered out only used for fuzzing
--output - selects what the output file will be (only accepts .txt, .csv, .json)

# Example commands

Subdomain scanning
# Basic subdomain scan
python main.py --target example.com --mode scan --wordlist wordlists/subdomains.txt

# Fast scan with higher rate limit
python main.py --target example.com --mode scan --wordlist wordlists/subdomains.txt --rate 50

# Save results to file
python main.py --target example.com --mode scan --wordlist wordlists/subdomains.txt --output results.json

URL Fuzzing
# Basic directory fuzzing
python main.py --target https://example.com --mode fuzz --wordlist wordlists/directories.txt

# Filter specific status codes
python main.py --target https://example.com --mode fuzz --wordlist wordlists/directories.txt --status-filters 200,301,403

# High-speed fuzzing
python main.py --target https://example.com --mode fuzz --wordlist wordlists/directories.txt --rate 100