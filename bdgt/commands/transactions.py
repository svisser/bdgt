from collections import defaultdict
from StringIO import StringIO

import asciitable
from colorama import Fore
from sqlalchemy.orm.exc import NoResultFound

from bdgt.storage.database import session_scope
from bdgt.storage.gateway import save_objects
from bdgt.models import Category, Transaction


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
            output['id'].append(tx.id)
            output['date'].append(str(tx.date))
            output['description'].append(tx.description[:30])
            output['amount'].append(tx.amount)
            output['reconciled'].append(tx.reconciled)
            if tx.category:
                output['category'].append(tx.category.name)
            else:
                output['category'].append('')

        def format_amount(x):
            if x < 0:
                color = Fore.RED
            else:
                color = Fore.GREEN
            output = "{}{:.2f}{}".format(color, x, Fore.RESET)
            return output

        output_io = StringIO()
        asciitable.write(output, output_io,
                         Writer=asciitable.FixedWidthNoHeader,
                         names=['id', 'date', 'description', 'category',
                                'reconciled', 'amount'],
                         formats={'amount': lambda x: format_amount(x),
                                  'reconciled': lambda x: 'Y' if x else 'N'})

        return output_io.getvalue()


class ParseIdMixin(object):
    def _parse_tx_ids(self, tx_ids):
        parsed_ids = []
        for tx_id in tx_ids.split(','):
            if '-' in tx_id:
                tx_id_range = tx_id.split('-')
                assert len(tx_id_range) == 2

                beg = int(tx_id_range[0])
                end = int(tx_id_range[1]) + 1
                parsed_ids.extend([x for x in range(beg, end)])
            else:
                parsed_ids.append(int(tx_id))
        # Remove duplicates by converting to a set and back
        return list(set(parsed_ids))


class CmdAssignTx(ParseIdMixin):
    def __init__(self, category_name, tx_ids):
        self.tx_ids = self._parse_tx_ids(tx_ids)
        self.category_name = category_name.lower()

    def __call__(self):
        # Get the category if it already exists, or create a new one.
        with session_scope() as session:
            try:
                category = session.query(Category) \
                                  .filter_by(name=self.category_name) \
                                  .one()
            except NoResultFound:
                category = Category(self.category_name)

        # Get the transactions
        with session_scope() as session:
            txs = session.query(Transaction) \
                         .filter(Transaction.id.in_(self.tx_ids)) \
                         .all()

        # Assign the category to the transactions
        for tx in txs:
            tx.category = category

        save_objects(txs)

        return ("Assigned {} transactions to the {} " +
                "category").format(len(txs), self.category_name)


class CmdUnassignTx(ParseIdMixin):
    def __init__(self, tx_ids):
        self.tx_ids = self._parse_tx_ids(tx_ids)

    def __call__(self):
        # Get the transactions
        with session_scope() as session:
            txs = session.query(Transaction) \
                         .filter(Transaction.id.in_(self.tx_ids)) \
                         .all()

        # Unassign the category
        for tx in txs:
            tx.category = None

        save_objects(txs)

        return ("Unassigned {} transactions from their " +
                "category").format(len(txs))


class CmdReconcileTx(ParseIdMixin):
    def __init__(self, tx_ids):
        self.tx_ids = self._parse_tx_ids(tx_ids)

    def __call__(self):
        # Get the transactions
        with session_scope() as session:
            txs = session.query(Transaction) \
                         .filter(Transaction.id.in_(self.tx_ids)) \
                         .all()

        # Unassign the category
        for tx in txs:
            tx.reconciled = True

        save_objects(txs)

        return ("Reconciled {} transactions").format(len(txs))
