from bdgt.commands import accounts, importer, transactions


__all__ = ['CommandFactory']


class CommandFactory(object):
    @classmethod
    def create(cls, args):
        assert hasattr(args, 'command')

        if args.command == 'account':
            return AccountCommandFactory.create(args)
        elif args.command == 'import':
            return ImportCommandFactory.create(args)
        elif args.command == 'tx':
            return TxCommandFactory.create(args)
        else:
            assert False


class AccountCommandFactory(object):
    @classmethod
    def create(cls, args):
        assert hasattr(args, 'sub_command')

        if args.sub_command == 'add':
            return accounts.CmdAddAccount(args.name, args.number)
        elif args.sub_command == 'delete':
            return accounts.CmdDeleteAccount(args.name)
        elif args.sub_command == 'list':
            return accounts.CmdListAccounts()
        else:
            assert False


class ImportCommandFactory(object):
    @classmethod
    def create(cls, args):
        return importer.CmdImport(args.account_name, args.type_, args.file_)


class TxCommandFactory(object):
    @classmethod
    def create(cls, args):
        assert hasattr(args, 'sub_command')

        if args.sub_command == 'list':
            return transactions.CmdListTx(args.account_name)
        elif args.sub_command == 'assign':
            return transactions.CmdAssignTx(args.transaction_ids,
                                            args.category_name)
        else:
            assert False
