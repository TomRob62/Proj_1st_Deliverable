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
        self.indent_num = 0
        self.print_stack = []
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

    def print_error(self, message: str) -> None:
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

    def print_to_stack(self, statement):
        if self.indent_num < 1:
            self.indent_num = 1
        line = str(self.my_scan.line_num) + "     "*self.indent_num
        line = line + statement
        self.print_stack.append(line)
        return None
    # end print_to_stack()

    def backtrack(self, num_remove:int  = 1) -> None:
        "Helper function that backtracks a specific number of tokens"
        for i in range(num_remove):
            if len(self.print_stack):
                self.print_stack.pop()
            
            self.my_scan.load_state(self.token_stack.pop())
            self.token = self.my_scan.token_class
    # end backtrack()

    def main(self) -> None:
        """
        Main driver function. Will request tokens until end of file
        is reached.
        """
        self.print_to_stack("Program: ")
        self.indent_num += 1
        while self.my_scan.next_char_class != 3: # 3 is end-of-file
            self.var_decls()
            self.method_decls()
            self.next_token()
        else:
            for statement in self.print_stack:
                print(statement)
    # end main()

    """
    From this point on, the functions are representative of the grammar. 
    Each function (procedure) are mutually recursive.
    """
    def method_decls(self):
        """
        Rule: MethodDecls = { MethodDecl } .

        allows zero or more method declarations.
        """
        while self.method_decl():
            self.next_token()
    # end method_decls()

    def method_decl(self):
        """
        Rule: MethodDecl  = MethodType identifier "(" [ { identifier Type }+, ] ")" Block
        """
        self.print_to_stack("FnDcl: ")
        self.indent_num += 1
        if self.token == "T_VOID" or self.type(): #  Type
            self.print_to_stack("Type: %s" % self.my_scan.lexeme)
            if self.next_token() == "T_IDENTIFIER": # identifier
                self.print_to_stack("Identifier: %s" % self.my_scan.lexeme)
                if self.next_token() == "T_LPAREN": # "("
                    self.paren_stack += 1
                    self.next_token()
                    # zero or more method arguments
                    while self.type(): # Type
                        self.print_to_stack("(formals) VarDecl:")
                        self.print_to_stack("\tType: %s" % self.my_scan.lexeme)
                        if self.next_token() == "T_IDENTIFIER": # identifier
                            self.print_to_stack("\tIdentifier: %s" % self.my_scan.lexeme)
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
                            if self.block():
                                self.indent_num -= 1
                                return True
                            else:
                                return False
            self.print_stack.pop()
            self.indent_num -= 1
            self.backtrack() # back tracking
            return False
        else:
            self.print_stack.pop()
            self.indent_num -= 1
            return False
    # end method _decl()

    def block(self):
        """
        Rule: Block = "{" VarDecls Statements "}" .
        """
        self.print_to_stack("(Body) StmtBlock: ")
        self.indent_num += 1
        if self.token == "T_LCB":
            self.next_token()
            self.var_decls() # VarDecls
            self.statements() # Statements
            if self.token == "T_RCB":
                self.indent_num -= 1
                return True
            self.print_error("Syntax Error: expected right bracket")
        else:
            self.print_stack.pop()
            self.indent_num -= 1
            return False
    # end block()

    def control_block(self):
        self.print_to_stack("StmtBlock:")
        self.indent_num += 1
        control_condition = False
        if self.token == "T_LCB":
            self.next_token()
            control_condition = True
            self.var_decls
            self.statements
        else: 
            self.var_decl()
            self.statement()
        self.indent_num -= 1
        if control_condition:
            if self.next_token() == "T_RCB":
                return True
            else:
                self.print_error("Syntax Error: expected right bracket")
        return True
    # end control_block

    def var_decls(self):
        """
        Rule: VarDecls = { VarDecl } .

        zero or more variable declarations
        """
        while self.var_decl():
            self.next_token()
    # end var_decls()

    def var_decl(self):
        """
        Rule: VarDecl  = Type identifier  ";" .

        Only allows 1 variable declaration at a time.
        """
        self.print_to_stack("VarDecl:")
        self.indent_num += 1
        if self.type(): # Type 
            self.print_to_stack("Type: %s" % self.my_scan.lexeme)
            if self.next_token() == "T_IDENTIFIER": # identifier
                self.print_to_stack("Identifier: %s" % self.my_scan.lexeme)
                if self.next_token() == "T_SEMICOLON": # ";"
                    self.indent_num -= 1
                    return True
                self.backtrack(2) # back tracking
                self.print_stack.pop()
                self.indent_num -= 1
                return False
            else:
                self.print_error("Syntax Error: expected identifier")
        else:
            self.indent_num -= 1
            self.print_stack.pop()
            return False
    # end var_decl()

    def statements(self):
        """
        Rule: Statements = { Statement } .

        zero or more statements
        """
        while self.statement():
            self.next_token()
    # end statements

    def assign(self):
        """
        Rule: Assign    = identifier "=" Expr .
        """
        self.print_to_stack("AssignExpr: ")
        self.indent_num += 1
        if self.token == "T_IDENTIFIER": # identifier
            self.print_to_stack("Identifier: %s" % self.my_scan.lexeme)
            if self.next_token() == "T_ASSIGN": # "="
                self.print_to_stack("Operator: =")
                self.next_token()
                if self.expr():
                    self.indent_num -= 1
                    return True # Expr
            self.backtrack()
            self.indent_num -= 1
            self.print_stack.pop()
            return False
        else:
            self.indent_num -= 1
            self.print_stack.pop()
            return False
    # end assign()

    def method_call(self):
        """
        Rule: MethodCall = identifier "(" [ { MethodArg }+, ] ")" .
        """
        self.print_to_stack("Call:")
        self.indent_num += 1
        if self.token == "T_IDENTIFIER": # identifer
            self.print_to_stack("Identifier: %s" % self.my_scan.lexeme)
            if self.next_token() == "T_LPAREN": # "("
                self.paren_stack += 1
                if self.next_token() == "T_RPAREN":
                    self.indent_num -= 1
                    return True
                else:
                    # zero or more Method Arg
                    # MethodArg  = Expr | Constant.
                    self.print_to_stack("Args: ")
                    self.indent_num += 1
                    paren_const = self.paren_stack
                    while self.token != "T_RPAREN":
                        if self.constant(): # Constant
                            self.next_token()
                        elif self.expr(): # Expr
                            self.next_token()
                        if self.token == "T_COMMA": # ","
                            self.next_token()
                        elif self.token == "T_RPAREN": # ")"
                            if self.paren_stack != paren_const:
                                self.next_token()
                            self.paren_stack -= 1
                        else:
                            break
                    else:
                        self.indent_num -= 2
                        return True
            self.indent_num -= 2
            self.print_stack.pop()
            self.backtrack()
            return False
        else:
            self.indent_num -= 1
            self.print_stack.pop()
            return False
    # end method_call()
    
    def statement(self):
        """
        Rule: Statement = Block 
                        | Assign ";" 
                        | MethodCall ";" 
                        | if "(" Expr ")" Block [ else Block ] 
                        | while "(" Expr ")" Block 
                        | for "(" { Assign }+, ";" Expr ";" { Assign }+, ")" Block 
                        | return [ "(" [ Expr ] ")" ] ";" 
                        | break ";" 
                        | continue ";" 
        """
        # Block
        if self.block(): 
           return True

        # Assign ";"
        elif self.assign(): 
            if self.next_token() == "T_SEMICOLON":
                return True
            self.print_error("Syntax Error: expected semicolon")

        # MethodCall ";"
        elif self.method_call(): 
            if self.next_token() == "T_SEMICOLON"  or self.paren_stack:
                return True
            self.print_error("Syntax Error: expected semicolon")

        # if "(" Expr ")" Block [ else Block ] 
        elif self.token == "T_IF": 
            self.print_to_stack("IfStmt")
            self.indent_num += 1
            if self.next_token() == "T_LPAREN":
                self.next_token()
                if self.expr():
                    if self.next_token() == "T_RPAREN":
                        self.next_token()
                        if self.control_block():
                            self.indent_num -= 1
                            if self.next_token() == "T_ELSE":
                                self.next_token()
                                self.print_to_stack("ElseStmt: ")
                                self.indent_num += 1
                                self.control_block()
                                self.indent_num -= 1
                                return True
                            else:
                                self.backtrack()
                                return True
                        else:
                            self.print_error("Syntax Error: expected left bracket")
                    self.print_error("Syntax Error: expected right parenthesis")
                else:
                    self.print_error("Syntax Error: expected expression")
            else:
                self.print_error("Syntax Error: expected left parenthesis")
        
        # for "(" { Assign }+, ";" Expr ";" { Assign }+, ")" Block 
        elif self.token == "T_FOR": 
            self.print_to_stack("ForStmt")
            self.indent_num += 1
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
                                        if self.control_block():
                                            self.indent_num -= 1
                                            return True
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

        # while "(" Expr ")" Block 
        elif self.token == "T_WHILE":  
            self.print_to_stack("WhileStmt")
            self.indent_num += 1
            if self.next_token() == "T_LPAREN":
                self.next_token()
                self.expr()
                if self.next_token() == "T_RPAREN":
                    self.control_block()
                    self.indent_num -= 1
                    return True
            self.print_error("Syntax Error: statement()")

        # return [ "(" [ Expr ] ")" ] ";" 
        elif self.token == "T_RETURN":
            self.print_to_stack("ReturnStmt:")
            self.indent_num += 1
            if self.next_token() == "T_SEMICOLON":
                self.indent_num -= 1
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
                    self.indent_num -=1
                    return True
                
        # break ";" 
        elif self.token == "T_BREAK":
            self.print_to_stack("BreakStmt:")
            if self.next_token() == "T_SEMICOLON":
                return True
            else:
                self.print_error("Syntax Error: statement()")

        # continue ";"
        elif self.token == "T_CONTINUE":
            self.print_to_stack("ContinueStmt: ")
            if self.next_token() == "T_SEMICOLON":
                return True
            else:
                self.print_error("Syntax Error: statement()")
        else:
            return False
    # end statement()

    def unary_op(self):
        """
        Rule: UnaryOperator = ( UnaryNot | UnaryMinus ) .
        """
        if self.token == "T_NOT" or self.token == "T_MINUS":
            self.print_to_stack("UrnaryOp: %s" % self.my_scan.lexeme)
            return True
        else:
            return False
    # end unary_op()

    def bin_op(self):
        """
        Rule: BinaryOperator = ( ArithmeticOperator | BooleanOperator ) .
        """
        return self.arith_op() or self.bool_op()  
    # end bin_op  

    def arith_op(self):
        """
        Rule: ArithmentOperator = ( "+" | "-" | "*" | "/" | "<<" | ">>" | "%" )
        """
        if (self.token == "T_PLUS"
                or self.token == "T_MINUS"
                or self.token == "T_MULT"
                or self.token == "T_DIV"
                or self.token == "T_LEFTSHIFT"
                or self.token == "T_RIGHTSHIFT"
                or self.token == "T_MOD"):
            self.print_to_stack("BinOp:")
            self.indent_num += 1
            self.print_to_stack("ArithOp: %s" % self.my_scan.lexeme)
            self.indent_num -= 1
            return True
        else:
            return False
    # end arith_op()

    def bool_op(self):
        """
        Rule: BooleanOperator = ( "==" | "!=" | "<" | "<=" | ">" | ">=" | "&&" | "||" ) 
        """
        if (self.token == "T_EQ"
                or self.token == "T_NEQ"
                or self.token == "T_LT"
                or self.token == "T_LEQ"
                or self.token == "T_RT"
                or self.token == "T_REQ"
                or self.token == "T_AND"
                or self.token == "T_OR"):
            self.print_to_stack("BinOp:")
            self.indent_num += 1
            self.print_to_stack("BoolOp: %s" % self.my_scan.lexeme)
            self.indent_num -= 1
            return True
        else:
            return False
    # end bool_op()

    def expr(self):
        """
        Rule Expr =   Constant
                    | UnaryOperator Expr
                    | MethodCall
                    | Expr BinaryOperator Expr
                    | identifier
        """
        self.print_to_stack("Expr: ")
        self.indent_num += 1
        if self.constant(): # constant
            self.indent_num -= 1
            return True
        elif self.unary_op(): # unary operator
            self.next_token()
            if self.expr():
                self.indent_num -= 1
                return True
            else:
                self.print_error("Syntax Error: expr()")
        elif self.token == "T_IDENTIFIER": 
            if self.method_call(): # method_call
                self.indent_num -= 1
                return True
            self.print_to_stack("Identifier: %s " % self.my_scan.lexeme)
            self.next_token()
            if self.bin_op(): # binary operator
                self.next_token()
                if self.expr():
                    self.indent_num -= 1
                    return True
                else:
                    self.print_error("Syntax Error: expr()")
            else:
                self.print_stack.pop()
                self.backtrack()
                self.print_to_stack("Identifier: %s" % self.my_scan.lexeme)
            return True # identifier
        else:
            self.print_stack.pop()
            self.indent_num -= 1
            return False
    # end expr()

    def type(self):
        """
        Rule: Type = int
                    | string
                    | char
                    | bool
                    | float
        """
        return (self.token == "T_INTTYPE"
                or self.token == "T_STRINGTYPE"
                or self.token == "T_CHARTYPE"
                or self.token == "T_BOOLTYPE"
                or self.token == "T_FLOATTYPE")
    # end type()

    def method_type(self):
        """
        Rule: MethodType = void
                            | Type
        """
        return (self.token == "T_VOID"
                or self.type())
    # end method_type()

    def bool_constant(self):
        """
        Rule: BoolConstant = ( true | false )
        """
        return (self.token == "T_BoolConstant (value= true)"
                or self.token == "T_BoolConstant (value= false)")
    # end bool_constant()

    def array_type(self):
        """
        Rule: ArrayType = "[" int_lit "]" Type .
        """
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
        """
        Rule: Constant = int_lit
                        | string_lit
                        | char_lit
                        | BoolConstant
        """
        if (self.token == "T_INTCONSTANT"
            or self.token == "T_STRINGCONSTANT"
            or self.token == "T_CHARCONSTANT"
            or self.bool_constant()):

            line = self.my_scan.token_class
            line = line[2:]
            line = line + ": " + self.my_scan.lexeme
            self.print_to_stack(line)
            return self.token
        else:
            return False
    # end constant
# end My_Parser