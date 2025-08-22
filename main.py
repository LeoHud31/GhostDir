from Utils.wordlist_loader import load_wordlist

def main():
    while True:
        file_path = input("Enter the path to the wordlist file: ")
        try:
            count = 0
            wordlist =  load_wordlist(file_path)
            for count, word in enumerate(wordlist, 1):
                print(f"{count}: Processing: {word}")
            break
        except FileNotFoundError as e:
            print(f"Error: {e}")
            continue

if __name__ == "__main__":
    main()
