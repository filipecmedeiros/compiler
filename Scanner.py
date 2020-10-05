from utils import BLANK, is_digit, is_letter

class Scanner:

    def __init__(self, file):
        self.file = file
        self.line = 1
        self.column = 1
        self.buffer = ""
        self.last_token = (None, "")


    def print_last_token(self):
        print ('Last Token: ', self.last_token)


    def read(self):
        char = self.file.read(1)
        if not char:
            return None
        else:
            char = str(char)

        if char == '\n':
            self.column = 1
            self.line = self.line + 1
        else:
            self.column = self.column + 1
        
        return char        


    def error(self, message="default"):
        print ("Erro na linha {line}, coluna {column}. Ultimo token lido: {token} \n {message}".format(
            line=self.line, column=self.column, token=self.last_token, message=message))
        exit(1)


    def get_no_blank(self, char):

        while char in BLANK:
            char = self.read()
        return char


    def _int(self, char):

        while(is_digit(char)):
            self.buffer = self.buffer + char
            lookahead = self.read()

            if lookahead == None:
                break
            elif lookahead == '.':
                return self._float(lookahead)

            char = lookahead
            
        return (1, self.buffer), lookahead


    def _float(self, char):
        
        self.buffer = self.buffer + char
        lookahead = self.read()

        if not is_digit(lookahead):
            self.error('float mal formado')

        char = lookahead

        while(is_digit(char)):
            self.buffer = self.buffer + char
            lookahead = self.read()

            if lookahead == None:
                break
            char = lookahead
            
        return (2, self.buffer), lookahead


    def _char(self, char):
        self.buffer = self.buffer + char
        lookahead = self.read()

        if (not is_digit(lookahead)) and (not is_letter(lookahead)):
            self.error('char mal formado')

        char = lookahead
        self.buffer = self.buffer + char
        lookahead = self.read()

        if lookahead != "'":
            self.error('char mal formado')

        char = lookahead
        self.buffer = self.buffer + char
        lookahead = self.read()

        return (3, self.buffer), lookahead

    def _add(self, char):
        self.buffer = self.buffer + char
        lookahead = self.read()
        return (4, self.buffer), lookahead

    def _sub(self, char):
        self.buffer = self.buffer + char
        lookahead = self.read()
        return (5, self.buffer), lookahead

    def _mul(self, char):
        self.buffer = self.buffer + char
        lookahead = self.read()
        return (6, self.buffer), lookahead


    def _div(self, char):
        lookahead = self.read()

        if lookahead == '/':
            return self._one_line_comment('/')

        elif lookahead == '*':
            return self._multiline_comment('*')

        self.buffer = self.buffer + char
        return (7, self.buffer), lookahead

    
    def _one_line_comment(self, char):
        lookahead = self.read()

        while char != '\n':
            char = lookahead
            lookahead = self.read()

            if char is None:
                return None, None
        return self.get_token(lookahead)

    
    def _multiline_comment(self, char):
        char = self.read()
        lookahead = self.read()
        
        if char == None or lookahead == None:
            self.error('Comentario de multilinha')
        
        while (char != '*' and lookahead != '/'):
            char = lookahead
            lookahead = self.read()

            if lookahead == None:
                self.error('Comentario de multilinha')

        char = lookahead
        lookahead = self.read()
        return self.get_token(lookahead)

    def _attr(self, char):
        self.buffer = self.buffer + char
        lookahead = self.read()

        if lookahead == '=':
            return self._equal(lookahead)        

        return (8, self.buffer), lookahead

    def _equal(self, char):
        self.buffer = self.buffer + char
        lookahead = self.read()

        return (9, self.buffer), lookahead


    def _min(self, char):
        self.buffer = self.buffer + char
        lookahead = self.read()

        if lookahead == '=':
            return self._min_equal(lookahead)        

        return (10, self.buffer), lookahead


    def _min_equal(self, char):
        self.buffer = self.buffer + char
        lookahead = self.read()

        return (11, self.buffer), lookahead


    def _max(self, char):
        self.buffer = self.buffer + char
        lookahead = self.read()

        if lookahead == '=':
            return self._max_equal(lookahead)        

        return (12, self.buffer), lookahead


    def _max_equal(self, char):
        self.buffer = self.buffer + char
        lookahead = self.read()

        return (13, self.buffer), lookahead


    def _diff(self, char):
        self.buffer = self.buffer + char
        lookahead = self.read()

        if lookahead != '=':
            self.error('operador invalido')

        char = lookahead
        self.buffer = self.buffer + char
        lookahead = self.read()

        return (14, self.buffer), lookahead

    def get_token(self, char):
        self.buffer = ""
        lookahead = None

        char = self.get_no_blank(char)

        if char is None: #EOF
            self.last_token = None
            lookahead = None
        elif is_digit(char):
            self.last_token, lookahead = self._int(char)
        elif char == '.':
            self.last_token, lookahead = self._float(char)
        elif char == "'":
            self.last_token, lookahead = self._char(char)
        elif char == '+':
            self.last_token, lookahead = self._add(char)
        elif char == '-':
            self.last_token, lookahead = self._sub(char)
        elif char == '*':
            self.last_token, lookahead = self._mul(char)
        elif char == '/':
            self.last_token, lookahead = self._div(char)
        elif char == '=':
            self.last_token, lookahead = self._attr(char)
        elif char == '<':
            self.last_token, lookahead = self._min(char)
        elif char == '>':
            self.last_token, lookahead = self._max(char)
        elif char == '!':
            self.last_token, lookahead = self._diff(char)

        return self.last_token, lookahead







