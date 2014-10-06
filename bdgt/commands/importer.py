import logging
import os
from collections import defaultdict
from StringIO import StringIO

import asciitable
import yaml
from colorama import Fore
from sqlalchemy.orm.exc import NoResultFound

from bdgt import get_data_dir
from bdgt.commands import ParseIdMixin
from bdgt.importer.parsers import TxParserFactory
from bdgt.models import Account
from bdgt.storage.database import session_scope


_log = logging.getLogger(__name__)

_IMPORT_YAML_PATH = os.path.join(get_data_dir(), 'import.yaml')


class BaseCmdImport(object):
    @classmethod
    def _load_parsed_txs(cls, file_obj):
        return yaml.load(file_obj)

    @classmethod
    def _save_parsed_txs(cls, parsed_txs, file_obj):
        yaml.dump(parsed_txs, file_obj)


class CmdAdd(BaseCmdImport, ParseIdMixin):
    def __init__(self, tx_ids):
        if not os.path.exists(_IMPORT_YAML_PATH):
            raise ValueError("You must import transactions first.")

        self.tx_ids = self._parse_tx_ids(tx_ids)

    def __call__(self):
        with open(_IMPORT_YAML_PATH, 'r') as f:
            i_txs = self._load_parsed_txs(f)

        num_processed = 0
        for i, i_tx in enumerate(i_txs, start=1):
            # Check that the account number in the transaction matches an
            # existing account. If not, the process is halted; however, any
            # transactions that have been processed remain so.
            with session_scope() as session:
                try:
                    session.query(Account)\
                           .filter_by(number=i_tx.parsed_tx.account)\
                           .one()
                except NoResultFound:
                    raise ValueError(
                        "Account number '{}' does not exist.".format(
                            i_tx.parsed_tx.account))

            if i in self.tx_ids:
                i_tx.processed = True
                num_processed += 1

        assert num_processed == len(self.tx_ids)

        # Write the changes back to the file.
        with open(_IMPORT_YAML_PATH, "w+") as f:
            self._save_parsed_txs(i_txs, f)

        return "{} transactions added to the staging area.".format(
            num_processed)


class CmdRemove(BaseCmdImport, ParseIdMixin):
    def __init__(self, tx_ids):
        if not os.path.exists(_IMPORT_YAML_PATH):
            raise ValueError("You must import transactions first.")

        self.tx_ids = self._parse_tx_ids(tx_ids)

    def __call__(self):
        with open(_IMPORT_YAML_PATH, 'r') as f:
            i_txs = self._load_parsed_txs(f)

        num_processed = 0
        for i, i_tx in enumerate(i_txs, start=1):
            if i in self.tx_ids:
                i_tx.processed = False
                num_processed += 1

        assert num_processed == len(self.tx_ids)

        # Write the changes back to the file.
        with open(_IMPORT_YAML_PATH, "w+") as f:
            self._save_parsed_txs(i_txs, f)

        return "{} transactions removed from the staging area.".format(
            num_processed)


class CmdImport(BaseCmdImport):
    def __init__(self, file_type, file_path):
        if os.path.exists(_IMPORT_YAML_PATH):
            raise ValueError("A previous import has not been processed.")

        self.file_type = file_type
        self.file_path = file_path

    def __call__(self):
        # Parse the transactions from the file
        parser = TxParserFactory.create(self.file_type)
        parsed_txs = parser.parse(self.file_path)

        _log.info("Parsed {} transactions from '{}'".format(len(parsed_txs),
                                                            self.file_path))

        # Write the transactions to the intermediary file in the bdgt data dir.
        # This is used by the "bdgt import add" and "bdgt import commit"
        # commands.
        with open(_IMPORT_YAML_PATH, "w+") as f:
            self._save_parsed_txs(parsed_txs, f)

        output = "Parsed {} transactions from {}.".format(len(parsed_txs),
                                                          self.file_path)
        return output


class CmdStatus(BaseCmdImport):
    def __init__(self):
        if not os.path.exists(_IMPORT_YAML_PATH):
            raise ValueError("You must import transactions first.")

    def __call__(self):
        with open(_IMPORT_YAML_PATH, 'r') as f:
            i_txs = self._load_parsed_txs(f)

        processed_output = defaultdict(list)
        unprocessed_output = defaultdict(list)
        for i, i_tx in enumerate(i_txs, start=1):
            if i_tx.processed:
                output = processed_output
            else:
                output = unprocessed_output

            output['id'].append(i)
            output['date'].append(str(i_tx.parsed_tx.date))
            output['account'].append(str(i_tx.parsed_tx.account))
            output['description'].append(
                i_tx.parsed_tx.description[:130].replace('\n', ' '))
            output['amount'].append(float(i_tx.parsed_tx.amount))
            output['category'].append(i_tx.category)

        output_io = StringIO()

        def format_amount(x):
            if x < 0:
                color = Fore.RED
            else:
                color = Fore.GREEN
            output = "{}{:.2f}{}".format(color, x, Fore.RESET)
            return output

        if processed_output:
            output_io.write("Transactions ready to commit:\n\n")
            asciitable.write(
                processed_output, output_io,
                Writer=asciitable.FixedWidthNoHeader,
                names=['id', 'date', 'account', 'description', 'category',
                       'amount'],
                formats={'amount': lambda x: format_amount(x)})
            if unprocessed_output:
                output_io.write("\n")

        if unprocessed_output:
            output_io.write("Transactions ready for processing:\n\n")
            asciitable.write(
                unprocessed_output, output_io,
                Writer=asciitable.FixedWidthNoHeader,
                names=['id', 'date', 'account', 'description', 'category',
                       'amount'],
                formats={'amount': lambda x: format_amount(x)})

        return output_io.getvalue()
