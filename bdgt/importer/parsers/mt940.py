from __future__ import absolute_import

from mt940 import MT940

from bdgt.importer.types import ParsedTransaction


class Mt940Parser(object):
    def parse(self, file_):
        mt940 = MT940(file_)
        i_txs = []
        for p_stmt in mt940.statements:
            for p_tx in p_stmt.transactions:
                i_tx = ParsedTransaction(p_tx.booking, p_tx.amount,
                                         unicode(p_tx.account),
                                         unicode(p_tx.description))
                i_txs.append(i_tx)
        return i_txs
