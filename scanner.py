# Thomas Roberts
# Dr. S. Islam
# CS 4308 (02) - Concepts of Programming Language
# September 22, 2024
"""
File Description: This file is a python program that scans a decaf program and
prints the tokens for that program.

Run this program in a terminal and pass the decaf program as a command line parameter.
"""
import sys

class Scanner:
    """
    Scanner for the decaf programming language

    Functions
    ---------
    __init__(file)
    add_char()
    get_char()
    get_non_blank()
    lookup(find_char)
    peak()
    lex()
    """
    # global variables
    char_classes = ('LETTER', 'DIGIT', 'UNKNOWN', 'EOF')
    next_char = ''
    next_char_class = 0
    lexeme = []
    token_class = ""
    col_num = 0
    line_num = 0
    current_line = ""
    file = []

    # list for parser
    t_list = []

    # look-up tables
    operators = ('+','-','*','/','(', ')', '{', '}','[',']',';','=',',','!', )
    token_name = ('T_AND', 'T_ASSIGN' ,'T_BOOLTYPE', 'T_BREAK', 'T_CHARCONSTANT',
                  'T_COMMA', 'T_COMMENT', 'T_CONTINUE', 'T_DIV', 'T_DOT','T_ELSE', 
                  'T_EQ', 'T_EXTERN', 'T_BoolConstant (value= false)', 'T_FOR', 'T_FUNC', 'T_GEQ','T_GT', 
                  'T_ID', 'T_IF','T_INTCONSTANT', 'T_Int', 'T_LCB', 'T_LEFTSHIFT', 
                  'T_LEQ', 'T_LPAREN', 'T_LSB', 'T_LT', 'T_MINUS', 'T_MOD', 'T_MULT', 
                  'T_NEQ', 'T_NOT', 'T_NULL', 'T_OR', 'T_PACKAGE', 'T_PLUS', 'T_RCB',
                  'T_RETURN', 'T_RIGHTSHIFT', 'T_RPAREN', 'T_RSB', 'T_SEMICOLON', 
                  'T_STRINGCONSTANT', 'T_STRINGTYPE', 'T_BoolConstant (value= true)', 'T_VAR', 'T_VOID', 
                  'T_WHILE', 'T_WHITESPACE')
    token_value = ('&&', '=', 'bool', 'break', 'char_lit', ',', 'comment', 'continue', 
                   '/', '.', 'else', '==', 'extern', 'false', 'for', 'func', '>=', '>', 
                    'identifier', 'if', 'int_lit', 'int', '{', '<<', '<=', '(', '[', '<', 
                    '-', '%', '*', '!=', '!', 'null', '||', 'package', '+', '}', 'return',
                    '>>', ')', ']', ';', 'string_lit', 'string', 'true', 'var', 'void',
                    'while', 'whitespace')
    

    def __init__(self, file) -> None:
        """
        Initializer function for Scanner obj

        Parameters
        ----------
        file - The file (in decaf language) being scanned
        """
        self.file = file.readlines()
        self.current_line = self.file[0]
        self.t_list = []
    # end __init__()

    def add_char(self) -> None:
        """
        Helper function that appends next_char to lexeme list
        """
        self.lexeme = self.lexeme + self.next_char
    # end of add_char()

    def get_char(self) -> None:
        """
        Helper function that checks if the next char is a digit, alpha, unknown, or EOF.
        Increments line_num, col_num as needed.
        """ 
        current_char = ''
        if self.col_num >= len(self.current_line): # checks for end of string
            if self.line_num < len(self.file)-1: # checks for EOF
                self.line_num = self.line_num+1 # incremenets line_num
                self.col_num = 0
                self.current_line = self.file[self.line_num]
            else: # goes to next string in file
                self.next_char = ''
                self.next_char_class = 3 # EOF
                return
        # end if
        current_char = self.current_line[self.col_num] 
        self.next_char = current_char # updates next char
        self.col_num = self.col_num+1 # increments col_num
        if current_char.isalpha(): # LETTER
            self.next_char_class = 0
            return 
        elif current_char.isdigit(): # DIGIT
            self.next_char_class = 1
            return 
        else:
            self.next_char_class = 2 # UNKNOWN
            return 
    # end of get_char()

    def get_non_blank(self) -> None:
        """
        Helper method that calls get_char until a nonblank is found
        """
        while(self.next_char.isspace()):
            self.get_char()
    # end of get_non_blank()

    def lookup(self, find_char) -> int:
        """
        lookup function to find the token_id for a given character

        Paramaters
        ----------
        find_char - character that needs to be identified

        Returns
        -------
        int - index of token. Reference Scanner.token_name and Scanner.token_value
        """
        next_token = 'NOTFOUND'
        if self.token_value.__contains__(find_char):
            token_index = self.token_value.index(find_char)
            self.token_class = self.token_name[token_index]
            next_token = self.token_class
        # end if
        return next_token 
    # end of lookup()

    def peak(self, char1) -> bool:
        """
        Helper method that determines if a possible combination of 
        unknown characters could form a known token. 

        Parameters
        -----------
        char1 - first part of a string for lexical analysis
        """
        if self.col_num < len(self.current_line): # checking next char is within index
            test_char = char1 + self.current_line[self.col_num-1]
        else:
            test_char = ""
        result = self.lookup(test_char)
        return not result == 'NOTFOUND' # return true if a known token exists
    # end peak()

    def lex(self) -> None:
        """
        This function acts as a lexical analyzer. It will determine if the nextchar is a digit, letter, or unknow
        and process the lexeme to match it with known tokens.

        This function will then print the lexeme and token information 
        """
        self.lexeme = ""
        self.get_non_blank()

        if self.next_char_class == 0: # CASE 1 LETTER
            self.add_char()
            self.get_char()
            while self.next_char_class == 0 or self.next_char_class == 1:
                self.add_char()
                self.get_char()
            current_token = self.lookup(self.lexeme) # checks for known token such as 'void' = 'T_VOID'
            if current_token == 'NOTFOUND':
                self.token_class = 'T_IDENTIFIER'
        elif self.next_char_class == 1: # CASE 2 DIGIT
            self.add_char()
            self.get_char()
            while self.next_char_class == 1:
                self.add_char()
                self.get_char()
            self.token_class = 'T_INTCONSTANT (value= %s)' % self.lexeme
        elif self.next_char_class == 2: # CASE 3 UNKNOWN
            if self.next_char == '"' or self.next_char == '\'': # Checks for string constants
                conditional = True
                while conditional:
                    self.add_char()
                    self.get_char()
                    conditional = not (self.next_char == '"' or self.next_char == '\'')
                self.add_char()
                self.get_char()
                self.token_class = 'T_STRINGCONSTANT (value= %s)' % self.lexeme
            else: # not a string constant
                self.add_char()
                self.get_char()
                current_token = self.lookup(self.lexeme)
                while self.next_char_class == 2 and current_token == 'NOTFOUND':
                    self.add_char()
                    self.get_char()
                    current_token = self.lookup(self.lexeme)
                if self.peak(self.lexeme): # peaks for a known combinations. For example '<=' is a known token. so is '<' and '=' by themselves
                    self.add_char()
                    self.get_char()
                    current_token = self.lookup(self.lexeme)
        else: # CASE 4 EOF
            self.lexeme = "EOF0"
        self.t_list.append((self.lexeme, 
                            self.line_num+1,
                            (self.col_num-len(self.lexeme)), 
                            self.col_num-1,  
                            self.token_class))
    # end of lex()

    def print_list(self):
        """
        """
        for item in self.t_list:
             print("%s     line %s Cols  %s - %s  is  %s" % (item[0], 
                                                  item[1], 
                                                  item[2], 
                                                  item[3], 
                                                  item[4]))
    # end of print_list()
# end of class Scanner