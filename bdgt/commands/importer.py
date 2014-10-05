import logging
import os

import yaml

from bdgt import get_data_dir
from bdgt.importer.parsers import TxParserFactory


_log = logging.getLogger(__name__)


class CmdImport(object):
    def __init__(self, file_type, file_path):
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
        data_dir = get_data_dir()
        with open(os.path.join(data_dir, 'import.yaml'), "w+") as f:
            self._save_parsed_txs(parsed_txs, f)

        output = "Parsed {} transactions from {}.".format(len(parsed_txs),
                                                          self.file_path)
        return output

    @classmethod
    def _save_parsed_txs(cls, parsed_txs, file_obj):
        yaml.dump(parsed_txs, file_obj)
