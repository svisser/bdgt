from bdgt.commands import accounts, importer


__all__ = ['CommandFactory']


class CommandFactory(object):
    @classmethod
    def create(cls, args):
        assert hasattr(args, 'command')

        if args.command == 'account':
            return AccountCommandFactory.create(args)
        elif args.command == 'import':
            return ImportCommandFactory.create(args)
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
