from scanner import Scanner
from parser import My_Parser
import sys

def main() -> None:
    """
    Program driver function
    """
    # try to open file
    try:
        file_name = sys.argv[1] # check for file name
        my_file = open(file_name, 'r') # open file
        scan_obj = Scanner(my_file) # pass IO stream to scanner
    except IndexError:
        print("file argument not given")
        sys.exit()
    except FileNotFoundError:
        print("file not found.")
        sys.exit()
    # end of try/except

    parse = My_Parser(scan_obj)
    parse.main()
# end of main()

if __name__ == '__main__':
    main()
