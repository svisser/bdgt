from __future__ import absolute_import

import os
import re
import tempfile

from ofxparse import OfxParser as OfxLibParser

from bdgt.importer.types import ParsedTransaction


class OfxParser(object):
    def parse(self, file_):
        # ofxparse workaround
        # ofxparse doesn't parse the transaction amount correctly. It assumes
        # that the decimal point separator is always a full-stop; however, it
        # depends on the locale of the statement.
        #
        # This workaround finds the transaction amount in the file and replaces
        # comma with a full-stop. A temporary file is used to make the change
        # so the original file data stays intact.
        with open(file_) as f:
            data = f.read()
        data = re.sub(r'<TRNAMT>([-\d]+),([\d]+)', r'<TRNAMT>\1.\2', data)

        ofx_file = tempfile.NamedTemporaryFile(delete=False)
        try:
            with ofx_file as f:
                f.write(data)

            # Actual parsing
            ofx = OfxLibParser.parse(file(ofx_file.name))
            i_txs = []
            for p_acc in ofx.accounts:
                for p_tx in p_acc.statement.transactions:
                    i_tx = ParsedTransaction(p_tx.date.date(), p_tx.amount,
                                             unicode(p_acc.number),
                                             unicode(p_tx.memo))
                    i_txs.append(i_tx)
            return i_txs
        finally:
            os.remove(ofx_file.name)