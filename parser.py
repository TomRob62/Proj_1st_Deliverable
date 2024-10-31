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
        self.my_scan.get_char()
        self.my_scan.lex()
        self.token = my_scan.token_class
        self.token_stack = []
        self.paren_stack = 0
    # end of __init__()

    def next_token(self) -> str:
        """
        Helper function the gets the next token.
        """
        self.token_stack.append(self.my_scan.save_state())
        self.my_scan.lex()
        self.token = self.my_scan.token_class
        if len(self.token_stack) > 5:
            self.token_stack.pop(0)
        return self.token
    # end next_token()

    def print_error(self, message) -> None:
        """
        Helper function that prints an error message.
        """
        print("\n*** Error line %s." % self.my_scan.line_num)
        line = self.my_scan.current_line
        line = line[:len(line)-1]
        print(line)
        print(" "*(self.my_scan.col_num-len(self.my_scan.lexeme)) + "^")
        print("*** %s" % message)
        exit()
    # end print_error()

    def backtrack(self, num_remove = 1):
        for i in range(num_remove):
            self.my_scan.load_state(self.token_stack.pop())
            self.token = self.my_scan.token_class
    # end backtrack()

    def main(self):
        while self.my_scan.next_char_class != 3:
            self.var_decls()
            self.method_decls()
            self.next_token()
        else:
            print("Success!")
    # end main()

    def method_decls(self):
        while self.method_decl():
            self.next_token()
    # end method_decls()

    def method_decl(self):
        if self.token == "T_VOID" or self.type():
            if self.next_token() == "T_IDENTIFIER":
                if self.next_token() == "T_LPAREN":
                    self.paren_stack += 1
                    self.next_token()
                    while self.type():
                        if self.next_token() == "T_IDENTIFIER":
                            if self.next_token() == "T_COMMA":
                                self.next_token()
                            elif self.token == "T_RPAREN":
                                None
                            else:
                                self.print_error("Syntax Error: expected comma")
                        else:
                            self.print_error("Syntax Error: expected identifier")
                    else:
                        if self.token == "T_RPAREN":
                            self.paren_stack -= 1
                            self.next_token()
                            return self.block()
            self.backtrack()
            return False
        else:
            return False
    # end method _decl()

    def block(self):
        if self.token == "T_LCB":
            self.next_token()
            self.var_decls()
            self.statements()
            if self.token == "T_RCB":
                return True
            self.print_error("Syntax Error: expected right bracket")
        else:
            return False
    # end block()

    def var_decls(self):
        while self.var_decl():
            self.next_token()
    # end var_decls()

    def var_decl(self):
        if self.type():
            if self.next_token() == "T_IDENTIFIER":
                if self.next_token() == "T_SEMICOLON":
                    return True
                self.backtrack(2)
                return False
            else:
                self.print_error("Syntax Error: expected identifier")
        else:
            return False
    # end var_decl()

    def statements(self):
        while self.statement():
            self.next_token()
    # end statements

    def assign(self):
        if self.token == "T_IDENTIFIER":
            if self.next_token() == "T_ASSIGN":
                self.next_token()
                return self.expr()
            self.backtrack()
            return False
        else:
            return False
    # end assign()

    def method_call(self):
        if self.token == "T_IDENTIFIER":
            if self.next_token() == "T_LPAREN":
                self.paren_stack += 1
                if self.next_token() == "T_RPAREN":
                    return True
                else:
                    while self.token != "T_RPAREN":
                        if self.constant():
                            self.next_token()
                        elif self.expr():
                            self.next_token()
                        if self.token == "T_COMMA":
                            self.next_token()
                        elif self.token == "T_RPAREN":
                            self.paren_stack -= 1
                        else:
                            break
                    else:
                        return True
            self.backtrack()
            return False
        else:
            return False
    # end method_call()
    
    def statement(self):
        if self.block():
            return True
        elif self.assign():
            if self.next_token() == "T_SEMICOLON":
                return True
            self.print_error("Syntax Error: expected semicolon")
        elif self.method_call():
            if self.next_token() == "T_SEMICOLON"  or self.paren_stack:
                return True
            self.print_error("Syntax Error: expected semicolon")
        elif self.token == "T_IF":
            if self.next_token() == "T_LPAREN":
                self.next_token()
                if self.expr():
                    if self.next_token() == "T_RPAREN":
                        self.next_token()
                        if self.block():
                            return True
                        else:
                            self.print_error("Syntax Error: expected left bracket")
                    self.print_error("Syntax Error: expected right parenthesis")
                else:
                    self.print_error("Syntax Error: expected expression")
            else:
                self.print_error("Syntax Error: expected left parenthesis")
        elif self.token == "T_FOR":
            if self.next_token() == "T_LPAREN":
                self.next_token()
                if self.assign():
                    if self.next_token() == "T_SEMICOLON":
                        self.next_token()
                        if self.expr():
                            self.next_token()
                            if self.token == "T_SEMICOLON":
                                self.next_token()
                                if self.assign():
                                    if self.next_token() == "T_RPAREN":
                                        self.next_token()
                                        return self.block()
                                    else: 
                                        self.print_error("Syntax Error: expected right parenthesis")
                                else:
                                    self.print_error("Syntax Error: expected assignment statement")
                            else: 
                                self.print_error("Syntax Error: expected semicolon")
                        else:
                            self.print_error("Syntax Error: expected expression")
                    else:
                        self.print_error("Syntax Error: expected semicolon")
                else:
                    self.print_error("Syntax Error: expected assignment statement")
            else:
                self.print_error("Syntax Error: expected left parenthesis")
        elif self.token == "T_WHILE":
            if self.next_token() == "T_LPAREN":
                self.next_token()
                self.expr()
                if self.next_token() == "T_RPAREN":
                    self.block()
                    return True
            self.print_error("Syntax Error: statement()")
        elif self.token == "T_RETURN":
            if self.next_token() == "T_SEMICOLON":
                return True
            if self.token == "T_LPAREN":
                condition = True
                self.next_token()
            else:
                condition = False
            if self.expr():
                if condition:
                    if self.next_token() == "T_RPAREN":
                        self.print_error("Syntax Error: expectedd right parenthesis")
                if self.next_token() == "T_SEMICOLON":
                    return True
        elif self.token == "T_BREAK":
            if self.next_token() == "T_SEMICOLON":
                return True
            else:
                self.print_error("Syntax Error: statement()")
        elif self.token == "T_CONTINUE":
            if self.next_token() == "T_SEMICOLON":
                return True
            else:
                self.print_error("Syntax Error: statement()")
        else:
            return False

    def unary_op(self):
        return self.token == "T_NOT" or self.token == "T_MINUS"
    # end unary_op()

    def bin_op(self):
        return self.arith_op() or self.bool_op()  
    # end bin_op  

    def arith_op(self):
        """( "+" | "-" | "*" | "/" | "<<" | ">>" | "%" )"""
        return (self.token == "T_PLUS"
                or self.token == "T_MINUS"
                or self.token == "T_MULT"
                or self.token == "T_DIV"
                or self.token == "T_LEFTSHIFT"
                or self.token == "T_RIGHTSHIFT"
                or self.token == "T_MOD")
    # end arith_op()

    def bool_op(self):
        """BooleanOperator = ( "==" | "!=" | "<" | "<=" | ">" | ">=" | "&&" | "||" ) """
        return (self.token == "T_EQ"
                or self.token == "T_NEQ"
                or self.token == "T_LT"
                or self.token == "T_LEQ"
                or self.token == "T_RT"
                or self.token == "T_REQ"
                or self.token == "T_AND"
                or self.token == "T_OR")
    # end bool_op()

    def expr(self):
        if self.constant(): # constant
            return True
        elif self.unary_op(): # unary operator
            self.next_token()
            if self.expr():
                return True
            else:
                self.print_error("Syntax Error: expr()")
        elif self.token == "T_IDENTIFIER": 
            if self.method_call(): # method_call
                return True
            self.next_token()
            if self.bin_op(): # binary operator
                self.next_token()
                if self.expr():
                    return True
                else:
                    self.print_error("Syntax Error: expr()")
            else:
                self.backtrack()
            return True
        else:
            return False
    # end expr()
    def type(self):
        return (self.token == "T_INTTYPE"
                or self.token == "T_STRINGTYPE"
                or self.token == "T_CHARTYPE"
                or self.token == "T_BOOLTYPE"
                or self.token == "T_FLOATTYPE")
    # end type()

    def method_type(self):
        return (self.token == "T_VOID"
                or self.type())
    # end method_type()

    def bool_constant(self):
        return (self.token == "T_BoolConstant (value= true)"
                or self.token == "T_BoolConstant (value= false)")
    # end bool_constant()

    def array_type(self):
        if self.token == "T_LSB":
            if self.next_token() == "T_INTCONSTANT":
                if self.next_token() == "T_RSB":
                    self.next_token()
                    return self.type()
            self.print_error("Syntax Error: array_type()")
        else:
            return False
    # end array_type()

    def constant(self):
        return (self.token == "T_INTCONSTANT"
            or self.token == "T_STRINGCONSTANT"
            or self.token == "T_CHARCONSTANT"
            or self.bool_constant())
    # end constant