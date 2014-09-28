import datetime
import os
import tempfile
from decimal import Decimal

from nose.tools import eq_, ok_

from bdgt.importer.parsers.mt940 import Mt940Parser


def test_parse():
    mt940_file = tempfile.NamedTemporaryFile(delete=False)
    try:
        with mt940_file as f:
            f.write("ABNANL2A\n" +
                    "940\n" +
                    "ABNANL2A\n" +
                    ":20:ABN AMRO BANK NV\n" +
                    ":25:123456789\n" +
                    ":28:13501/1\n" +
                    ":60F:C120511EUR5138,61\n" +
                    ":61:1205120514C500,01N654NONREF\n" +
                    "987654321\n" +
                    ":86:/TRTP/SEPA OVERBOEKING/IBAN/FR12345678901234/BIC/GEFRADAM\n" +
                    "/NAME/QASD JGRED/REMI/description lines/EREF/NOTPRO\n" +
                    "VIDED\n" +
                    ":62F:C120514EUR5638,62\n")
        parser = Mt940Parser()
        txs = parser.parse(mt940_file.name)
        eq_(len(txs), 1)
        eq_(txs[0].date, datetime.date(2012, 5, 14))
        eq_(txs[0].account, '987654321')
        ok_('description lines' in txs[0].description)
        eq_(txs[0].amount, Decimal('500.01'))
    finally:
        os.remove(mt940_file.name)
