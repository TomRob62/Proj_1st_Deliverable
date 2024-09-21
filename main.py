# Thomas Roberts
# Scanner
import sys

def main() -> None:
    # description
    file_name = ""
    try:
        file_name = sys.argv[1]
        my_file = open(file_name, 'r')
    except IndexError:
        print("file argument not given")
        sys.exit()
    except FileNotFoundError:
        print("file not found.")
        sys.exit()

def scanner() -> None:
    # description
    print("done")
    
if __name__ == 'main':
    main()