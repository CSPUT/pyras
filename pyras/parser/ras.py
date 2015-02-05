#!/usr/bin/env python

from pyparsing import Literal, Word, alphas, alphanums, Optional, ZeroOrMore, ParseException, Forward, Group, Combine, Or


class RasParser(object):

    def __init__(self):
        pass
# http://sourceforge.net/p/pyparsing/mailman/pyparsing-users/thread/4E8B3555.1090404@cs.wisc.edu/

    def grammar(self):
        prefix_op = Literal('.')
        parallel = Literal('|')
        comm_op = Literal('||')
        choice_op = Literal('+')
        colon = Literal(':')
        loca_sym = Literal('@').suppress()
        lpar = Literal('(').suppress()
        rpar = Literal(')').suppress()
        pound = Literal('#').suppress()
        slash = Literal('/')
        # 8
        lbra = Literal('{').suppress()
        rbra = Literal('}').suppress()
        define = Literal('=')
        Ident = Word(alphas.upper(), alphanums + "_")
        ident = Word(alphas.lower(), alphanums + "_")
        pragma = Optional(pound + Literal('language') + colon + 'ras')
        # pseudo uri: /a/s/s/s/s/ or /a/ or /a/s/s/s
        puri = Combine(slash + ident + ZeroOrMore(slash + ident) + Optional(slash))
        loca = loca_sym + puri 

        comm = Forward()
        choice = Forward()
        prefix = Forward()

        process = ident | loca + lbra + choice + rbra | lpar + choice + rpar
        prefix << Group(process + ZeroOrMore(prefix_op + prefix) )
        choice << Group(prefix + ZeroOrMore(choice_op + prefix))
        comm << Group(choice + ZeroOrMore(comm_op + comm ))
        rmdef = Ident + define + loca+ lbra + comm + rbra
        ras = pragma + rmdef

        return ras

    def parse(self, string):

        try:
            oo = self.grammar().parseString(string, parseAll=True).asList()
            # print(repr(oo))
            print(type(oo))
            print(oo)
        except ParseException as e:
            raise

if __name__ == "__main__":
    p = RasParser()
    p.parse("A=@/x/{a.a.s + s + @/o/{a.dd + s.d}}")
