import argparse
import logging
import os

from bdgt.commands.factory import CommandFactory
from bdgt.storage.database import open_database


_log = logging.getLogger(__name__)


def process_cmd(args):
    command = CommandFactory.create(args)
    output = command()
    print output


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--database')
    subparsers = parser.add_subparsers(dest='command')

    account_parser = subparsers.add_parser('account')
    account_subparsers = account_parser.add_subparsers(dest='sub_command')
    account_add_parser = account_subparsers.add_parser('add')
    account_add_parser.add_argument('name', type=unicode)
    account_subparsers.add_parser('list')
    account_delete_parser = account_subparsers.add_parser('delete')
    account_delete_parser.add_argument('name', type=unicode)

    args = parser.parse_args()

    # Open database
    if args.database:
        open_database(args.database)
    else:
        home_path = os.path.expanduser('~')
        if home_path == '~':
            raise RuntimeError("Unable to determine user's home folder.")
        bdgt_dir = os.path.join(home_path, ".bdgt")
        if not os.path.exists(bdgt_dir):
            os.makedirs(bdgt_dir)
        bdgt_db = os.path.join(bdgt_dir, "bdgt.db")
        open_database("sqlite:///{}".format(bdgt_db))

    # Process command
    process_cmd(args)
