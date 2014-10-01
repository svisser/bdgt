from nose.tools import ok_, raises

from bdgt.importer.parsers.mt940 import Mt940Parser
from bdgt.importer.parsers.factory import TxParserFactory


def test_tx_parser_factory():
    parser = TxParserFactory.create("mt940")
    ok_(isinstance(parser, Mt940Parser))


@raises(ValueError)
def test_tx_parser_factory_unknown_type():
    TxParserFactory.create("unknown")
