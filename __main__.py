from sly import Lexer, Parser
import discord
from discord.ext import commands
class DBLLexer(Lexer): 

    tokens = { NAME, NUMBER, STRING , PRINT,TOKEN,PREFIX,CMD} 

    ignore = '\t '

    literals = { '=' ,'+', '-', '/',  

                '*', '(', ')', ',', ';'} 

  

  

    # Define tokens as regular expressions 

    # (stored as raw strings) 

    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

    STRING = r'\".*?\"'
    #ID=r'[a-zA-Z_][a-zA-Z_]*'
    #NAME['3']=COLON
    # Number token 
    NAME['print']=PRINT
    NAME['TOKEN']=TOKEN
    NAME['PREFIX']=PREFIX
    NAME['command']=CMD

    @_(r'\d+') 

    def NUMBER(self, t): 

        

        # convert it into a python integer 

        t.value = int(t.value)  

        return t 
    '''
    @_(r'SYNTAX "=" STRING')
    def statement(self, t):
        return t
    '''
    # Comment token 

    @_(r'//.*') 

    def COMMENT(self, t): 

        pass

  

    # Newline token(used only for showing 

    # errors in new line) 

    @_(r'\n+') 

    def newline(self, t): 

        self.lineno = t.value.count('\n')



class DBLParser(Parser): 

    #tokens are passed from lexer to parser 

    tokens = DBLLexer.tokens 

  

    precedence = ( 

        ('left', '+', '-'), 

        ('left', '*', '/'), 

        ('right', 'UMINUS'), 

    ) 

  

    def __init__(self): 

        self.env = { } 

  

    @_('') 

    def statement(self, p): 

        pass

  

    @_('var_assign') 

    def statement(self, p): 

        return p.var_assign 


    @_('NAME "=" expr') 

    def var_assign(self, p): 

        return ('var_assign', p.NAME, p.expr) 

  

    @_('NAME "=" STRING') 

    def var_assign(self, p): 

        return ('var_assign', p.NAME, p.STRING) 

  

    @_('expr') 

    def statement(self, p): 

        return (p.expr) 

  

    @_('expr "+" expr') 

    def expr(self, p): 

        return ('add', p.expr0, p.expr1) 

    @_('CMD NAME "(" .* ")"')
    def statement(self,p):
        return ('command',p.NAME) #,p.)

    @_('expr "-" expr') 

    def expr(self, p): 

        return ('sub', p.expr0, p.expr1) 

    @_('PRINT expr')
    def statement(self,p):
       return ('print',p.expr)

    @_('PRINT STRING')
    def statement(self,p):
       return ('print',p.STRING)
    @_('TOKEN STRING')
    def statement(self,p):
       return ('token',p.STRING)
    @_('PREFIX NAME')
    def statement(self,p):
       return ('prefix',p.NAME)

    @_('expr "*" expr') 

    def expr(self, p): 

        return ('mul', p.expr0, p.expr1) 

  

    @_('expr "/" expr') 

    def expr(self, p): 

        return ('div', p.expr0, p.expr1) 

  

    @_('"-" expr %prec UMINUS') 

    def expr(self, p): 

        return p.expr 

  

    @_('NAME') 

    def expr(self, p): 

        return ('var', p.NAME) 

  

    @_('NUMBER') 

    def expr(self, p): 

        return ('num', p.NUMBER)


class DBLExecute: 

    

    def __init__(self, tree, env): 

        self.env = env 

        result = self.walkTree(tree) 

        if result is not None and isinstance(result, int): 

            print(result) 

        if isinstance(result, str) and result[0] == '"': 

            print(result) 

  

    def walkTree(self, node): 

  

        if isinstance(node, int): 

            return node 

        if isinstance(node, str): 

            return node 

  

        if node is None: 

            return None

  

        if node[0] == 'program': 

            if node[1] == None: 

                self.walkTree(node[2]) 

            else: 

                self.walkTree(node[1]) 

                self.walkTree(node[2]) 

  

        if node[0] == 'num': 

            self.walkTree(node[1])
        if node[0] == 'print':
            return self.walkTree(node[1])
            
        if node[0]=='prefix':
            Bot_var = commands.Bot(node[1])
            self.env['Bot_var'] = Bot_var
            return f'prefix set as {node[1]}'
        if node[0] == 'token':
            Bot_var = self.env['Bot_var']
            Bot_var.run(node[1].replace('"',''))
            #print('Server running')
            #return node[1]
        if node[0] == 'str': 

            return node[1] 

  

        if node[0] == 'add': 

            return self.walkTree(node[1]) + self.walkTree(node[2]) 

        elif node[0] == 'sub': 

            return self.walkTree(node[1]) - self.walkTree(node[2]) 

        elif node[0] == 'mul': 

            return self.walkTree(node[1]) * self.walkTree(node[2]) 

        elif node[0] == 'div': 

            return self.walkTree(node[1]) / self.walkTree(node[2]) 

  

        if node[0] == 'var_assign': 

            self.env[node[1]] = self.walkTree(node[2]) 

            return node[1] 

  

        if node[0] == 'var': 

            try: 

                return self.env[node[1]] 

            except LookupError: 

                print("Undefined variable '"+node[1]+"' found!") 

                return 0

if __name__ == '__main__': 

    lexer = DBLLexer() 

    parser = DBLParser() 

    print('Discord Bot Language') 

    env = {} 

      

    while True: 

          

        try: 

            text = input('DBL> ') 

          

        except EOFError: 

            break

          

        if text: 

            tree = parser.parse(lexer.tokenize(text)) 

            BasicExecute(tree, env)
