from bdgt.commands import accounts, budget, importer, transactions


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
        elif args.command == 'set':
            return budget.CmdSet(args.category_name, args.period, args.amount)
        elif args.command == 'status':
            return budget.CmdStatus(args.month, args.year)
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
            return transactions.CmdAssignTx(args.category_name,
                                            args.transaction_ids)
        elif args.sub_command == 'unassign':
            return transactions.CmdUnassignTx(args.transaction_ids)
        elif args.sub_command == 'reconcile':
            return transactions.CmdReconcileTx(args.transaction_ids)
        else:
            assert False
