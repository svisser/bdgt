from bdgt.importer.parsers.mt940 import Mt940Parser


class TxParserFactory(object):
    @classmethod
    def create(cls, type_):
        if type_ == 'mt940':
            return Mt940Parser()
        else:
            raise ValueError("Unknown parser type '{}'".format(type_))
