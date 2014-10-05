from bdgt.importer.parsers.mt940 import Mt940Parser
from bdgt.importer.parsers.ofx import OfxParser


class TxParserFactory(object):
    @classmethod
    def create(cls, type_):
        if type_ == 'mt940':
            return Mt940Parser()
        elif type_ == 'ofx':
            return OfxParser()
        else:
            raise ValueError("Unknown parser type '{}'".format(type_))
