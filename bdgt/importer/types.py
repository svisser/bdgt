from collections import namedtuple


ParsedTransaction = namedtuple('ParsedTransaction',
                               ['date', 'amount', 'account', 'description'])


class ImporterError(RuntimeError):
    pass
