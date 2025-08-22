def load_wordlist(file_path): 
    try: 
        with open(file_path, 'r') as file: 
            wordlist = [line.strip() for line in file if line.strip()] 
            if not wordlist: 
                raise ValueError("Wordlist is empty") 
            return wordlist 
    except FileNotFoundError: 
        print(f"File not found: {file_path}") 
        return []
    except Exception as e: 
        print(f"An error occurred while loading the wordlist: {e}") 
        return []