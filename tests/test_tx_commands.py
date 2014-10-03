from nose.tools import eq_

from bdgt.commands.transactions import CmdAssignTx


def test_cmd_assign_tx_parse_tx_ids():
    cmd = CmdAssignTx('1,2,3', 'cat1')
    eq_(cmd.tx_ids, [1, 2, 3])


def test_cmd_assign_tx_parse_tx_ids_range():
    cmd = CmdAssignTx('10-15', 'cat1')
    eq_(cmd.tx_ids, [10, 11, 12, 13, 14, 15])


def test_cmd_assign_tx_parse_tx_ids_mixture():
    cmd = CmdAssignTx('1,3,7,10-15,9', 'cat1')
    eq_(cmd.tx_ids, [1, 3, 7, 9, 10, 11, 12, 13, 14, 15])


def test_cmd_assign_tx_parse_tx_ids_mixture_remove_duplicates():
    cmd = CmdAssignTx('1,3,3,10-15,11,1', 'cat1')
    eq_(cmd.tx_ids, [1, 3, 10, 11, 12, 13, 14, 15])
