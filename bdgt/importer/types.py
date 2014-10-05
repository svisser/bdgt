from collections import namedtuple


ParsedTx = namedtuple('ParsedTx', ['date', 'amount', 'account', 'description'])


class ImportTx(object):
    def __init__(self, parsed_tx):
        self._parsed_tx = parsed_tx

    @property
    def parsed_tx(self):
        return self._parsed_tx
