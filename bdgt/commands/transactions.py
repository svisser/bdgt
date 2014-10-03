import asciitable
from collections import defaultdict
from StringIO import StringIO

from bdgt.storage.database import session_scope
from bdgt.models import Transaction


class CmdListTx(object):
    def __init__(self, account_name):
        self.account_name = account_name

    def __call__(self):
        # Get all the transactions
        with session_scope() as session:
            txs = session.query(Transaction) \
                         .filter(Transaction.account.has(
                             name=self.account_name)) \
                         .order_by(Transaction.date) \
                         .all()

        output = defaultdict(list)
        for tx in txs:
            output['date'].append(str(tx.date))
            output['description'].append(tx.description[:30])
            output['amount'].append(tx.amount)
            output['reconciled'].append(tx.reconciled)
        output_io = StringIO()
        asciitable.write(output, output_io,
                         Writer=asciitable.FixedWidthNoHeader,
                         names=['date', 'description', 'amount', 'reconciled'],
                         formats={'amount': '%.2f',
                                  'reconciled': lambda x: 'Y' if x else 'N'})

        return output_io.getvalue()
