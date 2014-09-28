import os
import shlex
import subprocess

from bdgt.storage.database import open_database, session_scope
from bdgt.models import Account


TOP = os.path.join(os.path.dirname(__file__), "..")
TEST_DATABASE = 'sqlite:///test.db'


class Command(object):
    COMMAND_MAP = {
        "bdgt": {
            "bin": os.path.normpath("{0}/bin/bdgt".format(TOP)),
            "args": ['-d', TEST_DATABASE],
        }
    }

    @classmethod
    def run(cls, cmd):
        cmd_split = shlex.split(cmd)
        given_cmd = cmd_split[0]
        if given_cmd in cls.COMMAND_MAP:
            for arg in reversed(cls.COMMAND_MAP[given_cmd]["args"]):
                cmd_split.insert(1, arg)
            cmd_split[0] = cls.COMMAND_MAP[given_cmd]["bin"]
        return subprocess.check_output(cmd_split)


def before_scenario(context, scenario):
    # Ensure that the database is indeed empty
    with session_scope() as session:
        assert session.query(Account).count() == 0


def after_scenario(context, scenario):
    # Clear all records from the database
    with session_scope() as session:
        session.query(Account).delete()


def before_all(context):
    # Add the command executor to the context so steps can execute commands via
    # subprocess.
    context.cmd_line = Command

    # Create the database used during the test
    open_database(TEST_DATABASE)


def after_all(context):
    # Delete the database file
    if os.path.exists(TEST_DATABASE[10:]):
        os.remove(TEST_DATABASE[10:])
