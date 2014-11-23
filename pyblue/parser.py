"""
    Parses the django template comments
"""
__author__ = 'ialbert'
from string import strip
import ply.lex as lex
import ply.yacc as yacc

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
def p_term_expr(p):
    'term : name EQUAL factor'

    # Only store mapping inside comments.
    if p.lexer.inside:
        p.lexer.meta[p[1]] = p[3]
    p[0] = p[2]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]


def p_term_start(p):
    'term : start'
    p[0] = p[1]


def p_term_end(p):
    'term : end'
    p[0] = p[1]


def p_name_def(p):
    'name : NAME'
    p[0] = p[1]


def p_factor_name(p):
    'factor : name'
    p[0] = p[1]


def p_factor_list(p):
    'factor : list'
    p[0] = p[1]


def p_factor_int(p):
    'factor : NUMBER'
    p[0] = p[1]


def p_factor_flt(p):
    'factor : FLOAT'
    p[0] = p[1]


def p_factor_factor(p):
    'factor : factor factor'
    p[0] = str(p[1]) + ' ' + str(p[2])


def p_start_def(p):
    'start : START'
    global collect
    collect = True


def p_end_def(p):
    'end : END'
    global collect
    collect = False


def p_elem_1(p):
    'elem : factor'
    p[0] = [p[1]]


def p_elem_def(p):
    'elem : elem COMMA elem'
    p[0] = p[1] + p[3]


def p_list_def(p):
    'list : LPAREN elem RPAREN'
    p[0] = p[2]


def p_error(p):
    if p.lexer.inside:
        print "*** syntax error in input!"


def process(lines):
    lines = map(strip, lines)
    lines = filter(None, lines)
    lexer = DjagnoCommentLexer()
    lexer.inside = False
    lexer.meta = {}
    parser = yacc.yacc(write_tables=0, debug=0)
    for line in lines:
        parser.parse(line, lexer=lexer)

    return lexer.meta

def test():
    text = """
    ABC
    {#
        x = AAA BBB CCC + some other 34 stuff!!!?
        y = zum123 + 234
        z = 100
        ggg = 3.1
        e = [ abc, efg, 123 s, !@#$%^&*()_+-= ]
    #}
    aaa = 123

    <%inherit file="../base.mako"/>
    <%namespace file="../extensions.mako" import="*"/>
    <html>
    """

    lines = text.splitlines()
    meta = process(lines)
    print meta

if __name__ == '__main__':
    test()