import logging
from collections import defaultdict

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from bdgt.importer.types import ImporterError
from bdgt.importer.parsers.factory import TxParserFactory
from bdgt.models import Account, Transaction
from bdgt.storage.gateway import save_objects, session_scope


_log = logging.getLogger(__name__)


class CmdImport(object):
    def __init__(self, account_name, type_, file_):
        with session_scope() as session:
            self.account = session.query(Account) \
                                  .filter_by(name=account_name) \
                                  .one()
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
        converted_txs = []
        for parsed_tx in parsed_txs:
            if parsed_tx.account is not None and \
               parsed_tx.account != self.account.number:
                msg = "Transaction is for account number '{}' not '{}'".format(
                        parsed_tx.account, self.account.number)
                _log.error(msg)
                raise ImportError(msg)

            converted_tx = Transaction(self.account,
                                       parsed_tx.date,
                                       parsed_tx.description,
                                       parsed_tx.amount)
            converted_txs.append(converted_tx)
        save_objects(converted_txs)

        # Compose output string
        output = "Imported {} transactions into account '{}'\n".format(
                len(converted_txs), self.account.name)
        return output
