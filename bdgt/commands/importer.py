import logging
from collections import defaultdict

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from bdgt.importer.types import ImporterError
from bdgt.importer.parsers.factory import TxParserFactory
from bdgt.models import Account, Transaction
from bdgt.storage.gateway import save_objects, session_scope


_log = logging.getLogger(__name__)


class CmdImport(object):
    def __init__(self, type_, file_):
        self.type_ = type_
        self.file_ = file_

    def __call__(self):
        # Parse the mt940 file
        parser = TxParserFactory.create(self.type_)
        parsed_txs = parser.parse(self.file_)

        _log.info("Parsed {} transactions from '{}'".format(len(parsed_txs),
                                                            self.file_))

        # Convert the imported transactions to real transactions and save to
        # the database. If there is a problem converting, nothing is saved.
        converted_txs = defaultdict(list)
        for parsed_tx in parsed_txs:
            with session_scope() as session:
                try:
                    account = session.query(Account) \
                                     .filter_by(number=parsed_tx.account) \
                                     .one()
                except (NoResultFound, MultipleResultsFound):
                    raise ImporterError("Account with number '{}' not found.".format(parsed_tx.account))

            converted_tx = Transaction(account,
                                       parsed_tx.date,
                                       parsed_tx.description,
                                       parsed_tx.amount)
            converted_txs[account.name].append(converted_tx)

        # Put all converted transactions into a single list.
        all_converted_txs = []
        for k, v in converted_txs.iteritems():
            all_converted_txs.extend(v)
        save_objects(all_converted_txs)

        # Compose output string
        output = ""
        for account_name, txs in converted_txs.iteritems():
            output += "Imported {} transactions into account '{}'\n".format(
                len(txs), account_name)
        return output
