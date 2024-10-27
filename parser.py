# Thomas Roberts
# Dr. S. Islam
# CS 4308 (02) - Concepts of Programming Language
# October 26, 2024
"""
File Description: First part of a recursive descent parser. Focuses on syntax.
"""

from scanner import Scanner

class My_Parser:
    def __init__(self, my_scan):
        """
        Initializer function
        """
        self.my_scan = my_scan
    # end of __init__()


    def scan_only(self):
        """
        
        """
        # body of main function
        self.my_scan.get_char()
        conditional = True
        while(conditional):
            self.my_scan.lex()
            conditional = (self.my_scan.next_char_class != 3) 

        self.my_scan.print_list()
    # end of scan_only()