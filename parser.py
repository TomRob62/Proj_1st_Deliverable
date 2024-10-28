# Thomas Roberts
# Dr. S. Islam
# CS 4308 (02) - Concepts of Programming Language
# October 26, 2024
"""
File Description: First part of a recursive descent parser. Focuses on syntax errors.
"""

from scanner import Scanner

class My_Parser:
    def __init__(self, my_scan):
        """
        Initializer function
        """
        self.my_scan = my_scan
        self.my_scan.get_char()
        self.my_scan.lex()
        self.token = my_scan.token_class
        self.last_token = ""
    # end of __init__()

    def main(self):
        """
        Main driver function that filters through the file until
        end of file is reached
        """
        while(self.my_scan.next_char_class != 3):
            self.program()
            self.next_token()
    # end main()

    def next_token(self) -> str:
        """
        Helper function the gets the next token.
        """
        self.last_token = self.token
        self.my_scan.lex()
        self.token = self.my_scan.token_class
        return self.token
    # end next_token()

    def print_error(self, message) -> None:
        """
        Helper function that prints an error message.
        """
        print("*** Error line %s." % self.my_scan.line_num)
        line = self.my_scan.current_line
        line = line[:len(line)-1]
        print(line)
        print(" "*self.my_scan.col_num + "^")
        print("*** %s" % message)
        SystemExit()
    # end print_error()
    # from this point on, the functions are based on the decaf grammars

    def program(self):
        if self.method_decl():
            return True
        else:
            return self.var_decl()
    # end program

    def method_decl(self):
        if self.method_type():
            self.next_token()
            if self.token == "T_IDENTIFIER":
                self.next_token()
                if self.token == "T_LPAREN":
                    self.next_token()
                    if self.token == "T_RPAREN":
                        self.next_token()
                        return self.block()
                    else:
                        self.print_error("Error: expected right parenthesis")
                else:
                    self.print_error("Error: expected left parenthesis")
            else:
                self.print_error("Error: expected identifier")
        else:
            return False
    # end method_decl()

    def block(self):
        if self.token == "T_LCB":
            self.next_token()
            if self.var_decls():
                self.next_token()
            if self.statements():
                self.next_token()
            if self.token == "T_RCB":
                return True
            else:
                self.print_error("Error: expected right bracket")
        else:
            return False
    # end block()

    def var_decls(self):
        if self.var_decl():
            self.next_token()
            while(self.var_decl()):
                self.next_token()
            else:
                return False
        else:
            return False
    # end var_decls()

    def var_decl(self):
        if self.extern_type():
            self.next_token()
            if self.token == "T_IDENTIFIER":
                self.next_token()
                if self.token == "T_SEMICOLON":
                    return True
                else:
                    self.print_error("Error: expected semicolon")
            else:
                self.print_error("Error: expected identifier")
        else:
            return False
    # end var_decl()

    def statements(self):
        if self.statement():
            self.next_token()
            while(self.statement()):
                self.next_token()
            return True
        else:
            return False
    # end statements()
    
    def assign(self):
        if self.l_value():
            if self.token == "T_ASSIGN":
                self.next_token()
                return self.expr(0)
            else:
                return False
        else:
            return False
    # end assign()

    def l_value(self):
        if self.token == "T_IDENTIFIER":
            self.next_token()
            if self.token == "T_LCB":
                self.next_token()
                if self.expr(0):
                    self.next_token()
                    if self.token == "T_RCB":
                        return True
                    else:
                        self.print_error("Error: expected right bracket")
            return True
        else:
            return False
    # end l_value()

    def method_call(self):
        if self.token == "T_IDENTIFIER":
            self.next_token()
            if self.token == "T_LPAREN":
                self.next_token()
                while self.method_arg():
                    self.next_token()
                    if self.token == "T_COMMA":
                        self.next_token()
                if self.token == "T_RPAREN":
                    return True
                else:
                    self.print_error("Error: expected right parenthesis")
            else:
                self.print_error("Error: expected left parenthesis")
        else:
            return False
    # end method_call()

    def method_arg(self):
        if self.expr(0):
            return True
        else:
            return self.token == "STRING_CONSTANT"
    # end method_arg()
    
    def statement(self):
        if self.block():
            return True
        elif self.assign():
            self.next_token()
            if self.token == "T_SEMICOLON":
                return True
            else:
                self.print_error("Error: expected semicolon")
        elif self.method_call():
            self.next_token()
            if self.token == "T_SEMICOLON":
                return True
            else:
                self.print_error("Error: expected semi colon")
        elif self.token == "T_IF": # Statement = if "(" Expr ")" Block [ else Block ] .
            self.next_token()
            if self.token == "T_LPAREN":
                self.next_token()
                self.expr(0)
                self.next_token()
                if self.token == "T_RPARAN":
                    self.next_token()
                    self.block()
                    self.next_token()
                    if self.token == "T_ELSE":
                        self.next_token()
                        self.block()
                    else:
                        return True
                else:
                    self.print_error("Error: expected right parenthesis")
            else:
                self.print_error("Error: expected left parenthesis")
        elif self.token == "T_WHILE": # Statement =  while "(" Expr ")" Block .
            self.next_token()
            if self.token == "T_LPAREN":
                self.next_token()
                self.expr(0)
                self.next_token()
                if self.token == "T_RPAREN":
                    self.next_token()
                    self.block()
                else:
                    self.print_error("Error: expected right parenthesis")
            else:
                self.print_error("Error: expected left parenthesis")
        else:
            return False
    # end def statement()

    def unary_operator(self) -> bool:
        return self.token == "T_NOT" or self.token == "T_MINUS"
    # end unary_operator()

    def binary_operator(self) -> bool:
        if self.arithmetic_operator():
            return True
        else:
            return self.boolean_operator()
    # end binary_operator()

    def arithmetic_operator(self):
        arithmetic_op = ["T_PLUS", "T_MINUS", "T_MULT", "T_DIV", 
                         "T_LEFTSHIFT", "T_RIGHTSHIFT", "T_MOD"]
        return arithmetic_op.__contains__(self.token)
    # end arithmetic_operator()

    def boolean_operator(self):
        boolean_op = ["T_EQ", "T_NEQ", "T_LT", "T_LEQ", "T_GT", "T_GEQ",
                      "T_AND", "T_OR"]
        return boolean_op.__contains__(self.token)
    # end boolean_operator()

    def expr(self, call_num):
        if call_num > 2:
            return False
        if self.method_call(): # Expr = MethodCall .
            return True
        elif self.token == "T_IDENTIFIER": # Expr = identifier "[" Expr "]" 
            self.next_token()
            if self.token == "T_LSB":
                self.expr(call_num+1)
                self.next_token()
                if self.token == "T_RSB":
                    return True
                else:
                    self.print_error("syntax error: expected right bracket")
            else: # Expr = identifier .
                return True
        elif self.constant(): # Expr = Constant .
            return True
        elif self.token == "T_LPAREN": # Expr = "(" Expr ")" .
            self.next_token()
            self.expr(call_num+1)
            self.next_token()
            if self.token == "T_RPAREN":
                return True
            else:
                self.print_error("sytnax error: expected right parenthesis")
        elif self.unary_operator(): # Expr = UnaryOperator Expr .
            self.next_token()
            self.expr()
        elif self.expr(call_num+1): # Expr = Expr BinaryOperator Expr .
            self.next_token()
            if self.binary_operator():
                self.next_token()
                if self.expr(call_num+1):
                    return True
                else:
                    self.print_error("syntax error: expected expr")
            else:
                self.print_error("syntax error: expected binary operator")
        else:
            return False
    # end expr()

    def extern_type(self) -> bool:
        if self.token == "T_STRINGTYPE":
            return True
        else:
            return self.type()
    # end entern_type()
    
    def type(self) -> bool:
        return self.token == "T_BOOLTYPE" or self.token == "T_INTTYPE"
    # end type()

    def method_type(self) -> bool:
        if self.token == "T_VOID":
            return True
        else:
            return self.type()
    # end of method_type()

    def bool_constant(self) -> bool:
        return self.token == "T_BoolConstant (value= false)" or self.token == "T_BoolConstant (value= true)"
        # end bool_constant()

    def constant(self) -> bool:
        if ( self.token == "T_INTCONSTANT"
            or self.token == "T_CHARCONSTANT"
            or self.token == "T_STRINGCONSTANT"):
            return True
        else:
            return self.bool_constant()
    # end Constant()

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