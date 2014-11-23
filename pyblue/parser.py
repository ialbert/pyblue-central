"""
Parses the django template comments
"""
__author__ = 'ialbert'
import logging
from string import strip
import ply.lex as lex
import ply.yacc as yacc

logger = logging.getLogger(__name__)

tokens = (
    'NAME', 'NUMBER', 'FLOAT', 'EQUAL',
    'START', 'END', 'LPAREN', 'RPAREN', 'COMMA',
)

def DjagnoCommentLexer():

    # Regular expression rules for simple tokens
    t_EQUAL = r'='
    t_COMMA = r','
    t_LPAREN = r'\['
    t_RPAREN = r'\]'


    t_ignore = ' \t'

    def t_START(t):
        r'{\#'
        t.lexer.inside = True
        return t

    def t_END(t):
        r'\#}'
        t.lexer.inside = False
        return t

    def t_FLOAT(t):
        r'\d+\.\d+'
        t.value = float(t.value)
        return t

    def t_NUMBER(t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_NAME(t):
        r'[\w!?\+]+'
        return t

    def t_error(t):
        if t.lexer.inside:
            print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)

    return lex.lex()

# Grammar definition

def p_expression_factor(p):
    'expression :  START NAME EQUAL factor END'
    p.lexer.meta[p[2]] = p[4]

def p_factor_flt(p):
    'factor : FLOAT'
    p[0] = p[1]

def p_factor_int(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_name(p):
    'factor : NAME'
    p[0] = p[1]

def p_factor_list(p):
    'factor : list'
    p[0] = p[1]

def p_factor_factor(p):
    'factor : factor factor'
    p[0] = str(p[1]) + ' ' + str(p[2])

def p_elem_one(p):
    'elem : factor'
    p[0] = [p[1]]

def p_elem_two(p):
    'elem : elem COMMA elem'
    p[0] = p[1] + p[3]

def p_list_def(p):
    'list : LPAREN elem RPAREN'
    p[0] = p[2]

def p_error(p):
    logger.error("syntax error in %s while parsing: %s" % (p.lexer.fname, p.lexer.lexdata))

def process(lines, fname="text"):
    lines = map(strip, lines)
    # Only process lines that are comments.
    lines = filter(lambda x: x.startswith("{#"), lines)
    lexer = DjagnoCommentLexer()
    lexer.fname=fname
    lexer.meta = {}
    parser = yacc.yacc(write_tables=0, debug=0)
    for line in lines:
        parser.parse(line, lexer=lexer)
    return lexer.meta

def test():
    text = """
    This is a test document. Only tags in comments will be parsed.

    {# title = Page Title #}

    {#  name = Hello #}

    {# x = AAA BBB CCC + some other 34 stuff!!!? #}

    {# y = zum123 + 234 #}

    {# ggg = 3.1 #}

    This should raise a sytax error

    {# abc #}

    aaa = 123

    {# value = [ 10, 20, hello world ] #}

    <body>Done!</body>
    """

    lines = text.splitlines()
    meta = process(lines)
    print meta

if __name__ == '__main__':
    logging.basicConfig()
    test()