import warnings
warnings.simplefilter('error')

import datetime
from decimal import Decimal

from mock import patch
from nose.tools import eq_, raises, with_setup
from sqlalchemy import create_engine

from bdgt.commands.importer import CmdImport
from bdgt.importer.types import ParsedTransaction
from bdgt.models import Account, Transaction
from bdgt.storage.database import Base, Session, session_scope
from bdgt.storage.gateway import save_object


def setup():
    global engine
    engine = create_engine('sqlite://', echo=False)
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)


def teardown():
    engine.dispose()
    Session.remove()


@patch('bdgt.importer.parsers.Mt940Parser')
@with_setup(setup, teardown)
def test_cmd_import_mt940(mock_mt940_parser):
    save_object(Account(u'test', u'987654321'))

    mock_mt940_parser.return_value.parse.return_value = [
        ParsedTransaction(datetime.date(2014, 11, 30),
                          Decimal('193.45'),
                          u"987654321",
                          u"desc")]

    CmdImport(u"test", "mt940", "data.mt940")()
    with session_scope() as session:
        num = session.query(Transaction).count()
        eq_(num, 1)


@raises(ImportError)
@with_setup(setup, teardown)
def test_cmd_import_mt940_incorrect_account():
    CmdImport(u"doesn't_exist", "mt940", "data.mt940")()
